from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_, and_

Base = declarative_base()

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test3",
    max_overflow=5,
    pool_size=10,
    echo=True
)

# 创建第三张表
User2Lan = Table('user_2_language',
                 Base.metadata,
                 Column('user_id', ForeignKey('user.id'), primary_key=True),
                 Column('language_id', ForeignKey('language.id'), primary_key=True))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    gender = Column(String(10), nullable=True, default='男')
    town = Column(String(128))
    language = relationship('Language', backref='user',
                            cascade='all, delete',  # 自动删除关联数据
                            secondary=User2Lan)  # 使用第三张表

class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    advantage = Column(String(128), nullable=True, default='无')
    disadvantage = Column(String(128), nullable=True, default='无')
    user_id = Column(Integer, ForeignKey('user.id'))

Base.metadata.create_all(engine)


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    """添加"""
    # 1.
    # 添加用户
    # u1 = User(name="张三", gender='男', town='北京')
    # u2 = User(name="李四", gender='女', town='天津')
    # session.add_all([u1, u2])
    # # 添加语言
    # l1 = Language(name='python', advantage='开发快', disadvantage='运行慢')
    # l1.user.append(u1)
    # session.add(l1)
    # session.commit()
    # 2. 同时添加
    # u3 = User(name='王五', gender='女', town='陕西')
    # u3.language = [
    #     Language(name='c++', advantage='运行快', disadvantage='开发慢'),
    #     Language(name='c', advantage='运行快', disadvantage='开发最慢')
    # ]
    # session.add(u3)
    # session.commit()
    """删除"""
    # 1.创建删除
    # u3 = User(name='王五', gender='女', town='陕西')
    # u3.language = [
    #     Language(name='c++', advantage='运行快', disadvantage='开发慢'),
    #     Language(name='c', advantage='运行快', disadvantage='开发最慢')
    # ]
    # session.add(u3)
    # session.commit()
    # session.delete(u3)
    # session.commit()
    # 2.查询删除
    # u3 = User(name='王五', gender='女', town='陕西')
    # u3.language = [
    #     Language(name='c++', advantage='运行快', disadvantage='开发慢'),
    #     Language(name='c', advantage='运行快', disadvantage='开发最慢')
    # ]
    # session.add(u3)
    # res = session.query(User).filter_by(id==3).first()
    # session.delete(res)
    # session.commit()
    """修改"""
    # u3 = User(name='王五', gender='女', town='陕西')
    # u3.language = [
    #     Language(name='c++', advantage='运行快', disadvantage='开发慢'),
    #     Language(name='c', advantage='运行快', disadvantage='开发最慢')
    # ]
    # session.add(u3)
    # res = session.query(User).filter_by(id==3).first()
    # res.language[0].name = 'pytohn3'
    # session.commit()
    """查找"""
    # 1. 数量
    number = session.query(User).filter(User.id > 0).count()
    print(number)
    # 2. 查找排序 -User.id:降序，User.id:升序
    u = session.query(User).order_by(-User.id).all()[:2]
    print(u)
    # 3. or_, and_
    print(session.query(User).filter(or_(User.id==1, User.id==3)).all())
    print(session.query(User).filter(and_(User.id==1, User.id==3)).all())
    # 4.模糊匹配
    # %：0个或任意多个字符
    # _:表示任意单个字符
    # []:表示括号内任意一个字符
    # [^]:表示不是括号内的字符
    print(session.query(User).filter(User.name.like("_三")).all())
