import threading
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test",
    max_overflow=5,  # 超过连接池大小外最多可以创建的链接
    pool_size=10,  # 连接池大小
    echo=True,  # 调试信息展示
)


Session = sessionmaker(bind=engine)
session = scoped_session(Session)

class MyThread(threading.Thread):

    def __init__(self, threadName):
        super(MyThread, self).__init__()

        self.threadname = threadName

    def run(self):
        # 每一个线程对应一个session，互不干扰
        sess = session()
        print(sess)

if __name__ == '__main__':
    arr = []
    for i in range(10):
        arr.append(MyThread("thread-%s") % i)
    for i in arr:
        i.start()
    for i in arr:
        arr.join()