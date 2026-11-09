from pydantic import BaseModel, Field
from enum import Enum

class SortField(str, Enum): #defines the allowed choices for which columm user is permitted to sort by
    title = "title"
    author = "author"
    rating = "rating"
    year = "year "

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    rating: float
    year: int
    available: bool