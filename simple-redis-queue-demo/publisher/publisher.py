import redis


class Publisher(object):

    def __init__(self, host, port=6379, auth=None):
        self.__r = redis.Redis(host=host, port=port, password=auth)

    def publish(self, list_name):
        while True:
            s = input("input: ")
            self.__r.rpush(list_name, s)


if __name__ == '__main__':
    c = Publisher("192.168.3.234", 6379)
    c.publish("pobby_queue")
