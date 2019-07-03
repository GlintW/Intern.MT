import redis


class Consumer(object):

    def __init__(self, host, port=6379, auth=None):
        self.__r = redis.Redis(host=host, port=port, password=auth)

    def subscribe(self, list_name):
        while True:
            msg = self.__r.lpop(list_name)[1]
            print(msg.decode("utf-8"))

    def blocking_subscribe(self, list_name):
        while True:
            msg = self.__r.blpop(list_name)[1]
            print(msg.decode("utf-8"))


if __name__ == '__main__':
    c = Consumer("192.168.3.234", 6379)
    c.blocking_subscribe("pobby_queue")
