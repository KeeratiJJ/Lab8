from main import User, Book

def test_add_user(db_session):
    new_user = User(username="test_user1", fullname="Test User 1")
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter_by(username="test_user1").first()
    assert user is not None
    assert user.username == "test_user1"

def test_delete_user(db_session):
    user = User(username="test_user2", fullname="Test User 2")
    db_session.add(user)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(username="test_user2").first()
    assert deleted_user is None

def test_add_book(db_session):
    new_book = Book(title="Test Book 1", firstauthor="Author 1", isbn="1234567890")
    db_session.add(new_book)
    db_session.commit()

    book = db_session.query(Book).filter_by(isbn="1234567890").first()
    assert book is not None
    assert book.title == "Test Book 1"

def test_delete_book(db_session):
    book = Book(title="Test Book 2", firstauthor="Author 2", isbn="0987654321")
    db_session.add(book)
    db_session.commit()

    db_session.delete(book)
    db_session.commit()

    deleted_book = db_session.query(Book).filter_by(isbn="0987654321").first()
    assert deleted_book is None
