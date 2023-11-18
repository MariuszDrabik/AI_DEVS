from datetime import datetime
from typing import Generic, Optional, TypeVar, Union
from pydantic import UUID4, BaseModel, Field
from pydantic.generics import GenericModel


class QuestionSchema(BaseModel):
    question: str

class ReplySchama(BaseModel):
    reply: str