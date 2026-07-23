# 图书管理系统 - 后端

## 技术栈
- Python 3.8+
- Flask
- MySQL

## 快速运行
1. 创建虚拟环境：`python -m venv venv`
2. 激活：`venv\Scripts\activate`
3. 安装依赖：`pip install -r requirements.txt`
4. 修改 config.py 里的数据库密码
5. 运行：`python app.py`

## 接口文档
见 `接口文档.docx`

## 接口列表
- GET /api/books - 查询所有图书
- POST /api/books - 添加图书
- PUT /api/books - 修改图书
- DELETE /api/books/<id> - 删除图书
- POST /api/borrow - 借书
- POST /api/return - 还书