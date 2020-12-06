# 实现一个 @timer 装饰器，记录函数的运行时间
from time import time, sleep


def timer(func):
    def inner(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        end = time()
        print(f'该函数运行了 {end-start} 秒')
        return res
    return inner


@timer
def list_sleep(nums):
    sleep(0.1)
    return nums


a = list_sleep(range(10))
print(a)
