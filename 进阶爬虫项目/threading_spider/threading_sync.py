from threading import Thread
from threading import Lock
#线程间同步
#库存

total = 0
total_lock = Lock()

def get_kc():
    return 1

def save_kc(kc):
    return True

def buy1(good_id):
    #1. 从数据库获取库存

    kc = get_kc()
    if kc:
        #2.记录购买
        pass
        #3. 库存减一
        kc -= 1
        save_kc()
    else:
        return False

def buy2(good_id):
    #1. 从数据库获取库存
    kc = get_kc()
    if kc:
        #2.记录购买
        pass
        #3. 库存减一
        kc -= 1
        save_kc()
    else:
        return False


def add():
    total_lock.acquire()
    global total
    for i in range(1000000):
        total += 1
    total_lock.release()


def desc():
    total_lock.acquire()
    global total
    for i in range(1000000):
        total -= 1
    total_lock.release()


if __name__ == "__main__":
    add_thread = Thread(target=add)
    desc_thread = Thread(target=desc)

    add_thread.start()
    desc_thread.start()

    add_thread.join()
    desc_thread.join()
    print(total)