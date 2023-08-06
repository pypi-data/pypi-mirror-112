from pydantic import BaseModel


class Service(BaseModel):
    service: str
    count: int
    price: float
