from threading import Thread

#gil是cpython的产物，python， jvm对java， jython， pypy
#1. 既然gil保证安全，但是gil又有时间片的概念
#2. gil会保证字节码的安全

total = 0


def add():
    global total
    for i in range(1000000):
        total += 1


def desc():
    global total
    for i in range(1000000):
        total -= 1


if __name__ == "__main__":
    add_thread = Thread(target=add)
    desc_thread = Thread(target=desc)

    add_thread.start()
    desc_thread.start()

    add_thread.join()
    desc_thread.join()
    print(total)