from pydantic import BaseModel


class Phone(BaseModel):
    phone: int
    activation_id: int
