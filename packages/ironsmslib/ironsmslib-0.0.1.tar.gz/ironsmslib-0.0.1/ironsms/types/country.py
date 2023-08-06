from typing import List

from pydantic import BaseModel

from ironsms.types import Service


class Country(BaseModel):
    country: str
    services: List[Service]
