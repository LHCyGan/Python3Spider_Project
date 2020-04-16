from sqlalchemy import create_engine, Table
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test",
    max_overflow=5,
    pool_size=10,
    echo=True,
)

class HOST(BASE):
    # 表名
    __tablename__ = 'hosts2'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=8080)
# # 创建
BASE.metadata.create_all(engine)

#
if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    sess = Session()  # 创建实例
    h1 = HOST(hostname='test1', ip="127.0.0.1")
    h2 = HOST(hostname='test2', ip="192.168.0.1", port=80)
    h3 = HOST(hostname='test3', ip='198.3.2.1')
    # 添加
    # sess.add(h1)
    # sess.add_all([h2, h3])
    # 删除
    # sess.query(HOST).filter(HOST.id==1).delete()
    # 更新
    # sess.query(HOST).filter(HOST.id==3).update({'port':3066})
    # 查询
    res = sess.query(HOST).filter_by(id = 3).all()
    for i in res:
        print(i)

    sess.commit()  # 提交