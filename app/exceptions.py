from fastapi import HTTPException

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already exists")

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class GroupNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Group not found")