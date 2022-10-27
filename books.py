
from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'book_1': {'title ': 'title one', 'author ':' author one '},
    'book_2': {'title ': 'title two', 'author ': ' author two '},
    'book_3': {'title ': 'title three', 'author ': ' author three '},
    'book_4': {'title ': 'title four', 'author ': ' author four '},
    'book_5': {'title ': 'title five', 'author ': ' author five'}
}

@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.spilt('_')[-1])
            if x > current_book_id:
                current_book_id = x
                
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_information
    return book_information

@app.delete("/{book_name}")
async def delete_book(book_name):
    del BOOKS[book_name]
    return f'Book_{book_name} is deleted. '

@app.get("/")
async def read_all_books():
    return BOOKS

@app.get("/{book_name}")
async def read_book(book_name:str):
    return BOOKS[book_name]