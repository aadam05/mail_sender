import logging
from pydantic import BaseModel, EmailStr
from typing import Union, List


class EmailSchema(BaseModel):
    to: Union[EmailStr, List[EmailStr]]
    subject: str
    message: str

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValueError as e:
            logging.error(f"Invalid email address: {data.get('to')}")
            raise e
