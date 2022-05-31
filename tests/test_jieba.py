import fast_jieba
from sparrow.performance import MeasureTime
from fast_jieba.analyse import extract_tags, textrank
import jieba
import time

ms = MeasureTime()

import random
tt = []
t = "小明就读北京清华大学物理系"
for i in range(1000):
    idx = random.randint(0, len(t) - 1)
    t += t[idx]
    t = t[idx] + t
    t += t[idx]
    t = t[idx] + t
    tt.append(t)

# texts = [tt for _ in range(4000)]
# print(tt[:2])
texts = tt
ms.start()
[fast_jieba.tokenize(text) for text in texts]
ms.show_interval(msg='fast jieba')

words = fast_jieba.batch_tokenize(texts, )
ms.show_interval('batch fast jieba')

[list(jieba.tokenize(text)) for text in texts]
ms.show_interval(msg="jieba")
