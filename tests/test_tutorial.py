from cmath import log
import pytest
from sparrow.performance import MeasureTime
from sparrow.log import SimpleLogger
from sparrow import rel_to_abs


# parametrize 参数化测试用例, 意义就是
# 我们只需要编写一个测试用例，然后用这个装饰器 实现不同的值的测试用例 被多次执行。
# 这个优势，暂时看起来就是能然不同的测试用例执行起来清晰一点。。。
@pytest.mark.parametrize("value", [1, 2, "1", "2"])
def test_print_func(value):
    print(value)


# fixture 夹具，用于初始化的参数的，暂时没明白为啥大家都这么夸这玩意儿.
# 有点懂了，依旧是，后面每次调用这个参数时，都会被重新初始化
# 又有点懂了，这玩意儿可以看成是类中的__init__(), 这样我们的测试用例就不用写在类里面了。
@pytest.fixture(params=["a", "b", "c"])
def a_array(request):
    inputs = [1, 2, 3]
    log1 = SimpleLogger("log1", log_dir=rel_to_abs("./log1"))
    log2 = SimpleLogger("log2", log_dir=rel_to_abs("./log2"))
    return (inputs, log1, log2, request.param)  # request.param会依次将params里面的值返回去


def test_print1(a_array):
    print(a_array)
