from logics_book import add_book

def test_add_book():
    book = add_book(
        "Война и мир", 
        "Лев Толстой", 
        1869, 
        500
    )
    
    assert book["id"] == 1
    assert book["title"] == "Война и мир"
    assert book["author"] == "Лев Толстой"
    assert book["year"] == 1869
    assert book["price"] == 500