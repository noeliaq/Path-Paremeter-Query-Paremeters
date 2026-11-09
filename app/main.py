from fastapi import FastAPI
from app.routers import books

app = FastAPI(
    title="A Library Search API",
    description="Search and filter library catalog books by title , author, genre",
    version="0.1.0"
)

app.include_router(books.router)

