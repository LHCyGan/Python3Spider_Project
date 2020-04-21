#1. 实例化Thread
#2. 继承Thread类
import time
from threading import Thread


def sleep_task(sleep_time):
    print("sleep {} seconds start!".format(sleep_time))
    time.sleep(sleep_time)
    print("sleep {} seconds end!".format(sleep_time))


class SleepThread(Thread):
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time
        super().__init__()

    def run(self):
        print("sleep {} seconds start!".format(self.sleep_time))
        time.sleep(self.sleep_time)
        print("sleep {} seconds end!".format(self.sleep_time))


# if __name__ == "__main__":
#     start_time = time.time()
#     t1 = Thread(target=sleep_task, args=(2,))
#     t1.setDaemon(True)
#     t1.start()
#
#     t2 = Thread(target=sleep_task, args=(3,))
#     t2.setDaemon(True)
#     t2.start()
#
#     # t1.join()
#     # t2.join()
#     time.sleep(1)
#     end_time = time.time()
#     print("last_time: {}".format(end_time-start_time))
#
#     #1.当开启一个程序的时候，会默认启动一个主线程
#     #2. 如何在主线等到其他线程执行完以后才继续执行, join, setDaemon

if __name__ == "__main__":
    t1 = SleepThread(2)
    t2 = SleepThread(3)
    t1.start()
    t2.start()