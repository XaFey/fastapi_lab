from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Data models
class Author(BaseModel):
    name: str
    email: Optional[str] = None

class Book(BaseModel):
    id: int
    title: str
    author: Author
    year: int
    genre: str
    ratings: List[int] = []

# HTTP Basic Authentication
security = HTTPBasic()

def security_check(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" and credentials.password == "password":
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"}
    )

# In-memory dataset
books: List[Book] = [
    Book(
        id=1,
        title="The Great Gatsby",
        author=Author(name="F. Scott Fitzgerald", email="fscottfitzgerald@example.com"),
        year=1925,
        genre="Fiction",
        ratings=[1, 2, 4]
    ),
    Book(
        id=2,
        title="1984",
        author=Author(name="George Orwell", email="georgeorwell@example.com"),
        year=1949,
        genre="Dystopian",
        ratings=[4, 5, 3]
    )
]

# Get all books
@app.get("/books/all", response_model=List[Book])
async def get_all_books():
    return books

# Exercise 5: Book count
@app.get("/books/count")
async def book_count():
    return {"count": len(books)}

# Exercise 1: Search books by genre
@app.get("/books/search/{genre}", response_model=List[Book])
async def search_books_by_genre(genre: str):
    matched = [b for b in books if b.genre.lower() == genre.lower()]
    return matched

# Get single book by ID
@app.get("/books/get/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Exercise 2: Create a book (Secured)
@app.post("/books/create", response_model=Book, dependencies=[Depends(security_check)])
async def create_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book)
    return book

# Full update: PUT (Secured)
@app.put("/books/update/{book_id}", response_model=Book, dependencies=[Depends(security_check)])
async def update_book(book_id: int, book: Book):
    for i, b in enumerate(books):
        if b.id == book_id:
            books[i] = book
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Exercise 4: Delete a book (Secured)
@app.delete("/books/delete/{book_id}", dependencies=[Depends(security_check)])
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)