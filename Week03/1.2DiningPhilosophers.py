# 哲学家进餐：使用信号量
from threading import Condition, Thread, Semaphore
from time import sleep
from random import choice

res = []


def pickLeftFork(i):
    print(f'哲学家 {i} 拿起左边叉子。')
    res.append([i, 1, 1])
    sleep(0.2)


def pickRightFork(i):
    print(f'哲学家 {i} 拿起右边叉子。')
    res.append([i, 2, 1])
    sleep(0.2)


def eat(i):
    print(f'哲学家 {i} 进餐中……')
    res.append([i, 0, 3])
    sleep(choice([1, 2]))


def putLeftFork(i):
    print(f'哲学家 {i} 放下左边叉子。')
    res.append([i, 1, 2])
    sleep(0.2)


def putRightFork(i):
    print(f'哲学家 {i} 放下右边叉子。')
    res.append([i, 2, 2])
    sleep(0.2)


class DiningPhilosophers:

    def __init__(self):
        self.forks = [Semaphore() for _ in range(5)]  # 不能写成 [Semaphore()] * 5

    def wantsToEat(self, philosopher: int, *actions) -> None:
        a, b = self.forks[philosopher], self.forks[(philosopher+1) % 5]
        with a:
            with b:
                list(map(lambda func: func(philosopher), actions))


if __name__ == '__main__':
    threads = []
    d = DiningPhilosophers()
    for i in range(5):
        t = Thread(target=d.wantsToEat, args=(i, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(res)
    # print(len(res))
