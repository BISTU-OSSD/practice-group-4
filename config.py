import os

class Config:
    # 数据库连接配置（把密码改成你自己的）
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:JQy081507@localhost:3306/library_db?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 解决中文乱码
    JSON_AS_ASCII = False