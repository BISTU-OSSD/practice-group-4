# borrow_api.py - 借阅管理模块（C完整代码）
from flask import Blueprint, request, jsonify
from models import db, BorrowRecord, User
from book_api import get_book_by_id, update_book_status

borrow_bp = Blueprint('borrow', __name__, url_prefix='/api/borrows')

# ====== 1. 借书 ======
@borrow_bp.route('/', methods=['POST'])
def borrow_book():
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    
    # 参数校验
    if not book_id or not user_id:
        return jsonify({'code': 400, 'message': 'book_id和user_id不能为空'})
    
    # 检查图书是否存在
    book = get_book_by_id(book_id)
    if not book:
        return jsonify({'code': 404, 'message': '图书不存在'})
    
    # 检查图书是否已被借出
    if book.status == 0:
        return jsonify({'code': 400, 'message': '这本书已被借出'})
    
    # 检查用户是否存在
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'})
    
    # 检查该用户是否已经借了这本书（同一本书不能重复借）
    existing = BorrowRecord.query.filter_by(book_id=book_id, user_id=user_id, status=1).first()
    if existing:
        return jsonify({'code': 400, 'message': '您已借了这本书，请先归还'})
    
    # 创建借阅记录
    record = BorrowRecord(
        book_id=book_id,
        user_id=user_id
    )
    db.session.add(record)
    
    # 更新图书状态为已借出
    update_book_status(book_id, 0)
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'data': record.to_dict(),
        'message': '借书成功'
    })

# ====== 2. 还书 ======
@borrow_bp.route('/return', methods=['PUT'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')  # 可选：指定还书人
    
    if not book_id:
        return jsonify({'code': 400, 'message': 'book_id不能为空'})
    
    # 查找借阅记录
    query = BorrowRecord.query.filter_by(book_id=book_id, status=1)
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    record = query.first()
    if not record:
        return jsonify({'code': 400, 'message': '未找到借阅记录，可能已归还'})
    
    # 更新记录
    from datetime import datetime
    record.return_time = datetime.now()
    record.status = 0
    
    # 更新图书状态为在库
    update_book_status(book_id, 1)
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'data': record.to_dict(),
        'message': '还书成功'
    })

# ====== 3. 查询某本书的借阅历史 ======
@borrow_bp.route('/book/<int:book_id>', methods=['GET'])
def get_book_borrow_history(book_id):
    records = BorrowRecord.query.filter_by(book_id=book_id).order_by(BorrowRecord.borrow_time.desc()).all()
    return jsonify({
        'code': 200,
        'data': [r.to_dict() for r in records],
        'message': '查询成功'
    })

# ====== 4. 查询某个用户的借阅记录 ======
@borrow_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_borrow_records(user_id):
    records = BorrowRecord.query.filter_by(user_id=user_id).order_by(BorrowRecord.borrow_time.desc()).all()
    return jsonify({
        'code': 200,
        'data': [r.to_dict() for r in records],
        'message': '查询成功'
    })