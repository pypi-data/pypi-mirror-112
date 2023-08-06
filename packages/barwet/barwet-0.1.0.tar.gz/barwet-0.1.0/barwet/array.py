
from typing import Iterable

def sort(_iterable: Iterable, key=None, reverse=False):
    return sorted(_iterable, key, reverse)

def argsort(_iterable: Iterable, key=None, reverse=False):
    _it = sorted(enumerate(_iterable), key=key, reverse=reverse)
    index = [iv[0] for iv in _it]
    return index

def to_batch(arr, num_batches):
    size = len(arr)
    each_size = int(size / num_batches)
    batches = []
    for s in range(num_batches):
        e = (s + 1) * each_size
        if e > size:
            e = size
        batches.append(arr[s:e])
    return batches

def flatten(arr):
    flatted_arr = []
    for sub in arr:
        if isinstance(sub, Iterable):
            flatted_arr.extend(flatten(sub))
        else:
            flatted_arr.append(sub)
    return flatted_arr