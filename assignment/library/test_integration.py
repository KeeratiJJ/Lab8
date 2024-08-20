import pytest
from fastapi.testclient import TestClient
from main import app, Base, engine, get_db, User, Book, Borrowlist
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_library.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Recreate the database tables for testing
Base.metadata.create_all(bind=test_engine)

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_and_get_borrowlist(client, db_session):
    # Create user
    response = client.post("/users/", params={"username": "test_user3", "fullname": "Test User 3"})
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Create book
    response = client.post("/books/", params={"title": "Test Book 3", "firstauthor": "Author 3", "isbn": "1122334455"})
    assert response.status_code == 200
    book_id = response.json()["id"]

    # Create borrowlist entry
    response = client.post("/borrowlist/", params={"user_id": user_id, "book_id": book_id})
    assert response.status_code == 200

    # Get borrowlist for the user
    response = client.get(f"/borrowlist/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["book_id"] == book_id
