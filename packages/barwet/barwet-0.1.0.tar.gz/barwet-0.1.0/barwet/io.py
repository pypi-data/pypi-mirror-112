import re

def openFile(filepath: str, mode='r'):
    if filepath.endswith('.gz'):
        import gzip
        _mode = 'rt' if mode == 'r' else mode
        return gzip.open(filepath, _mode)
    if filepath.endswith('.bz2'):
        import bz2
        _mode = 'rt' if mode == 'r' else mode
        return bz2.open(filepath, _mode)
    else:
        return open(filepath, mode)


def write_once(fp: str, data):
    """
        写入一个数据到一个文件，然后关闭文件
        :param fp:
        :param data: 任意类型的数据
        :param data_type: 数据的类型，与Python3的类型注解一致
            支持的类型有:
            1. str 写入一个字符串
            2. List[str] 写入一个字符串数组
        :return:
        """

    text = None
    if isinstance(data, str):
        text = data
    elif isinstance(data, list):
        if any([isinstance(i, str) for i in data]):
            text = '\n'.join(data)
        elif any([isinstance(i, int) for i in data]):
            text = '\n'.join([int(i) for i in data])

    if text is None:
        raise ValueError('Not supported type')

    with open(fp, 'w') as writer:
        writer.write(text)


def read_chunk(fp: str, chunk_size=512):
    with openFile(fp) as reader:
        while True:
            chunk = reader.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def iterate_fasta(fn, replace_degenerate=True, seq_header=False):

    degenerate_pattern = re.compile('[YRWSMKBDHV]')

    def process(f):
        curr_header = ''
        curr_seq = ''
        for line in f:
            line = line.rstrip()
            if len(line) == 0:
                # Skip the blank line
                continue
            if line.startswith('>'):
                # Yield the current sequence (if there is one) and reset the
                # sequence being read
                if len(curr_seq) > 0:
                    if seq_header:
                        yield curr_seq, curr_header
                    else:
                        yield curr_seq
                curr_header = line
                curr_seq = ''
            else:
                # Append the sequence
                if replace_degenerate:
                    line = degenerate_pattern.sub('N', line)
                curr_seq += line
        
        if len(curr_seq) > 0:
            if seq_header:
                yield curr_seq, curr_header
            else:
                yield curr_seq

    with openFile(fn) as reader:
        yield from process(reader)