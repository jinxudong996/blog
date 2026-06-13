from fastapi import APIRouter, HTTPException

# 兼容包内外运行：优先相对导入，失败时回退到绝对导入

from database.mysql import fetch_all_students, fetch_student_by_id

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", summary="查询所有学生信息")
async def list_students():
    try:
        rows = await fetch_all_students()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e}")


@router.get("/{student_id}", summary="根据学号查询学生信息")
async def get_student(student_id: str):
    try:
        row = await fetch_student_by_id(student_id)
        if not row:
            raise HTTPException(status_code=404, detail="未找到该学生")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e}")