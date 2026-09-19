book = []
next_id = 1

def add_book(title, author, year, price):
    
    if price < 0 or price > 10000:
        raise ValueError("Цена книги должна быть в диапазоне от 0 до 10000")
    
    global next_id
    
    books = {
        "id": next_id,
        "title": title,
        "author": author,
        "year": year,
        "price": price
    }
    
    book.append(books)
    next_id += 1
    
    return books

# book = add_book("Война и мир", "Лев Толстой", 1869, 500) 
# print(book)  # Вывод информации о добавленной книге


def get_books():
    return book

def update_book(id, title, author, year, price):
    for books in book:
        if books["id"] == id:
            books["title"] = title
            books["author"] = author
            books["year"] = year
            books["price"] = price
            return books
    return None

def delete_book(id):
    for books in book:
        if books["id"] == id:
            book.remove(books)
            return True
    return False
