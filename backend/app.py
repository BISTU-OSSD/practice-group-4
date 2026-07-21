# app.py（最终完整版）
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# 注册所有API蓝图
from book_api import book_bp
from borrow_api import borrow_bp
app.register_blueprint(book_bp)
app.register_blueprint(borrow_bp)

@app.route('/')
def hello():
    return '图书管理系统后端已启动！'

# 创建表并初始化测试数据
with app.app_context():
    db.create_all()
    
    from models import User
    if User.query.count() == 0:
        users = [
            User(name='张三', student_id='2024001'),
            User(name='李四', student_id='2024002'),
            User(name='王五', student_id='2024003'),
        ]
        db.session.add_all(users)
        db.session.commit()
        print('✅ 测试用户创建成功')
    
    print('✅ 所有表创建完成，服务已就绪！')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)