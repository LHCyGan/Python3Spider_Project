import threading
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test",
    max_overflow=5,  # 超过连接池大小外最多可以创建的链接
    pool_size=10,  # 连接池大小
    echo=True,  # 调试信息展示
    pool_timeout=10,  # 池中没有线程最多等待时间，否则报错
    pool_recycle=-1,  # 线程多久回收一次， -1不回收
)


Session = sessionmaker(bind=engine)
session = scoped_session(Session)
# 同一线程同一session， 避免在不同线程获取同一session，造成线程安全问题
a = session()
b = session()
print(a, b, sep='\n')