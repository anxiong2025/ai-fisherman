from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar: str | None
    role: str
    provider: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenVerifyResponse(BaseModel):
    valid: bool
    user: UserResponse | None = None
