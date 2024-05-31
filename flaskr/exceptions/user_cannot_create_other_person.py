class UserCannotCreateOtherPerson(Exception):
    message:str
    status_code:int
    def __init__(self, message="You cannot create other person",status_code=400) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)