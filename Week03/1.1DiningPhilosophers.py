# 哲学家进餐：使用条件变量
from collections import defaultdict
from threading import Condition, Thread
from time import sleep
from random import choice

res = []


def pick_left_fork(i):
    print(f'哲学家 {i} 拿起左边叉子。')
    res.append([i, 1, 1])
    sleep(0.2)


def pick_right_fork(i):
    print(f'哲学家 {i} 拿起右边叉子。')
    res.append([i, 2, 1])
    sleep(0.2)


def eat(i):
    print(f'哲学家 {i} 进餐中……')
    res.append([i, 0, 3])
    sleep(choice([1, 2]))


def put_left_fork(i):
    print(f'哲学家 {i} 放下左边叉子。')
    res.append([i, 1, 2])
    sleep(0.2)


def put_right_fork(i):
    print(f'哲学家 {i} 放下右边叉子。')
    res.append([i, 2, 2])
    sleep(0.2)


class DiningPhilosophers:
    """
    使用条件变量。
    定义哲学家字典：key 为哲学家索引号，value 表示是否正在进餐中。默认 False 表示没有进餐，True 表示正在进餐中。

    若哲学家左右都没人进餐，则该哲学家可以进行进餐了，即 dic[i-1] == False and dic[i+1] == False。
    哲学家个数有定数，注意边界值。进餐开始前要修改 value 的值，进餐结束后也要改回来。
    记得最后使用 notify_all 通知其他人。
    """
    def __init__(self):
        self.cond = Condition()
        self.dic = defaultdict(bool)

    def wants_to_eat(self, philosopher: int, *actions) -> None:
        # l_neighbor = philosopher - 1 if philosopher > 0 else 4
        # r_neighbor = philosopher + 1 if philosopher < 4 else 0

        l_neighbor, r_neighbor = (philosopher - 1) % 5, (philosopher + 1) % 5

        with self.cond:
            self.cond.wait_for(lambda: not self.dic[l_neighbor] and not self.dic[r_neighbor])
            self.dic[philosopher] = True

        # 写在外面，资源便于抢占。
        list(map(lambda func: func(philosopher), actions))

        with self.cond:
            self.dic[philosopher] = False
            self.cond.notify_all()


if __name__ == '__main__':
    threads = []
    d = DiningPhilosophers()
    for i in range(5):
        t = Thread(target=d.wants_to_eat, args=(i, pick_left_fork, pick_right_fork, eat, put_left_fork, put_right_fork))
        t.start()
        threads.append(t)

    # 等待子线程结束。若没该句，父线程先结束，res 取不到正确值。
    for t in threads:
        t.join()

    print(res)
