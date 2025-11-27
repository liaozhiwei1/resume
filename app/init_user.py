"""
初始化用户脚本
运行: python init_user.py
"""
import sys
from database import SessionLocal
from models import User
from auth import get_password_hash

def init_user():
    """创建默认管理员用户"""
    db = SessionLocal()
    try:
        # 检查是否已存在用户
        existing_user = db.query(User).first()
        if existing_user:
            print("用户已存在，跳过初始化")
            return
        
        # 创建默认用户
        default_username = "admin"
        default_password = "admin123"  # 生产环境请修改
        
        hashed_password = get_password_hash(default_password)
        new_user = User(
            username=default_username,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()
        print(f"✅ 默认用户创建成功！")
        print(f"   用户名: {default_username}")
        print(f"   密码: {default_password}")
        print(f"   ⚠️  请在生产环境中修改默认密码！")
    except Exception as e:
        db.rollback()
        print(f"❌ 创建用户失败: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    init_user()

