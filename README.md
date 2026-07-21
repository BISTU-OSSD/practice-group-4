# 图书管理系统

> 课程实践项目：开源软件开发

## 项目简介

本项目是一个基于 **Flask + MySQL** 的图书管理系统，提供图书信息的增删改查以及借书、还书功能。后端提供 RESTful API 接口，前端可通过 Vue 或 Postman 进行调用。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Flask (Python) |
| 数据库 | MySQL 8.0 |
| ORM | Flask-SQLAlchemy |
| 接口测试 | Postman |
| 版本控制 | Git + GitHub |

## 快速运行

### 1. 克隆项目
```bash
git clone https://github.com/promising-gif/OSSDT.git
cd OSSDT
```

### 2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置数据库
- 修改 `config.py` 中的数据库密码
- 在 MySQL 中执行 `schema.sql` 和 `data.sql`

### 5. 启动项目
```bash
python app.py
```

启动后访问：`http://localhost:5000/api/books`

## 接口列表

| 功能 | 方法 | URL |
|------|------|-----|
| 查询所有图书 | GET | `/api/books` |
| 添加图书 | POST | `/api/books` |
| 修改图书 | PUT | `/api/books` |
| 删除图书 | DELETE | `/api/books/<id>` |
| 借书 | POST | `/api/borrow` |
| 还书 | POST | `/api/return` |

详细接口文档见 `接口文档.docx`

## 团队成员

- 组长：[姓名] - 项目协调与版本集成
- 前端：[姓名] - 页面开发
- 后端：[姓名] - 接口开发
- 管家：[姓名] - 仓库管理
- 秘书：[姓名] - 文档编写

## 许可证

MIT License