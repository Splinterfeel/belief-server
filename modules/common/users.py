import hashlib
from orm import Session
from orm.common import User
from sqlalchemy import exc
from schemas import AddUser


def hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def add_user(user: AddUser) -> bool:
    with Session() as session:
        new_user = User()
        new_user.login = user.login
        new_user.password = hash(user.password)
        try:
            session.add(new_user)
            session.commit()
        except exc.IntegrityError:
            return False  # login exists
        return True
