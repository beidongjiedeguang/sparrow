from sparrow.log.core import Logger
from sparrow.ner import Extractor
from sparrow.log import SimpleLogger
from sparrow import rel_to_abs
import pytest


@pytest.fixture
def extractor():
    return Extractor()


@pytest.fixture
def logger():
    return SimpleLogger("extract-log", log_dir=rel_to_abs("log-ner"))


@pytest.mark.parametrize("text", ("我的手机号码是13120572919", "我的手机是+86-13120572919你还记得吗"))
def test_extractor(extractor: Extractor, logger: SimpleLogger, text: str):

    logger.debug(extractor.extract_cellphone(text))
    logger.debug(
        extractor.extract_email(
            "emmmm則我的email是beidongjiedeguang@gmail.com或者502245897@qq.com或者kunyuan@163.com"
        )
    )
    assert extractor.extract_email("emmmm則我的email是beidongjiedeguang@gmail.com或者") == [
        "beidongjiedeguang@gmail.com"
    ]

    assert extractor.extract_email("emmm怎麼說呢502245897@qq.com或者") == ["502245897@qq.com"]
