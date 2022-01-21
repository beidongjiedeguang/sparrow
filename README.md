# sparrow_tool
[![image](https://img.shields.io/badge/Pypi-0.3.16-green.svg)](https://pypi.org/project/sparrow_tool)
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-GNU_GPL--v3-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-kunyuan-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)

## Requirements
```python
pyyaml
numpy
colour
pendulum
twine
cn2an
colorlog
concurrent-log-handler
Deprecated
fire
uvicorn>=0.16.0
fastapi
#GitPython
```

-------------------------
## Install
```bash
pip install sparrow-tool
```

## Usage

### Safe logger in `multiprocessing`
```python
from sparrow.log import Logger
import numpy as np
logger = Logger(name='train-log', log_dir='./logs', )
logger.info("hello","numpy:",np.arange(10))

logger2 = Logger.get_logger('train-log')
print(id(logger2) == id(logger))
>>> True
```

