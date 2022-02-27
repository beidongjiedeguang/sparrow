import logging
import numpy as np
from sparrow.version_ops import VersionControl
from sparrow.color.constant import *
from sparrow.core import *
from sparrow.string.color_string import rgb_string
from sparrow.decorators import *
from sparrow.string.color_string import rgb_string
from sparrow.time import *
import time


# vc = VersionControl("sparrow-tool")
# vc.update_version(1)


# @repeat(10)
@benchmark
@optional_debug
@broadcast
def function(n):
    s = n
    time.sleep(0.1)
    return s


if __name__ == "__main__":
    print(rgb_string("hello rgb string", YELLOW))
    print(rgb_string("hello rgb string", GREEN))
    print(rgb_string("hello rgb string", [1., 1., 1.]))
    color = np.array([0.5, 0.5, 1.])
    print(rgb_string("hello rgb string", color))
    print(rgb_string("hello rgb string", [23, 233, 233]))
    print(rgb_string("hello rgb string", np.array([23, 233, 233])))
    # print(function(300, 23, 432, debug=True))
    # print(function(200))
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # # 声明了一个 Logger 对象
    # logger = logging.getLogger(__name__)
    #
    # logger.info("Start print log")
    # logger.debug("Do something")
    # logger.warning("Something maybe fail.")
    # logger.info("Finish")
    # print(inspect.signature(function))
    # bj = Beijing()
    # print(bj.now)
