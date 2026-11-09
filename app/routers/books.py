from fastapi import APIRouter, HTTPException, Query, Path
from app.schemas.book import BookResponse, SortField
from typing import Optional


router = APIRouter(prefix="/books", tags=["Books"]) #organize APi into separate modular files . "Books"header in swagger

#Books Data

books_db =[
    {"id": 1, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "rating": 4.7, "year": 1949, "available": True,
    },
    {"id": 2, "title": "Animal Farm", "author": "George Orwell", "genre": "Satire", "rating": 4.6, "year": 1945, "available": True,
    },
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "rating": 4.8, "year": 1813, "available": False,
    },
    {"id": 4, "title": "Sense and Sensibility", "author": "Jane Austen", "genre": "Romance", "rating": 4.4, "year": 1811, "available": True,
    }, 
    {"id": 5, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 4.9, "year": 1937, "available": True,
    }, 
    {"id": 6, "title": "The Fellowsip of the Ring", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 4.9, "year": 1954, "available": False,
    }, 
    {"id": 7, "title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "rating": 4.7, "year": 1965, "available": True,
    }, 
    {"id": 8, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "rating": 4.8, "year": 1960, "available": True,
    }, 
    {"id": 9, "title": "Dune Messiah", "author": "Frank Herbert", "genre": "Sci-Fi", "rating": 4.3, "year": 1969, "available": True,
    }, 
    {"id": 10, "title": "Go Set a Watchman", "author": "Harper Lee", "genre": "Classic", "rating": 3.7, "year": 2015, "available": False,
    }, 
                            
]
#route decorator. Registers an httop GET endpoint and configures URL path and schema

@router.get ("/{book_id}", response_model=BookResponse)

#constrain Path - Parameter validation
def get_book(
    book_id: int = Path(gt=0, description="The ID of the book")

):
    #Get specific book id or 404 if it doens't exist
    for book in books_db:
        if book ["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book ID: {book_id} not found")

@router.get ("/", response_model=list[BookResponse])

#GET /books — Search and filter books with query parameters:
def list_books(
    genre: Optional[str] = Query(default=None),
    min_rating: Optional[float] = Query(default = 0, ge=0, le= 5,description= "Minimum rating (0-5)"),
    sort_by: SortField = SortField.title,
    skip: int= Query(default=0, ge=0),
    limit: Optional[int] = Query(default=10, ge=1, le=100),
):
  # .copy is to avoid accidentally modifyimg or corruptiong your original books_db in memory
    results = books_db.copy()

#list comprehensive 
    if genre:
        results=[book for book in results if book["genre"].lower() == genre.lower()]
    if min_rating is not None and min_rating >0:
        results = [book for book in results if book["rating"] >= min_rating] 

    #sort ,use of key function.
    results.sort(key=lambda book: book[sort_by.value])

    #paginate
    #start = skip , stop = skip +limit
    results = results[skip:skip +limit]
    return results 

#List all books by a given author
author_db= {
1: {"id": 1, "name": "George Orwell"},
2: {"id": 2, "name": "Jane Austen"},
3: {"id": 3, "name": "J.R.R. Tolkien"},
4: {"id": 4, "name": "Frank Herbert"},
5: {"id": 5, "name": "Harper Lee"},
}

@router.get("/authors/{author_id}/books", response_model=list[BookResponse]) 


def list_author_books(
    author_id: int= Path(gt=0, description="The Author's id"),
    sort_by: SortField = SortField.title
    ):

    author = author_db.get(author_id)
    if not author:
        raise HTTPException(
            status_code=404, detail="Author ID Not found "
        )
    #Get all books by specific author 

    results = [book for book in books_db if book["author"].lower() ==author["name"].lower() ]
    results.sort(key=lambda book: book[sort_by.value])
    return results









