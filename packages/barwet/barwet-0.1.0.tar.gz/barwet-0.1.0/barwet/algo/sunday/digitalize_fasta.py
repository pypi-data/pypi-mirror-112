"""将fasta序列数字化，保存到hdf5文件中"""
from collections import defaultdict
from typing import Callable
import h5py
import numpy as np
from Bio import SeqIO
from barwet.io import openFile
from barwet.log import getLogger
logger = getLogger(__name__)


# digitalize a str into np array.
def digitalize(seq_str: str, keys: str = 'NAGCT') -> np.ndarray:
    mappings = defaultdict(int)
    for i, v in enumerate(keys):
        mappings[v.upper()] = i
        mappings[v.lower()] = i
    return np.array([mappings[c] for c in seq_str], dtype='i1')


## write to fasta file.
def write_to_fasta(input_file: str, output_file: str):
    with openFile(input_file) as reader, \
    openFile(output_file, 'wb') as writer:
        for line_n in reader:
            line = line_n.strip()
            if line.startswith('>'):
                logger.info(f'now at {line}')
                writed_line = line_n
            elif not line:
                writed_line = line_n
            else:
                writed_line = digitalize(line) + '\n'
            writer.write(writed_line.encode('utf8'))


## write to hdf5 file.
def write_to_hdf5(input_file: str,
                  output_file: str,
                  key_fn: Callable[[str], str] = None):
    """
    Args:
        input_file: .fasta or .fna
        output_file: .h5
        key_fn: get dataset name from <SeqRecord>.id
    """
    if key_fn is None: key_fn = lambda x: x
    with openFile(input_file) as reader, \
    h5py.File(output_file, 'w') as h5:
        for record in SeqIO.parse(reader, 'fasta'):
            chr_id = key_fn(record.id)
            logger.info(f'Now at {chr_id}')
            digital_seq = digitalize(record.seq)
            h5.create_dataset(chr_id, data=digital_seq)


if __name__ == '__main__':
    input_file = '/home/barwe/data/barwe/pd/human/HumanGRCh38.fna.gz'
    # output_file = '/home/barwe/data/barwe/pd/human/HumanGRCh38.digit.fna.gz'
    output_file = '/home/barwe/data/barwe/pd/human/HumanGRCh38.digit.h5'
    key_fn = lambda s: s.split(' ')[0].split('|')[-1]
    write_to_hdf5(input_file, output_file, key_fn)
