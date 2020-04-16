from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, String, Integer, select

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test",
    max_overflow=5,  # 超过连接池大小外最多可以创建的链接
    pool_size=10,  # 连接池大小
    echo=True,  # 调试信息展示
)

metadata = MetaData() # 取得元数据，介绍数据库
"""定义表"""
user = Table('user', metadata,
             Column("id", Integer, primary_key=True, autoincrement=True),  # 开启主键加快检索速度；开启自增长
             Column("name", String(10)))
# metadata.create_all(engine)  # 创建数据表

"""命令式写法"""
# # 插入数据
# engine.execute("insert into user (name) values ('lh')")
# # 更新表
# engine.execute("UPDATE USER SET id=5,name='python' where id=1")
# # 查看表
# res = engine.execute("select * from user ;")
# for i in res:
#     print(i)
# 删除
# engine.execute("delete from user where id=2")

"""函数式写法"""
conn = engine.connect()
# 插入数据
# conn.execute(user.insert(), {'name': "lder"})
# 更新数据
# conn.execute(user.update().where(user.c.id==6).values(name='lh2'))
# 查看数
# res = conn.execute((select([user.c.name, user.c.id])))
# print(res.fetchall())
# 删除数据
conn.execute(user.delete().where(user.c.id == 6))

conn.close()













