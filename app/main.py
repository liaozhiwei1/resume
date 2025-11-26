import os
import sys
import uuid
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 设置标准输出编码为 UTF-8，避免 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from database import Base, engine, get_db
from models import Candidate
from parser import parse_resume_file, parse_resume_text_cn, extract_docx_to_html

Base.metadata.create_all(bind=engine)

# 执行数据库迁移（添加 tags 字段）
try:
    from migrate import migrate_add_tags_field
    migrate_add_tags_field()
except Exception as e:
    print(f"数据库迁移警告: {e}")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="简历解析后端",
    description="上传 PDF/DOCX 简历，自动解析候选人信息并入库。",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vue 开发服务器端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return JSONResponse({"message": "服务运行中。访问 /docs 查看接口文档。"})


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/preview", summary="预览简历解析结果（不保存）")
async def preview_resume(
        file: UploadFile = File(...),
):
    """上传文件并解析，但不保存到数据库，仅返回解析结果用于预览"""
    filename_lower = file.filename.lower()
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
        raise HTTPException(status_code=400, detail="只支持 PDF 或 DOCX 文件")
    
    # 检查文件大小
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"文件大小不能超过 {MAX_FILE_SIZE / 1024 / 1024}MB")
    
    ext = ".pdf" if filename_lower.endswith(".pdf") else ".docx"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)

    # 临时保存文件用于解析
    try:
        with open(save_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {e}")

    # 解析
    try:
        parsed = parse_resume_file(save_path)
    except Exception as e:
        # 删除临时文件
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
        except:
            pass
        # 安全处理异常消息
        error_msg = str(e)
        try:
            error_msg = error_msg.encode('utf-8', errors='replace').decode('utf-8')
        except:
            error_msg = "解析简历时发生错误"
        raise HTTPException(status_code=500, detail=f"解析简历失败: {error_msg}")

    # 安全处理文件名
    safe_filename = file.filename
    try:
        safe_filename = safe_filename.encode('utf-8', errors='replace').decode('utf-8')
    except:
        safe_filename = "unknown_file"
    
    # 返回预览结果（包含临时文件信息，用于后续保存）
    return {
        "parsed": {
            "name": parsed.get("name"),
            "email": parsed.get("email"),
            "phone": parsed.get("phone"),
            "university": parsed.get("university"),
            "degree": parsed.get("degree"),
            "major": parsed.get("major"),
        },
        "file_info": {
            "stored_name": unique_name,
            "original_name": safe_filename,
            "temp_path": save_path,  # 临时文件路径，保存时需要
        }
    }


@app.post("/save", summary="保存已解析的候选人信息")
async def save_candidate(
        parsed_data: dict = Body(...),
        db: Session = Depends(get_db),
):
    """保存预览后的候选人信息"""
    try:
        parsed = parsed_data.get("parsed", {})
        file_info = parsed_data.get("file_info", {})
        
        if not file_info.get("temp_path") or not os.path.exists(file_info["temp_path"]):
            raise HTTPException(status_code=400, detail="文件已过期，请重新上传")
        
        candidate = Candidate(
            name=parsed.get("name"),
            email=parsed.get("email"),
            phone=parsed.get("phone"),
            university=parsed.get("university"),
            degree=parsed.get("degree"),
            major=parsed.get("major"),
            resume_filename=file_info.get("stored_name"),
            resume_original_name=file_info.get("original_name"),
            resume_path=file_info.get("temp_path"),
        )
        print(candidate.resume_path)
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "university": candidate.university,
            "degree": candidate.degree,
            "major": candidate.major,
            "tags": candidate.tags or "",
            "created_at": candidate.created_at,
        }
    except Exception as e:
        db.rollback()
        error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
        raise HTTPException(status_code=500, detail=f"保存失败: {error_msg}")


@app.post("/upload", summary="上传简历（PDF/DOCX）并解析")
async def upload_resume(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    filename_lower = file.filename.lower()
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
        raise HTTPException(status_code=400, detail="只支持 PDF 或 DOCX 文件")
    
    # 检查文件大小
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"文件大小不能超过 {MAX_FILE_SIZE / 1024 / 1024}MB")
    
    ext = ".pdf" if filename_lower.endswith(".pdf") else ".docx"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)

    # 保存文件
    try:
        with open(save_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {e}")

    # 解析
    try:
        parsed = parse_resume_file(save_path)
    except Exception as e:
        # 安全处理异常消息，避免编码问题
        error_msg = str(e)
        try:
            # 尝试编码为 UTF-8，如果失败则使用错误替换
            error_msg = error_msg.encode('utf-8', errors='replace').decode('utf-8')
        except:
            error_msg = "解析简历时发生错误"
        raise HTTPException(status_code=500, detail=f"解析简历失败: {error_msg}")

    # 安全处理文件名，避免特殊字符导致的编码问题
    safe_filename = file.filename
    try:
        # 确保文件名可以安全编码
        safe_filename = safe_filename.encode('utf-8', errors='replace').decode('utf-8')
    except:
        safe_filename = "unknown_file"
    
    candidate = Candidate(
        name=parsed.get("name"),
        email=parsed.get("email"),
        phone=parsed.get("phone"),
        university=parsed.get("university"),
        degree=parsed.get("degree"),
        major=parsed.get("major"),
        resume_filename=unique_name,
        resume_original_name=safe_filename,
        resume_path=save_path,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "university": candidate.university,
        "degree": candidate.degree,
        "major": candidate.major,
        "resume_file": {
            "stored_name": candidate.resume_filename,
            "original_name": candidate.resume_original_name,
        },
        "created_at": candidate.created_at,
    }


@app.post("/upload-text", summary="上传简历纯文本并解析（爬虫/接口用）")
def upload_resume_text(
        text: str = Body(..., embed=True, description="简历的纯文本内容"),
        db: Session = Depends(get_db),
):
    try:
        parsed = parse_resume_text_cn(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析简历文本失败: {e}")
    candidate = Candidate(
        name=parsed.get("name"),
        email=parsed.get("email"),
        phone=parsed.get("phone"),
        university=parsed.get("university"),
        degree=parsed.get("degree"),
        major=parsed.get("major"),
        resume_filename="(from_text)",
        resume_original_name="(from_text)",
        resume_path="(from_text)",
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "university": candidate.university,
        "degree": candidate.degree,
        "major": candidate.major,
        "created_at": candidate.created_at,
    }


@app.get("/candidates/{candidate_id}/resume/download", summary="下载简历文件")
def download_resume(candidate_id: int, db: Session = Depends(get_db)):
    """下载候选人的原始简历文件"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    if not os.path.exists(candidate.resume_path):
        raise HTTPException(status_code=404, detail="简历文件不存在")
    
    # 使用原始文件名作为下载文件名
    return FileResponse(
        path=candidate.resume_path,
        filename=candidate.resume_original_name,
        media_type="application/octet-stream"
    )


@app.get("/candidates/{candidate_id}/resume/preview", summary="预览简历文件")
def preview_resume_file(candidate_id: int, db: Session = Depends(get_db)):
    """预览候选人的原始简历文件（PDF可直接预览，DOCX返回HTML）"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    print(candidate)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    if not os.path.exists(candidate.resume_path):
        raise HTTPException(status_code=404, detail="简历文件不存在")
    
    file_ext = os.path.splitext(candidate.resume_path)[1].lower()
    
    # PDF 文件可以直接在浏览器中预览
    if file_ext == ".pdf":
        return FileResponse(
            path=candidate.resume_path,
            filename=candidate.resume_original_name,
            media_type="application/pdf"
        )
    # DOCX 文件转换为 HTML 预览
    elif file_ext == ".docx":
        try:
            html_content = extract_docx_to_html(candidate.resume_path)
            return JSONResponse({
                "type": "html",
                "content": html_content,
                "filename": candidate.resume_original_name
            })
        except Exception as e:
            error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
            raise HTTPException(status_code=500, detail=f"DOCX 预览失败: {error_msg}")
    else:
        raise HTTPException(status_code=400, detail="不支持的文件格式")


@app.get("/candidates/{candidate_id}/resume/preview-html", summary="获取DOCX文件的HTML预览")
def get_docx_html_preview(candidate_id: int, db: Session = Depends(get_db)):
    """获取DOCX文件的HTML格式预览内容"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    print(candidate)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    if not os.path.exists(candidate.resume_path):
        raise HTTPException(status_code=404, detail="简历文件不存在")
    
    file_ext = os.path.splitext(candidate.resume_path)[1].lower()
    if file_ext != ".docx":
        raise HTTPException(status_code=400, detail="此接口仅支持 DOCX 文件")
    
    try:
        html_content = extract_docx_to_html(candidate.resume_path)
        return JSONResponse({
            "type": "html",
            "content": html_content,
            "filename": candidate.resume_original_name
        })
    except Exception as e:
        error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
        raise HTTPException(status_code=500, detail=f"DOCX 预览失败: {error_msg}")


@app.get("/candidates", summary="获取候选人列表")
def list_candidates(
    tag: str = None,
    db: Session = Depends(get_db)
):
    """获取候选人列表，支持按标签筛选"""
    query = db.query(Candidate)
    
    # 如果提供了标签参数，进行筛选
    if tag and tag.strip():
        tag_filter = f"%{tag.strip()}%"
        query = query.filter(Candidate.tags.like(tag_filter))
    
    candidates: List[Candidate] = query.order_by(Candidate.id.desc()).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "university": c.university,
            "degree": c.degree,
            "major": c.major,
            "tags": c.tags or "",
            "resume_original_name": c.resume_original_name,
            "created_at": c.created_at,
        }
        for c in candidates
    ]


@app.put("/candidates/{candidate_id}/tags", summary="更新候选人标签")
def update_candidate_tags(
    candidate_id: int,
    tags: str = Body(..., embed=True, description="标签字符串，多个标签用逗号分隔"),
    db: Session = Depends(get_db),
):
    """更新候选人的标签"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    # 清理标签：去除空格，去重
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    candidate.tags = ",".join(tag_list)
    
    db.commit()
    db.refresh(candidate)
    
    return {
        "id": candidate.id,
        "tags": candidate.tags or "",
    }


@app.get("/tags", summary="获取所有标签列表")
def get_all_tags(db: Session = Depends(get_db)):
    """获取所有候选人的标签列表（去重）"""
    candidates = db.query(Candidate).filter(Candidate.tags.isnot(None), Candidate.tags != "").all()
    all_tags = set()
    for candidate in candidates:
        if candidate.tags:
            tags = [t.strip() for t in candidate.tags.split(",") if t.strip()]
            all_tags.update(tags)
    return sorted(list(all_tags))


@app.delete("/candidates/{candidate_id}", summary="删除候选人")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """删除候选人及其关联的简历文件"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    # 删除关联的简历文件（如果存在）
    resume_path = candidate.resume_path
    if resume_path and os.path.exists(resume_path):
        try:
            # 排除特殊标记路径（如 "(from_text)"）
            if not resume_path.startswith("(") and not resume_path.endswith(")"):
                os.remove(resume_path)
                print(f"已删除简历文件: {resume_path}")
        except Exception as e:
            # 文件删除失败不影响数据库删除，只记录警告
            print(f"删除简历文件失败: {e}")
    
    # 删除数据库记录
    try:
        db.delete(candidate)
        db.commit()
        return {
            "message": "候选人删除成功",
            "id": candidate_id
        }
    except Exception as e:
        db.rollback()
        error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
        raise HTTPException(status_code=500, detail=f"删除失败: {error_msg}")