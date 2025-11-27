"""
迁移脚本：更新 users 表的 password_hash 字段长度
"""
from sqlalchemy import text
from database import engine

def migrate_user_password_hash():
    """检查并更新 password_hash 字段长度"""
    with engine.begin() as conn:
        # SQLite 不支持直接修改列类型，需要重建表
        # 但为了安全，我们只检查字段是否存在
        result = conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result]
        
        if 'password_hash' in columns:
            print("password_hash 字段已存在")
            # SQLite 中 String 类型没有长度限制，所以不需要迁移
            # 但如果将来迁移到其他数据库，需要确保字段长度足够
            print("注意：SQLite 中 String 类型没有长度限制")
            print("bcrypt 哈希通常是 60 字符，当前字段可以存储")
        else:
            print("password_hash 字段不存在，需要创建表")

if __name__ == "__main__":
    migrate_user_password_hash()

