from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True


class SUserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
