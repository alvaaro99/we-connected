class UserNotValidException(Exception):
    message:str
    status_code:str
    def __init__(self, message="User not Valid",status_code=400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)