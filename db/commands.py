import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import User, Case, Data, Drunk, Eaten, Calla, Urine
from db.settings import engine


def add_user(telegram_id, username):
    with Session(engine) as session:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()
    return True


def check_user(telegram_id):
    with Session(engine) as session:
        is_member = session.scalar(select(User).where(User.telegram_id == telegram_id))
    if is_member:
        return True
    return False


def add_case(case_id, user_id, date_start, age, height, weight):
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


def add_one_eaten(case_id, data):
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
    with Session(engine) as session:
        item = Urine(
            case_id=case_id,
            date=datetime.datetime.today(),
            urine=data
        )
        session.add(item)
        session.commit()
    return True
