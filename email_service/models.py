import logging
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    to: EmailStr
    subject: str
    message: str

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValueError as e:
            logging.error(f"Invalid email address: {data.get('to')}")
            raise e
