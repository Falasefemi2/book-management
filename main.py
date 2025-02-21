from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal,Book
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Define Pydantic model for request validation
class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    
# Add a new book to the database
@app.post("/books")
async def add_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(title=book.title, author=book.author, year=book.year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "Book added successfully", "book": new_book}

@app.get("/books")
def get_books(
    db: Session = Depends(get_db),
    year: int = Query(None, description="Filter books by publication year"),
    title: str = Query(None, description="Search books by title"),
    author: str = Query(None, description="Search books by author")
):
    query = db.query(Book)

    if year:
        query = query.filter(Book.year == year)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))  # Case-insensitive search
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    return query.all()

    
    

@app.get("/books/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
async def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update all fields
    book.title = book_data.title
    book.author = book_data.author
    book.year = book_data.year
    
    db.commit()
    db.refresh(book)
    return {"message": "Book updated successfully", "book": book}

@app.patch("/books/{book_id}")
async def update_book_partial(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Only update provided fields
    if book_update.title:
        book.title = book_update.title
    if book_update.author:
        book.author = book_update.author
    if book_update.year:
        book.year = book_update.year
    
    db.commit()
    db.refresh(book)
    return {"message": "Book updated successfully", "book": book}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()    
    
    return {"message": "Book deleted successfully"}