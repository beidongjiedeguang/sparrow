from multiprocessing.managers import SyncManager, BaseManager
from typing import TypeVar
from queue import Queue


class QueueManager(BaseManager):
    queue = Queue()

    def get_queue(self) -> Queue:
        pass


DictProxy = TypeVar('DictProxy')
class DataManager(SyncManager):
    data = {}

    def get_data(self) -> DictProxy:
        pass


QueueManager.register('get_queue', callable=lambda: QueueManager.queue)
DataManager.register('get_data', callable=lambda: DataManager.data)
if __name__ == "__main__":
    manager = DataManager(address=('0.0.0.0', 50001), authkey=b'kunyuan')
    manager.get_server().serve_forever()
