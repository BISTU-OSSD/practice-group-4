from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Book, User, Borrow
from datetime import date

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 允许跨域（前端访问用）
CORS(app)

# ============================================
# 图书管理接口（增删改查）
# ============================================

# 1. 查询所有图书 + 搜索
@app.route('/api/books', methods=['GET'])
def get_books():
    keyword = request.args.get('keyword', '').strip()
    if keyword:
        books = Book.query.filter(
            Book.book_name.contains(keyword) | Book.author.contains(keyword)
        ).order_by(Book.id.desc()).all()
    else:
        books = Book.query.order_by(Book.id.desc()).all()
    
    return jsonify({
        'code': 200,
        'data': [book.to_dict() for book in books]
    })


# 2. 根据ID查询单本图书
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'message': '图书不存在'})
    return jsonify({'code': 200, 'data': book.to_dict()})


# 3. 添加图书
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    
    if not data.get('bookName') or not data.get('author'):
        return jsonify({'code': 400, 'message': '书名和作者不能为空'})
    
    book = Book(
        book_name=data['bookName'],
        author=data['author'],
        publisher=data.get('publisher', ''),
        isbn=data.get('isbn', ''),
        category=data.get('category', ''),
        total_count=data.get('totalCount', 1),
        available_count=data.get('totalCount', 1)
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '添加成功', 'data': book.to_dict()})


# 4. 修改图书
@app.route('/api/books', methods=['PUT'])
def update_book():
    data = request.get_json()
    book_id = data.get('id')
    if not book_id:
        return jsonify({'code': 400, 'message': '缺少图书ID'})
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'message': '图书不存在'})
    
    if data.get('bookName'):
        book.book_name = data['bookName']
    if data.get('author'):
        book.author = data['author']
    if data.get('publisher') is not None:
        book.publisher = data['publisher']
    if data.get('isbn') is not None:
        book.isbn = data['isbn']
    if data.get('category') is not None:
        book.category = data['category']
    if data.get('totalCount'):
        book.total_count = data['totalCount']
    if data.get('availableCount') is not None:
        book.available_count = data['availableCount']
    
    db.session.commit()
    return jsonify({'code': 200, 'message': '修改成功', 'data': book.to_dict()})


# 5. 删除图书
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'message': '图书不存在'})
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'code': 200, 'message': '删除成功'})


# ============================================
# 借阅功能接口
# ============================================

# 6. 借书
@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    book_id = data.get('bookId')
    user_id = data.get('userId')
    
    if not book_id or not user_id:
        return jsonify({'code': 400, 'message': '缺少图书ID或用户ID'})
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'message': '图书不存在'})
    if book.available_count <= 0:
        return jsonify({'code': 400, 'message': '库存不足'})
    
    existing = Borrow.query.filter_by(book_id=book_id, user_id=user_id, status='borrowed').first()
    if existing:
        return jsonify({'code': 400, 'message': '您已借阅这本书，尚未归还'})
    
    borrow = Borrow(
        book_id=book_id,
        user_id=user_id,
        borrow_date=date.today(),
        status='borrowed'
    )
    db.session.add(borrow)
    book.available_count -= 1
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '借书成功'})


# 7. 还书
@app.route('/api/return', methods=['POST'])
def return_book():
    data = request.get_json()
    borrow_id = data.get('borrowId')
    
    if not borrow_id:
        return jsonify({'code': 400, 'message': '缺少借阅记录ID'})
    
    borrow = Borrow.query.get(borrow_id)
    if not borrow:
        return jsonify({'code': 404, 'message': '借阅记录不存在'})
    if borrow.status == 'returned':
        return jsonify({'code': 400, 'message': '这本书已经还过了'})
    
    borrow.status = 'returned'
    borrow.return_date = date.today()
    
    book = Book.query.get(borrow.book_id)
    if book:
        book.available_count += 1
    
    db.session.commit()
    return jsonify({'code': 200, 'message': '还书成功'})


# ============================================
# 启动应用
# ============================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)