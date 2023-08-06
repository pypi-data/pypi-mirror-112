import h5py
from typing import List
import numba as nb
import numpy as np
from Bio import SeqIO
from timeit import timeit
from barwet.io import openFile
from barwet.log import getLogger

logger = getLogger(__name__)


## 从文件加载用于测试的探针列表
def load_demo_probes(fp: str) -> List[str]:
    probes = []
    with openFile(fp) as r:
        for _p in r:
            p = _p.strip()
            if p:
                probes.append(p)
    return probes


## 将探针数字化
from digitalize_fasta import digitalize


def digitalize_probes(probes: List[str]) -> np.ndarray:
    p_num = len(probes)
    p_len = len(probes[0])
    digital_probes = np.zeros(shape=(p_num, p_len), dtype='i1')
    for i, p in enumerate(probes):
        digital_probes[i, :] = digitalize(p)
    return digital_probes


## Load digital genome from fasta file.
def load_digital_genome_from_fasta(fp: str):
    with openFile(fp) as reader:
        records = []
        for record in SeqIO.parse(reader, 'fasta'):
            print(record.id)
            seq_digit = np.array([int(i) for i in record.seq], 'i1')
            records.append(seq_digit)
            break
    return records


## Load digital genome from hdf5 file.
## Return a Generator object.
def load_digital_genome_from_hdf5(fp: str):
    chrdata = {}
    with h5py.File(fp, 'r') as db:
        for chrname in db.keys():
            chrseq = np.array(db[chrname], dtype='i1')
            chrdata[chrname] = chrseq
            # yield chrname, chrseq
    return chrdata


@nb.njit(nogil=True)
def search_probe_in_chr(chrseq: np.ndarray, probe: np.ndarray,
                        mismatches: int) -> int:
    c_len = chrseq.size
    p_len = probe.size

    char_pos = {}
    for idx, char in enumerate(probe):
        char_pos[char] = idx

    index = 0  # 母串上与子串首字符比较的位置
    while index <= c_len - p_len:
        num_mismatches = 0  # 当前位置下的错配数
        for i, pi in enumerate(probe):
            # 子串第i个字符与母串第index+i个字符不匹配时
            if chrseq[index + i] != pi:
                num_mismatches += 1
                # 当错配数超过阈值时考虑移动子串
                if num_mismatches > mismatches:
                    # 下一个移动位置超过母串长度时，匹配失败
                    if index + p_len >= c_len:
                        return -1
                    # 否则可以继续移动子串
                    pos = char_pos.get(chrseq[index + p_len])
                    if pos is None:
                        index += p_len + 1
                    else:
                        index += p_len - pos
                    break
        if num_mismatches <= mismatches:
            return index
    return -1


@nb.njit(nogil=True)
def search_probes_in_chr(chrseq, probes, mismatches):
    """
    Args:
        chrseq: [C_LEN,]
        probes: [P_NUM, P_LEN]
    Returns:
        np.ndarray[P_NUM,] index of each probe located in chromosome.
    """
    p_num = probes.shape[0]
    # logger.info(f'chromosome length: {c_len}, probe length: {p_len}, probe counts: {p_num}')

    positions = np.empty((p_num, ), dtype='int64')
    for idx in nb.prange(p_num):
        positions[idx] = search_probe_in_chr(chrseq, probes[idx, :],
                                             mismatches)

    return positions


from multiprocessing import pool


def search_async(chrseq, probes, mismatches, processes):
    """将单个探针的在单个染色体上的搜索下发到子进程"""
    p_num = probes.shape[0]
    positions = np.empty((p_num, ), dtype='int64')
    results: List[pool.AsyncResult] = []
    p = pool.Pool(processes)
    for i in nb.prange(p_num):
        args = [chrseq, probes[i, :], mismatches]
        results.append(p.apply_async(search_probe_in_chr, args))
    p.close()
    p.join()
    positions = [r.get() for r in results]
    return np.array(positions, dtype='int64')


if __name__ == '__main__':

    genome = load_digital_genome_from_hdf5(
        '/home/barwe/data/barwe/pd/human/HumanGRCh38.digit.h5')
    probes = digitalize_probes(
        load_demo_probes('/home/barwe/data/barwe/pd/human/probes.txt.gz')[:20])

    for chrname, chrseq in genome.items():
        logger.info(f'Searching in chromosome: {chrname}')
        # print(timeit(lambda: search_probes_in_chr(chrseq, probes, 1), number=2)) # 17.14
        print(timeit(lambda: search_async(chrseq, probes, 1, 4), number=1))  #
        print(timeit(lambda: search_async(chrseq, probes, 1, 6), number=1))  #
        print(timeit(lambda: search_async(chrseq, probes, 1, 8), number=1))  #
        break