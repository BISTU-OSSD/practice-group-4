# 图书管理系统 (Library Management System)

一个基于 **Flask + Vue 2 + MySQL** 的前后端分离图书管理项目，提供图书增删改查、借阅归还及记录查询功能。

## 📚 项目架构
- **后端**：Python 3.8+ / Flask / SQLAlchemy / PyMySQL
- **前端**：Vue 2 / Element UI / Axios
- **数据库**：MySQL 5.7+

## 🚀 快速开始

### 1. 环境准备
- 安装 Python 3.8+
- 安装 Node.js 14+ 和 npm
- 安装并启动 MySQL 数据库

### 2. 初始化数据库
1. 打开 MySQL 客户端（如 Navicat 或命令行）。
2. 执行 `schema.sql` 文件中的 SQL 语句，创建数据库 `library_db` 及相关表结构。

### 3. 启动后端
```bash
# 1. 进入项目根目录
cd library-system

# 2. 创建并激活虚拟环境 (Windows)
python -m venv venv
venv\Scripts\activate

# 3. 安装后端依赖
pip install -r requirements.txt

# 4. 修改数据库配置
# 打开 config.py，将 SQLALCHEMY_DATABASE_URI 中的密码改成你本地 MySQL 的 root 密码

# 5. 运行 Flask 后端
python app.py
