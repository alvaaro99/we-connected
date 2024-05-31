from flaskr.db import get_db
from ..models.User import User
import re
from . import password_service
from ..exceptions.user_not_valid_exception import UserNotValidException
from sqlite3 import IntegrityError

def create_user(user: User):

    if not validate_user(user):
        raise UserNotValidException()

    user.password = password_service.encrypt_pass(user.password)

    db = get_db()
    try:
        db.execute('INSERT INTO user (email,password) VALUES (?,?)',(user.email,user.password))
        db.commit()
    except IntegrityError as e:
        raise e
    
def find_user_by_email(email: str):

    db = get_db()
    try:
        user = db.execute('SELECT * from user WHERE email = ? ',(email,)).fetchone()
        db.commit()
    except Exception as e:
        raise e
    
    return user

def is_same_password(password_to_login:str,stored_password:str):
    if password_to_login == password_service.decrypt_pass(stored_password):
        return True
    return False

def validate_user(user: User):
    if not validate_email(user.email) or not validate_password(user.password):
        return False
    return True

def validate_email(email: str):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email) is not None


def validate_password(password:str):
    return re.match(r"^(?=(?:.*[a-zA-Z]){5,}).{5,}$", password) is not None