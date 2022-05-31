from sparrow.multiprocess.server import DataManager, QueueManager
from sparrow.multiprocess.config import Config


class Client:
    """
    Example:
    First start service:
    ~$ sparrow start-server
    >>> from sparrow.multiprocess.client import Client
    >>> client = Client()
    >>> client.update_data({'a': 1, 'b': 2})
    >>> print(client.get_data())
    """
    def __init__(self):
        server_config = Config()
        manager = DataManager(address=(server_config.host, server_config.port), authkey=b'kunyuan')
        manager.connect()
        self._dict = manager.get_data()

    def update_data(self, data: dict):
        self._dict.update(data)

    def get_data(self):
        """Return a copy of original data."""
        return dict(self._dict.items())

    def get_raw_data(self):
        return self._dict

