from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date, timedelta

from models import BookCreate, BookResponse, BookUpdate, BorrowRequest, BookDetailResponse, Genre

router = APIRouter()

# ВАЖНО: импортируем main, а не из main
import main

# GET /books - получение списка всех книг с фильтрацией
@router.get("/books", response_model=List[BookResponse])
async def get_books(
    
    genre: Optional[Genre] = Query(None, description="Фильтр по жанру"),
    author: Optional[str] = Query(None, description="Фильтр по автору"),
    available_only: bool = Query(False, description="Только доступные книги"),
    skip: int = Query(0, ge=0, description="Количество книг для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит книг на странице")
):
    print(f"=== get_books вызван ===")
    print(f"books_db: {main.books_db}")
    """
    Получить список книг с возможностью фильтрации.
    """
    filtered_books = []
    
    for book_id, book_data in main.books_db.items():
        if genre and book_data["genre"] != genre:
            continue
        if author and author.lower() not in book_data["author"].lower():
            continue
        if available_only and not book_data.get("available", True):
            continue
        
        filtered_books.append(main.book_to_response(book_id, book_data))
    
    # Пагинация
    return filtered_books[skip:skip + limit]

# GET /books/{book_id} - получение книги по ID
@router.get("/books/{book_id}", response_model=BookDetailResponse)
async def get_book(book_id: int):
    """
    Получить информацию о книге по её ID.
    """
    if book_id not in main.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    book_data = main.books_db[book_id]
    response = BookDetailResponse(
        id=book_id,
        title=book_data["title"],
        author=book_data["author"],
        genre=book_data["genre"],
        publication_year=book_data["publication_year"],
        pages=book_data["pages"],
        isbn=book_data["isbn"],
        available=book_data.get("available", True)
    )
    
    if book_id in main.borrow_records:
        response.borrowed_by = main.borrow_records[book_id]["borrower_name"]
        response.borrowed_date = main.borrow_records[book_id]["borrowed_date"]
        response.return_date = main.borrow_records[book_id]["return_date"]
    
    return response

# POST /books - создание новой книги
@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate):
    """
    Создать новую книгу в библиотеке.
    """
    # Проверка уникальности ISBN
    for existing_book in main.books_db.values():
        if existing_book["isbn"] == book.isbn:
            raise HTTPException(
                status_code=400, 
                detail="Книга с таким ISBN уже существует"
            )
    
    book_id = main.get_next_id()

    # Сохраняем книгу
    main.books_db[book_id] = {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "publication_year": book.publication_year,
        "pages": book.pages,
        "isbn": book.isbn,
        "available": True
    }
    
    return main.book_to_response(book_id, main.books_db[book_id])

# POST /books/{book_id}/borrow - заимствование книги
@router.post("/books/{book_id}/borrow", response_model=BookDetailResponse)
async def borrow_book(book_id: int, borrow_request: BorrowRequest):
    """
    Взять книгу из библиотеки.
    """
    if book_id not in main.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    if not main.books_db[book_id].get("available", True):
        raise HTTPException(status_code=400, detail="Книга уже взята")

    # Обновляем статус книги
    main.books_db[book_id]["available"] = False
    
    # Создаем запись о заимствовании
    today = date.today()
    main.borrow_records[book_id] = {
        "borrower_name": borrow_request.borrower_name,
        "borrowed_date": today,
        "return_date": today + timedelta(days=borrow_request.return_days)
    }
    
    # Возвращаем обновленную информацию
    return await get_book(book_id)

# POST /books/{book_id}/return - возврат книги
@router.post("/books/{book_id}/return", response_model=BookResponse)
async def return_book(book_id: int):
    """
    Вернуть книгу в библиотеку.
    """
    if book_id not in main.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    if main.books_db[book_id].get("available", True):
        raise HTTPException(status_code=400, detail="Книга не была взята")
    
    # Обновляем статус книги
    main.books_db[book_id]["available"] = True
    
    if book_id in main.borrow_records:
        del main.borrow_records[book_id]
    
    return main.book_to_response(book_id, main.books_db[book_id])

# DELETE /books/{book_id} - удаление книги
@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    """
    Удалить книгу из библиотеки.
    """
    if book_id not in main.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if not main.books_db[book_id].get("available", True):
        raise HTTPException(status_code=400, detail="Нельзя удалить взятую книгу")

    del main.books_db[book_id]
    
    if book_id in main.borrow_records:
        del main.borrow_records[book_id]
    
    return None

# GET /stats - статистика библиотеки
@router.get("/stats")
async def get_library_stats():
    """
    Получить статистику библиотеки.
    """
    stats = {
        "total_books": len(main.books_db),
        "available_books": 0,
        "borrowed_books": 0,
        "books_by_genre": {},
        "most_prolific_author": None
    }
    
    author_count = {}
    
    for book_data in main.books_db.values():
        if book_data.get("available", True):
            stats["available_books"] += 1
        else:
            stats["borrowed_books"] += 1
        
        genre = book_data["genre"]
        stats["books_by_genre"][genre] = stats["books_by_genre"].get(genre, 0) + 1
        
        author = book_data["author"]
        author_count[author] = author_count.get(author, 0) + 1
    
    if author_count:
        stats["most_prolific_author"] = max(author_count, key=author_count.get)
    
    return stats