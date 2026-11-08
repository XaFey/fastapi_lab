from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import uvicorn

app = FastAPI()
#define complex object models
class Author(BaseModel):
    name: str
    email: Optional[str] = None

class Book(BaseModel):
    id: int
    title: str
    author: Author
    year: int
    genre: str
    #add book ratings
    ratings: List[int] = []
####SECURITY THING
#authentication and authorization with httpbasic
security = HTTPBasic()

def security_check(credentials: HTTPBasicCredentials= Depends(security)):
    if credentials.username == "admin" and credentials.password == "password":
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

#in-memory dataset
books = [
    Book(
        id=1,
        title="The Great Gatsby",
        author=Author(name="F. Scott Fitzgerald", email="fscottfitzgerald@example.com"),
        year=1925,
        genre="Fiction",
        ratings=[1,2,4]

    ),
    Book(
        id=2,
        title= "1984",
        author=Author(name="George Orwell", email="georgeorwell@example.com"),
        year=1949,
        genre="Dystopian",
        ratings=[4,5,3]

    )
]

#Get all books
@app.get("/books/all/", response_model=List[Book])
async def get_all_books():
    return books

#Get a book by ID
@app.get("/books/get/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

#POST a new book
@app.post("/books/create/", response_model=Book, dependencies=[Depends(security_check)])
async def create_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book)
    return book

#PUT a new book
@app.put("/books/update/{book_id}", response_model=Book,dependencies=[Depends(security_check)])
async def update_book(book_id: int, book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = book
            return book
    raise HTTPException(status_code=404, detail="Book not found")

#DELETE a new book
@app.delete("/books/delete/{book_id}", response_model=Book,dependencies=[Depends(security_check)])
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

#Search books by genre
@app.get("/books/search/{genre}", response_model=List[Book])
async def search_books_by_genre(genre: str):
    for i in books:
        if i.genre.lower()== genre.lower():
            return {"message": "Book found", "book": i}
    raise HTTPException(status_code=404, detail="Book not found")

#Book Count
@app.get("books/count")
async def book_count():
    return {"count": len(books)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
