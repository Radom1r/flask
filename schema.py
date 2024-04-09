import pydantic

class CreateUser(pydantic.BaseModel):
    username: str
    password: str

class CreateAdv(pydantic.BaseModel):
    title: str
    description: str
    user: int