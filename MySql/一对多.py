from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test2",
    max_overflow=5,
    pool_size=10,
    echo=True
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    gender = Column(String(10), nullable=True, default='男')
    town = Column(String(128))
    language = relationship('Language', backref='user',
                            cascade='all, delete')  # 自动删除关联数据

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
    try:
        """添加"""
        # # 添加用户
        # u1 = User(name='刘恒', gender='男', town="陕西宝鸡")
        # u2 = User(name='李德', gender='女', town='陕西榆林')
        # session.add_all([u1, u2])
        # session.commit()
        # # 添加语言
        # l1 = Language(name='python', advantage='简单，易操作', disadvantage='运行速度慢')
        # l1.user = u1
        # session.add(l1)
        # session.commit()
        # 同时添加
        # u3 = User(name='lyy', gender='女', town='上海')
        # u3.language = [Language(name='C++', advantage='运行快', disadvantage='结构复杂,不易上手'),
        #                Language(name='C', advantage='万能')]
        # session.add(u3)
        # session.commit()
        """查找"""
        # u = session.query(User).filter_by(id=6).first()
        # print(u.name)
        # lan = session.query(Language).filter_by(user_id=u.id).all()
        # for l in lan:
        #     print(l.name)
        """删除"""
        # u = session.query(User).filter_by(id=6).first()
        # session.delete(u)
        # session.commit()
        """更新"""
        # u = session.query(User).filter_by(id=1).first()
        # u.name = 'lh'
        # session.commit()
        #
        # u = session.query(User).filter_by(id=1).first()
        # lan = u.language[0].name='python3'
        # session.commit()
    except:
        # 修改过程中发生错误，回滚到修改之前
        session.rollback()
