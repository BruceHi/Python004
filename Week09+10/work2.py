# 作业二：自定义一个 python 函数，实现 map() 函数的功能。
from operator import add

# map 结果演示
a = map(int, '1234')
print(list(a))

b = map(add, [1, 2, 3, 4], [1, 2, 3, 4])
print(list(b))

c = map(add, [1, 2, 3], [1, 2, 3, 4])
print(list(c))


def map2(func, *iterables):
    for args in zip(*iterables):
        yield func(*args)


a = map2(int, '1234')
print(list(a))

b = map2(add, [1, 2, 3, 4], [1, 2, 3, 4])
print(list(b))

c = map2(add, [1, 2, 3], [1, 2, 3, 4])
print(list(c))
