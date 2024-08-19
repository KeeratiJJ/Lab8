from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal, User, Book
import pytest


client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_and_delete_user():
    # Create user
    response = client.post("/users/", json={"username": "testuser", "fullname": "Test User"})
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == "testuser"
    assert user["fullname"] == "Test User"
    
    # Get verify
    response = client.get(f"/borrowlist/{user['id']}")
    assert response.status_code == 404 

def test_create_and_delete_book():
    # Create book
    response = client.post("/books/", json={"title": "Test Book", "firstauthor": "Test Author", "isbn": "1234567890"})
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == "Test Book"
    assert book["firstauthor"] == "Test Author"
    assert book["isbn"] == "1234567890"

def test_borrow_book():
    # Create user
    response = client.post("/users/", json={"username": "testuser", "fullname": "Test User"})
    assert response.status_code == 200
    user = response.json()

    # Create book
    response = client.post("/books/", json={"title": "Test Book", "firstauthor": "Test Author", "isbn": "1234567890"})
    assert response.status_code == 200
    book = response.json()

    # Borrow book
    response = client.post("/borrowlist/", json={"user_id": user["id"], "book_id": book["id"]})
    assert response.status_code == 200
    borrow_entry = response.json()
    assert borrow_entry["user_id"] == user["id"]
    assert borrow_entry["book_id"] == book["id"]

    # Check borrowed books
    response = client.get(f"/borrowlist/{user['id']}")
    assert response.status_code == 200
    borrowed_books = response.json()
    assert len(borrowed_books) == 1
    assert borrowed_books[0]["book_id"] == book["id"]

