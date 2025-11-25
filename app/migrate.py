"""
数据库迁移脚本：添加 tags 字段
"""
from sqlalchemy import text
from database import engine

def migrate_add_tags_field():
    """检查并添加 tags 字段"""
    with engine.connect() as conn:
        # 检查字段是否已存在
        result = conn.execute(text("PRAGMA table_info(candidates)"))
        columns = [row[1] for row in result]
        
        if 'tags' not in columns:
            print("正在添加 tags 字段...")
            conn.execute(text("ALTER TABLE candidates ADD COLUMN tags TEXT"))
            conn.commit()
            print("tags 字段添加成功！")
        else:
            print("tags 字段已存在，无需迁移")

if __name__ == "__main__":
    migrate_add_tags_field()

