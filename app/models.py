from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, nullable=True)
    university = Column(String, index=True, nullable=True)
    degree = Column(String, nullable=True)
    major = Column(String, nullable=True)

    # 文件相关
    resume_filename = Column(String, nullable=False)  # 存在服务器上的文件名
    resume_original_name = Column(String, nullable=False)  # 原始上传文件名
    resume_path = Column(String, nullable=False)  # 文件路径

    # 标签（逗号分隔的字符串，如："前端,React,3年经验"）
    tags = Column(String, nullable=True, default="")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
