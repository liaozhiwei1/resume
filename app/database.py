from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./resume_app.db"

engine = create_engine(
DATABASE_URL,
connect_args={"check_same_thread": False}, # 只对 SQLite 必需
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI 依赖注入使用的数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()