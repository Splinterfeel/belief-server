import hashlib
import uuid
from orm import Session
from orm.common import User, Resource, ResourceGain
from sqlalchemy import exc
from modules.common import schemas
from modules.stronghold.main import create_initial_user_stronghold


def hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def get_user_resources(user_id: int) -> schemas.UserResourcesDTO:
    with Session() as session:
        return schemas.UserResourcesDTO.model_validate(
            session.query(Resource).where(Resource.user_id == user_id).one()
        )


def add_user(user: schemas.User) -> bool:
    with Session() as session:
        new_user = User()
        new_user.login = user.login
        new_user.password = hash(user.password)
        try:
            session.add(new_user)
            session.commit()
        except exc.IntegrityError:
            return False  # login exists
        create_initial_user_resources(new_user.id)
        create_initial_user_stronghold(new_user)
        return True


def create_initial_user_resources(user_id: int) -> None:
    with Session() as session:
        resources = Resource(user_id=user_id)
        resources_gain = ResourceGain(user_id=user_id)
        session.add(resources)
        session.add(resources_gain)
        session.commit()


def check_cookie(cookie: str) -> bool:
    # TODO make expire for cookie
    cookie = str(cookie)  # just in case
    with Session() as session:
        row_exists = session.query(User.cookie).filter(User.cookie == cookie).one_or_none()
        if row_exists:
            return True
        return False


def auth_user(user: schemas.User) -> schemas.AuthResult:
    with Session() as session:
        password_hash = hash(user.password)
        db_user = session.query(User).filter(
            User.login == user.login, User.password == password_hash).one_or_none()
        if db_user:
            cookie = f"{db_user.login}_{uuid.uuid4()}"
            print('set cookie', cookie)
            db_user.cookie = cookie
            session.commit()
            return schemas.AuthResult(
                successful=True, user=schemas.AuthUser.model_validate(db_user))
        return schemas.AuthResult(successful=False)
