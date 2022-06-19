import os

from sparrow.proto.python import trainstatus_pb2
from sparrow import rel_to_abs

if not os.path.exists('./bin'):
    os.mkdir('./bin')


# productor
def productor():
    state = trainstatus_pb2.TrainStatus()

    state.step = 100
    state.finished = True
    state.progress = 0.5
    state.loss = 1.2

    with open(rel_to_abs("./bin/train_state.bin"), "wb") as f:
        f.write(state.SerializeToString())


# consumer
def consumer():
    state = trainstatus_pb2.TrainStatus()
    with open(rel_to_abs("./bin/train_state.bin"), "rb") as f:
        state.ParseFromString(f.read())

    print(state, type(state))


productor()
consumer()
