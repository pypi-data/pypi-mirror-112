def auto_as(obj):
    if isinstance(obj, str):
        if obj.lower() == 'false':
            return False
        elif obj.lower() == 'true':
            return True
        else:
            try:
                _f = float(obj)
            except ValueError:
                # 不可转化为数值的字符串
                return obj
            else:
                try:
                    _i = int(obj)
                except ValueError:
                    # 可转化为浮点数但不能转化为整数的字符串
                    return _f
                else:
                    if _f == _i:
                        # 可转化为整数的字符串
                        return _i
                    else:
                        return _f

def getMismatchCounts(seq1: str, seq2: str):
    """
    Count number of mismatches between two strings.
    """
    assert len(seq1) == len(seq2), 'two string must be of same length'
    n = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            n += 1
    return n