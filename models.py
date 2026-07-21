from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

# 图书表模型
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


# 用户表模型
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


# 借阅记录表模型
class Borrow(db.Model):
    __tablename__ = 'borrows'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='borrowed')
    create_time = db.Column(db.DateTime, default=datetime.now)

    book = db.relationship('Book', backref='borrows')
    user = db.relationship('User', backref='borrows')

    def to_dict(self):
        return {
            'id': self.id,
            'bookId': self.book_id,
            'bookName': self.book.book_name if self.book else None,
            'userId': self.user_id,
            'userName': self.user.real_name if self.user else None,
            'borrowDate': self.borrow_date.strftime('%Y-%m-%d') if self.borrow_date else None,
            'returnDate': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'status': self.status
        }