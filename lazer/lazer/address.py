from typing import TypedDict


class Address(TypedDict):
    zipcode: int
    city: str
    state: str
    country: str
