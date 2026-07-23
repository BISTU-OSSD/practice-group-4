-- 创建数据库
CREATE DATABASE IF NOT EXISTS library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE library_db;

-- 图书表
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '图书ID',
    book_name VARCHAR(100) NOT NULL COMMENT '书名',
    author VARCHAR(50) NOT NULL COMMENT '作者',
    publisher VARCHAR(100) COMMENT '出版社',
    isbn VARCHAR(20) UNIQUE COMMENT 'ISBN号',
    category VARCHAR(50) COMMENT '分类',
    total_count INT DEFAULT 1 COMMENT '总数量',
    available_count INT DEFAULT 1 COMMENT '可借数量',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
);

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password VARCHAR(100) NOT NULL COMMENT '密码',
    real_name VARCHAR(50) COMMENT '真实姓名',
    phone VARCHAR(20) COMMENT '手机号',
    role VARCHAR(20) DEFAULT 'user' COMMENT '角色：admin/user',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 借阅记录表
CREATE TABLE borrows (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    book_id INT NOT NULL COMMENT '图书ID',
    user_id INT NOT NULL COMMENT '用户ID',
    borrow_date DATE NOT NULL COMMENT '借书日期',
    return_date DATE COMMENT '还书日期',
    status VARCHAR(20) DEFAULT 'borrowed' COMMENT '状态：borrowed/returned',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);