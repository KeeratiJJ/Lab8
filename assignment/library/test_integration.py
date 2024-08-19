from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal, User, Book, Borrowlist
import pytest

# Create a new TestClient instance
client = TestClient(app)

# Fixture to create and drop tables for each test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test creating a borrow entry and retrieving borrowed books
def test_create_and_get_borrowlist():
    # Create a user
    response = client.post("/users/", json={"username": "testuser", "fullname": "Test User"})
    assert response.status_code == 200
    user = response.json()

    # Create a book
    response = client.post("/books/", json={"title": "Test Book", "firstauthor": "Test Author", "isbn": "1234567890"})
    assert response.status_code == 200
    book = response.json()

    # Create a borrow entry
    response = client.post("/borrowlist/", json={"user_id": user["id"], "book_id": book["id"]})
    assert response.status_code == 200
    borrow_entry = response.json()
    assert borrow_entry["user_id"] == user["id"]
    assert borrow_entry["book_id"] == book["id"]

    # Retrieve borrowed books for the user
    response = client.get(f"/borrowlist/{user['id']}")
    assert response.status_code == 200
    borrowed_books = response.json()
    assert len(borrowed_books) == 1
    assert borrowed_books[0]["user_id"] == user["id"]
    assert borrowed_books[0]["book_id"] == book["id"]

