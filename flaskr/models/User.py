import datetime

class User():
    email:str
    password:str
    created_at:datetime

    def __init__(self,email,password,created_at=None) -> None:
        self.email = email
        self.password = password
        self.created_at = created_at