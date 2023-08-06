import os

if __name__ == '__main__':
    import log
    import jsn
else:
    from . import log
    from . import jsn

logger = log.getLogger(__name__, level=log.INFO)
# logger = log.getLogger(__name__, level=log.DEBUG)


class Glovar(object):
    ## 单态
    __shared_state = {}

    ## 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, gvfile=None):
        """
        Args:
            gvfile: str, JSON file storing global variables.
        """
        super().__init__()
        ## 从单态字典中查询字段
        shared_file_path = self.__shared_state.get('gvfile')
        # 字段不存在时添加字段
        if shared_file_path is None:
            if gvfile is None:
                raise ValueError(f'`gvfile` cannot be None: {gvfile}')
            else:
                self.__shared_state['gvfile'] = gvfile
        # 字段存在时使用原字段值
        else:
            if gvfile is not None:
                logger.warn(f'Existed instance, `gvfile` will be ignored')
        ## 从单态字典更新对象属性字典
        self.__dict__ = self.__shared_state

    def _load(self):
        if os.path.exists(self.gvfile):
            d = jsn.load(self.gvfile)
            if isinstance(d, dict):
                return d
        return {}

    def get(self, k, default=None):
        d = self._load()
        return d.get(k, default)

    def set(self, k, v):
        d = self._load()
        d[k] = v
        jsn.dump(d, self.gvfile)

    def close(self):
        _ = os.system(f'rm -f {self.gvfile}')


def get_glovar(gvfile=None):
    return Glovar(gvfile)

def get(k):
    return Glovar().get(k)

if __name__ == '__main__':

    gv1 = Glovar('./test.json')
    gv1.set('name', 'barwe')
    gv2 = Glovar('a')
    print(gv2.get('name'))

    print(id(gv1), id(gv2))
    print(gv1.gvfile, gv2.gvfile)
    print(gv1.__dict__, gv2.__dict__)
