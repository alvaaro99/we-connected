class UserNotFoundException(Exception):
    message:str
    status_code:int
    def __init__(self, message="Email and/or passwords incorrect",status_code=404) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)