from sqlalchemy import Column, INTEGER, BIGINT, VARCHAR, DATE, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase

from db.settings import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(BIGINT, primary_key=True, nullable=False, comment='telegram id пользователя')
    username = Column(VARCHAR(255), unique=False, nullable=True, comment='username пользователя, если он есть')
    is_moderator = Column(Boolean, default=False, comment='флаг модератора')


class Case(Base):
    __tablename__ = 'cases'

    case_id = Column(INTEGER, primary_key=True, unique=True, nullable=False, comment='номер истории болезни')
    user_id = Column(BIGINT, ForeignKey('users.telegram_id'), comment='поле для связи с моделью User')
    user = relationship('User', )
    date_start = Column(DATE, nullable=False, comment='дата госпитализации')
    age = Column(INTEGER, nullable=False, comment='возраст')
    height = Column(INTEGER, nullable=False, comment='рост')
    weight = Column(INTEGER, nullable=False, comment='вес')
    is_active = Column(Boolean, default=True, comment='открытый/закрытый')

    def __repr__(self):
        return f'case_id:{self.case_id} user_id:{self.user_id} date_start:{self.date_start}'


class Data(Base):
    __tablename__ = 'data'

    data_id = Column(INTEGER, primary_key=True, autoincrement=True)
    case_id = Column(INTEGER, ForeignKey('cases.case_id'))
    date = Column(DATE, nullable=False, comment='Дата записи')
    eaten = Column(INTEGER, default=0, comment='Объем съеденного')
    drunk = Column(INTEGER, default=0, comment='Объем выпитой жидкости')
    calla = Column(INTEGER, default=0, comment='Количество стула')
    urine = Column(INTEGER, default=0, comment='Объем мочи')


class Eaten(Base):
    __tablename__ = 'eaten'

    entry_id = Column(INTEGER, primary_key=True, autoincrement=True)
    case_id = Column(INTEGER, ForeignKey('cases.case_id'))
    date = Column(DateTime, nullable=False, comment='Дата записи')
    eaten = Column(INTEGER, default=0, comment='Объем съеденной порции')


class Drunk(Base):
    __tablename__ = 'drunk'

    entry_id = Column(INTEGER, primary_key=True, autoincrement=True)
    case_id = Column(INTEGER, ForeignKey('cases.case_id'))
    date = Column(DateTime, nullable=False, comment='Дата записи')
    drunk = Column(INTEGER, default=0, comment='Объем выпитой порции')


class Calla(Base):
    __tablename__ = 'calla'

    entry_id = Column(INTEGER, primary_key=True, autoincrement=True)
    case_id = Column(INTEGER, ForeignKey('cases.case_id'))
    date = Column(DateTime, nullable=False, comment='Дата записи')
    calla = Column(INTEGER, default=0, comment='Количество стула')


class Urine(Base):
    __tablename__ = 'urine'

    entry_id = Column(INTEGER, primary_key=True, autoincrement=True)
    case_id = Column(INTEGER, ForeignKey('cases.case_id'))
    date = Column(DateTime, nullable=False, comment='Дата записи')
    urine = Column(INTEGER, default=0, comment='Разовый объем мочи')


def create_table():
    with engine.begin():
        Base.metadata.create_all(engine)
