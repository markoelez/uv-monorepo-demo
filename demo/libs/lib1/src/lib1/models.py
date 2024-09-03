import requests
from pydantic import BaseModel


class TestModel(BaseModel):
    name: str
    age: int = 2
