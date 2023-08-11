import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import User, Case, Drunk, Eaten, Calla, Urine
from db.settings import engine


def add_user(telegram_id, username):
    """Добавление нового пользователя телеграм в БД"""
    with Session(engine) as session:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()
    return True


def one_user(telegram_id):
    """Получение данных пользователя по телеграм ID, возвращает атрибут is_moderator"""
    with Session(engine) as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return user.is_moderator


def check_user(telegram_id):
    """Проверка есть ли пользователь в БД"""
    with Session(engine) as session:
        is_member = session.scalar(select(User).where(User.telegram_id == telegram_id))
    if is_member:
        return True
    return False


def show_users_without_moderation():
    """Список пользователей без прав модератора"""
    users_list = []
    with Session(engine) as session:
        users = session.query(User).filter(User.is_moderator == False).all()
        for user in users:
            users_list.append((user.telegram_id, user.username))
    return users_list


def give_moderation(telegram_id):
    """Назначение модератором"""
    with Session(engine) as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        user.is_moderator = True
        session.commit()


def show_moderators():
    """Список пользователей-модераторов"""
    users_list = []
    with Session(engine) as session:
        users = session.query(User).filter(User.is_moderator == True).all()
        for user in users:
            users_list.append((user.telegram_id, user.username))
    return users_list


def delete_moderator(telegram_id):
    """Удаление из модераторов"""
    with Session(engine) as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        user.is_moderator = False
        session.commit()


def add_case(case_id, user_id, date_start, age, height, weight):
    """Добавление случая госпитализации в БД"""
    with Session(engine) as session:
        case = Case(
            case_id=case_id,
            user_id=user_id,
            date_start=date_start,
            age=age,
            height=height,
            weight=weight,
        )
        session.add(case)
        session.commit()
    return True


def get_all_cases():
    with Session(engine) as session:
        cases = session.query(Case).all()  # получаем список объектов таблицы cases
    return cases


def switch_case_status(case_id):
    with Session(engine) as session:
        case = session.query(Case).filter(Case.case_id == case_id).first()
        if case.is_active:
            case.is_active = False
        else:
            case.is_active = True
        session.commit()


def delete_cases():
    with Session(engine) as session:
        session.query(Case).filter(Case.is_active == False).delete(synchronize_session="fetch")
        session.commit()


def add_one_eaten(case_id, data):
    """Добавление записи о съеденном"""
    with Session(engine) as session:
        item = Eaten(
            case_id=case_id,
            date=datetime.datetime.today(),
            eaten=data
        )
        session.add(item)
        session.commit()
    return True


def add_one_drink(case_id, data):
    """Добавление записи о выпитом"""
    with Session(engine) as session:
        item = Drunk(
            case_id=case_id,
            date=datetime.datetime.today(),
            drunk=data
        )
        session.add(item)
        session.commit()
    return True


def add_one_calla(case_id, data):
    """Добавление записи об однократном стуле"""
    with Session(engine) as session:
        item = Calla(
            case_id=case_id,
            date=datetime.datetime.today(),
            calla=data
        )
        session.add(item)
        session.commit()
    return True


def add_one_urine(case_id, data):
    """Добавление записи об объеме разовой порции мочи"""
    with Session(engine) as session:
        item = Urine(
            case_id=case_id,
            date=datetime.datetime.today(),
            urine=data
        )
        session.add(item)
        session.commit()
    return True


def get_eaten_per_time(case_id, date):
    with Session(engine) as session:
        volume = session.query(Eaten.eaten).filter(Eaten.case_id == case_id, Eaten.date >= date).all()
    return volume


def get_drunk_per_time(case_id, date):
    with Session(engine) as session:
        volume = session.query(Drunk.drunk).filter(Drunk.case_id == case_id, Drunk.date >= date).all()
    return volume


def get_urine_per_time(case_id, date):
    with Session(engine) as session:
        volume = session.query(Urine.urine).filter(Urine.case_id == case_id, Urine.date >= date).all()
    return volume


def get_calla_per_time(case_id, date):
    with Session(engine) as session:
        volume = session.query(Calla.calla).filter(Calla.case_id == case_id, Calla.date >= date).all()
    return volume


def get_weight(case_id):
    with Session(engine) as session:
        weight = session.query(Case.weight).filter(Case.case_id == case_id)
    return weight[0][0]
