from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import engine, Catalogue, CatalogueCreate

app = FastAPI()

@app.get("/catalogue")
def get_catalogue():
    with Session(engine) as session:
        return session.exec(select(Catalogue)).all()#makes it the list of dictionaries    

@app.post("/catalogue")
def add_book(book: CatalogueCreate):

    with Session(engine) as session:

        new_book = Catalogue(
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            releaseYear=book.releaseYear,
            description=book.description
        )

        session.add(new_book)

        session.commit()

        session.refresh(new_book)

        return {
            "message": "Book added successfully",
            "book": new_book
        }


# DELETE BOOK

@app.delete("/catalogue/{book_id}")
def delete_book(book_id: int):

    with Session(engine) as session:

        book = session.get(Catalogue, book_id)

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        session.delete(book)

        session.commit()

        return {
            "message": f"Book {book_id} deleted successfully"
        }

app.mount("/", StaticFiles(directory="static", html=True), name="static")