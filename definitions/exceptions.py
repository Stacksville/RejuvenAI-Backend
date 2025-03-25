from fastapi import HTTPException, status


class NoUserException(HTTPException):
    def __init__(self) -> None:
        self.status = status.HTTP_401_UNAUTHORIZED
        self.detail = "No user with provided identifier exists"
        super().__init__(status_code=self.status, detail=self.detail)


class InvalidJWSException(HTTPException):
    def __init__(self) -> None:
        self.status = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not verify authenticity of token"
        super().__init__(status_code=self.status, detail=self.detail)


class MissingAuthorizationHeaderException(HTTPException):
    def __init__(self) -> None:
        self.status = status.HTTP_401_UNAUTHORIZED
        self.detail = "Authorization header might be missing"
        super().__init__(status_code=self.status, detail=self.detail)
