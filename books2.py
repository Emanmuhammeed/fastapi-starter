from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse

app = FastAPI()
BOOKS = []

class NegativeNumException(Exception):
    def __int__(self, book_to_return):
        self.book_to_return = book_to_return

class Book(BaseModel):
    id: int = Field(title=" the id of book")
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="what book do",min_length=1, max_length=100)
    rate: int =Field(gt=-1, lt=101)

class BookNoRating(BaseModel):
    id: int = Field(title=" the id of book")
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None,
                                       title="what book do",
                                       min_length=1,
                                       max_length=100)

@app.post("/book/login")
async def book_login(user_name: str = Form(...), password: str = Form(...)):
    return {'User name': user_name, 'Password': password}

@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}

@app.get("/")
async def read_all_books():
    return BOOKS

@app.get("/book/{book_id}")
async def read_book(book_id :int):
    for x in BOOKS :
        if x.id == book_id:
            return  x
    raise raise_item_con_not_be_found_exception()

@app.get("/book/rating/{book_id}", response_model= BookNoRating)
async def read_book_no_rating(book_id :int):
    for x in BOOKS :
        if x.id == book_id:
            return  x
    raise raise_item_con_not_be_found_exception()

@app.post("/", status_code= status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id=int, book=Book):
    counter = 0

    for x in BOOKS :
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]

@app.delete("/{book_id}")
async def delete_book(book_id=int):
    counter = 0

    for x in BOOKS :
        counter += 1
        if x.id == book_id:
            del BOOKS[counter -1]
            return f'ID :{book_id} is deleted. '
    raise raise_item_con_not_be_found_exception()

@app.exception_handlers(NegativeNumException)
async def negative_number_exception_handler(request :Request , exception :NegativeNumException):
    return JSONResponse(status_code=418 ,
                        content= {"message": f'f Hey Why do you want {exception.book_to_return} You Need To Read More'})


def create_book_with_no_api():
    book_1 = Book(id=1, title=" book 1", author="author one", rate=40)
    book_2 = Book(id=2, title=" book 2", author="author two", rate=50)
    book_3 = Book(id=3, title=" book 3", author="author three", rate=60)
    book_4 = Book(id=4, title=" book 4", author="author four", rate=70)
    book_5 = Book(id=5, title=" book 5", author="author five", rate=80)

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)

async def raise_item_con_not_be_found_exception():
    return HTTPException(status_code=404,
                         headers={"X-Header-Error": "no thing to see at UUID"},
                         detail="can not be founded")



