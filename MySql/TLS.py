import threading


"""
同一个local, 对于不同的线程， 不同value,;
同一线程， 同一value  --线程隔离
"""

# 主线程中开启local, 只能主线程访问
a = threading.local()
a.value = 9

def change(name):
    try:
        print(threading.current_thread().name, a.value)
    except AttributeError:
        print(threading.current_thread().name, 'no value')

    a.value = name
    print(threading.current_thread().name, a.value)


for i in range(3):
    threading.Thread(target=change, args=(i, )).start()
print(threading.current_thread().name, a.value)