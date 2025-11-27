"""
数据库迁移：添加 notes（备注）字段
"""
from sqlalchemy import text
from database import engine

def migrate_add_notes_field():
    """
    为 candidates 表添加 notes 字段
    """
    with engine.begin() as conn:  # 使用 begin() 自动管理事务
        # 检查字段是否已存在
        result = conn.execute(text("PRAGMA table_info(candidates)"))
        columns = [row[1] for row in result]
        
        if 'notes' not in columns:
            print("正在添加 notes 字段...")
            conn.execute(text("ALTER TABLE candidates ADD COLUMN notes TEXT DEFAULT ''"))
            # begin() 上下文管理器会自动提交，无需手动 commit
            print("notes 字段添加成功！")
        else:
            print("notes 字段已存在，无需迁移")

if __name__ == "__main__":
    migrate_add_notes_field()

