import redis
import json


class Person(object):

    def __init__(self, name, age, gender):
        self.__name = name
        self.__age = age
        self.__gender = gender

    def get_name(self):
        return self.__name

    def to_string(self):
        return '''{name: "%s", age: %f, gender: "%s"}''' % (self.__name, self.__age, self.__gender)


class DataOperation(object):

    def __init__(self, host, port=6379, auth=None):
        self.__r = redis.Redis(host=host, port=port, password=auth)

    def add_person(self, person):
        name = person.get_name()
        if self.__r.get(name) is None:
            j = json.dumps(person.to_string())
            self.__r.set(name, j)
            print("[%s]存储成功" % j)
        else:
            print("[%s]已存在" % name)

    def query_person(self, name):
        value = self.__r.get(name)
        return value.decode("utf-8")

    def del_person(self, name):
        if self.__r.get(name) is None:
            print("[%s]不存在" % name)
        else:
            self.__r.delete(name)
            print("[%s]删除成功" % name)


def test():
    p1 = Person("pobby", 23, "female")
    p2 = Person("glint", 24, "female")
    p3 = Person("cc", 25, "male")
    p4 = Person("fool", 26, "male")

    op = DataOperation("192.168.3.234", 6379)

    op.add_person(p1)
    result = op.query_person("pobby")
    print(result)

    op.add_person(p2)
    result = op.query_person("glint")
    print(result)

    op.add_person(p3)
    result = op.query_person("cc")
    print(result)

    op.add_person(p4)
    result = op.query_person("fool")
    print(result)

    op.del_person("pobby")
    op.del_person("glint")
    op.del_person("cc")
    op.del_person("fool")


if __name__ == "__main__":
    test()
