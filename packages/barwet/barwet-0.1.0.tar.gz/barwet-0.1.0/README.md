`ecotools` 提供了一些常用的方法，写一些小程序时十分方便。

# 安装

初次安装：

```
pip install -i https://pypi.python.org/simple ecotools
```

更新：

```
pip install -i https://pypi.python.org/simple --upgrade barwet
```

# 子模块

## json

对内置的 `json` 模块进行了封装，提供了几个常用的函数。

引入：
```python
from ecotools import json
```

下面四个函数封装了内置 `json` 模块的对应函数：
* `dump(obj: Any, fp: str, indent: int=4, **kwargs)`: 导出数据到文件
* `dumps(obj: Any, indent: int=None,  **kwargs)`: 导出数据为字符串
* `load(fp: str, **kwargs)`: 从文件加载数据
* `loads(s: str, **kwargs)`: 从字符串加载数据

下面是额外的工具函数：
* `dump_jstr(jstr: str, fp: str, indent: int=4, **kwargs)`: 将json字符串保存到文件
* `load_from_simple_yaml(fp: str, sep=':', header=False)`: 从简单的yaml配置文件加载json数据。文件每一行的格式为 `key: value`。

## logging

提供了一个 `Logger` 类，用于初始化一个日志记录器对象:
```python
from ecotools.logging import Logger
```

**Logger**

* `__init__(self, name, output_dir=None, use_timestamp=True)`
* `write(self, string)`: 写入一条消息
* `set_dir(self, output_dir)`: 更改输入目录

通常使用静态方法 `get_logger()` 获取实例：
`get_logger(name, output_dir=None, suffix='log', use_timestamp=True)`

## path

对路径的相关操作:
```python
from ecotools.path import *
```

`if_file_exists(file_path, return_bool=False)`

检查文件是否存在，不存在抛出 `FileNotFoundError` 异常。

`check_dir(dir_path: str, return_abspath=False)`

检查目录是否存在，不存在则创建，返回目录路径。

## status

使用json文件记录状态。

**class JStatus**
```python
from ecotools import JStatus
```
* `__init__(self, fp: str)`
* `set(self, key: str, val: BaseType)`: 修改键值对
* `get(self, key: str)`: 查询键值对

## vprint

打印格式控制:
```python
from ecotools import vprint
```

* `center(msg: str, decorator='#', width=80)`

