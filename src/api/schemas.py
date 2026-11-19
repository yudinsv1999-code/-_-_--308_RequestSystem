from pydantic import BaseModel, Field
from typing import Optional

class RequestCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    category_id: int

class RequestAssign(BaseModel):
    executor_id: int

class StatusChange(BaseModel):
    status_id: int

class CommentCreate(BaseModel):
    text: str = Field(min_length=1)

class RequestOut(BaseModel):
    id: int
    number: str
    title: str
    description: str
    applicant_id: int
    executor_id: Optional[int] = None
    status_id: int
    category_id: int

class CommentOut(BaseModel):
    id: int
    request_id: int
    user_id: int
    text: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

class ErrorOut(BaseModel):
    error: str
    detail: str
