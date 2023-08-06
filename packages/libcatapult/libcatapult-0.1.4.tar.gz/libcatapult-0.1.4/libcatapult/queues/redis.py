import redis as redis

from libcatapult.queues.base_queue import BaseQueue, NotConnectedException


class RedisQueue(BaseQueue):
    """
    RedisQueue is an implementation of BaseQueue for talking to redis queues.
    """

    def __init__(self, host: str, port: str):
        """
        RedisQueue requires the host and port parameters
        :param host: host name of the redis servers
        :param port: port number ot connect to.
        """
        super().__init__()
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = redis.Redis(host=self.host, port=self.port, db=0)

        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def publish(self, channel: str, message: str):
        if not self.connection:
            raise NotConnectedException()
        self.connection.rpush(channel, message)
