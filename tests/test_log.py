import logging
from sparrow.log.core import Logger, SimpleLogger
from sparrow import yaml_load
from sparrow import rel_to_abs
import time
# import logging
# from logtest1 import func1
from multiprocessing import Process, context
import multiprocessing


def test_simple_log():
    # simp
    logger = SimpleLogger.get_logger(name="train-log", log_dir=rel_to_abs("./log"), print_stream=True)
    logger.debug("hello", "list", [1, 2, 3, 4, 5])
    logger2 = SimpleLogger.get_logger(name="train-log", )
    print(id(logger2) == id(logger))
    assert (id(logger2) == id(logger))


def test_simplelog_log():
    logger = SimpleLogger.get_logger("emmm")
    logger.log(logging.DEBUG, "hahahhah")


def test_logger():
    logger = Logger(name="train-log", log_dir=rel_to_abs("./log"), print_debug=True)
    logger.debug("hello", "list", [1, 2, 3, 4, 5])
    logger2 = Logger.get_logger("train-log")
    print(id(logger2) == id(logger))


def test_log():
    logger = Logger(name="train-log", log_dir=rel_to_abs("./log"), print_debug=True)
    logger.debug("hello", "list", [1, 2, 3, 4, 5])

    logger2 = Logger.get_logger("train-log")
    print(id(logger2) == id(logger))

    def get_logger(i, name="name"):
        # logger = Logger(name=name, log_dir=f"./logs/2022-01-12-{i}", print_error=True, single_mode=True, multi_process=False)
        logger = SimpleLogger(
            name=name,
            log_dir=rel_to_abs(f"./logemm/2022-01-12-{i}"),
            print_stream=True,
            multi_process=False,
        )
        return logger

    logger1 = get_logger(1, "emm")

    # def func1(n=2):
    #     with multiprocessing.Pool(2) as p:
    #         p.apply(func=f, args=(n,))

    def f(n, logger):
        for i in range(n):
            time.sleep(0.01)
            logger.debug("em 我在debug")
            # logger.info("额")
            # logger.warning(f"emmmm, {i}")
            logger.error("粗错啦")

    f(2, logger1)
