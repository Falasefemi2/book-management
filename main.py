from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
# from database import SessionLocal,Book
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import asc, desc
from auth import hash_password
# from models import User
from schemas import UserCreate
from fastapi.security import  OAuth2PasswordRequestForm
from auth import verify_password, create_access_token, get_current_user
from datetime import timedelta
from database import SessionLocal, Book, User



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
async def add_book(book: BookCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    return {"message": f"Book added successfully by {current_user}"}



@app.get("/books")
async def get_books(
    db: Session = Depends(get_db),
    year: int = Query(None, description="Filter books by publication year"),
    title: str = Query(None, description="Search books by title"),
    author: str = Query(None, description="Search books by author"),
    sort_by: str = Query("title", regex="^(title|author|year)$", description="Sort books by title, author, or year"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sorting order: 'asc' or 'desc'"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return per oage")
):
    query = db.query(Book)

    if year:
        query = query.filter(Book.year == year)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))  # Case-insensitive search
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    
    # Sorting logic
    sort_column = getattr(Book, sort_by)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    
    total = query.count()
    books = query.offset(skip).limit(limit).all()
    
    return {"total": total, "books": books}

    
    

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

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token= create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

