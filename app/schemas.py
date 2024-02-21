from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing_extensions import Annotated



# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

## rether then this, this is best way 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int 
    owner: UserOut                              
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str 



class UserLogin(BaseModel):
    email: EmailStr
    password: str

# class Post(BaseModel):
#     id: int
#     title:str
#     content: str
#     published: bool
#     created_at: datetime
    
#     class Config:
#         orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

#creating schema for Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    # dir: Annotated[int, Field(strict=True, gt=0)]

class PostWithVotes(Post):
    votes: int
    