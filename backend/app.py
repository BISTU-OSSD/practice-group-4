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
    print("后端收到的数据:", data)
    
    if not data.get('name') or not data.get('author'):
        return jsonify({'code': 400, 'message': '书名和作者不能为空'})

    book = Book(
        book_name=data['name'],
        author=data['author'],
        publisher=data.get('publisher', ''),
        isbn=data.get('isbn', ''),
        category=data.get('category', ''),
        total_count=data.get('total_count', 1),
        available_count=data.get('available_count', 1)
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({'code': 200, 'message': '添加成功', 'data': book.to_dict()})


# 4. 修改图书
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    print("后端收到的编辑数据:", data)

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'message': '图书不存在'})

    # 前端用 name，后端用 book_name
    if data.get('name'):
        book.book_name = data['name']
    if data.get('author'):
        book.author = data['author']
    if data.get('isbn') is not None:
        book.isbn = data['isbn']
    # 处理状态：前端传 status，转成 available_count
    if data.get('status') is not None:
        # status=1 表示在库，available_count=1；status=0 表示已借出，available_count=0
        book.available_count = 1 if data['status'] == 1 else 0

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
@app.route('/api/borrows', methods=['POST'])
def borrow_book():
    data = request.get_json()
    print("借书收到的数据:", data)
    book_id = data.get('book_id')
    user_id = data.get('user_id')

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
@app.route('/api/borrows/return', methods=['PUT'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({'code': 400, 'message': '缺少图书ID'})

    borrow = Borrow.query.filter_by(book_id=book_id, status='borrowed').first()
    if not borrow:
        return jsonify({'code': 404, 'message': '借阅记录不存在'})

    borrow.status = 'returned'
    borrow.return_date = date.today()

    book = Book.query.get(book_id)
    if book:
        book.available_count += 1

    db.session.commit()
    return jsonify({'code': 200, 'message': '还书成功'})


# 8. 查询用户借阅记录
@app.route('/api/borrows/user/<int:user_id>', methods=['GET'])
def get_user_borrows(user_id):
    borrows = Borrow.query.filter_by(user_id=user_id).order_by(Borrow.borrow_date.desc()).all()
    print("借阅历史返回的数据:", [b.to_dict() for b in borrows])
    return jsonify({
        'code': 200,
        'data': [b.to_dict() for b in borrows]
    })


# 9. 查询图书借阅历史
@app.route('/api/borrows/book/<int:book_id>', methods=['GET'])
def get_book_borrows(book_id):
    borrows = Borrow.query.filter_by(book_id=book_id).order_by(Borrow.borrow_date.desc()).all()
    print("借阅历史返回的数据:", [b.to_dict() for b in borrows])
    return jsonify({
        'code': 200,
        'data': [b.to_dict() for b in borrows]
    })


# ============================================
# 启动应用
# ============================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)