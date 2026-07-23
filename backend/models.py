from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(100))
    isbn = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(50))
    total_count = db.Column(db.Integer, default=1)
    available_count = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # ✅ 关键：在父模型这边定义 relationship，并设置 passive_deletes='all'
    borrows = db.relationship('Borrow', backref='book', passive_deletes='all')

    def to_dict(self):
        return {
            'id': self.id,
            'bookName': self.book_name,
            'author': self.author,
            'publisher': self.publisher,
            'isbn': self.isbn,
            'category': self.category,
            'totalCount': self.total_count,
            'availableCount': self.available_count,
            'createTime': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'updateTime': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    real_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='user')
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'realName': self.real_name,
            'phone': self.phone,
            'role': self.role
        }


class Borrow(db.Model):
    __tablename__ = 'borrows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # 不再是外键
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='borrowed')
    create_time = db.Column(db.DateTime, default=datetime.now)

    # ❌ 删掉这一行，因为已经在 Book 那边定义过了
    # book = db.relationship('Book', backref='borrows', passive_deletes='all')

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_name': self.book.book_name if self.book else None,
            'user_id': self.user_id,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d') if self.borrow_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'status': self.status
        }