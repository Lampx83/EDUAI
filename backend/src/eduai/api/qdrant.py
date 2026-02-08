# backend/src/eduai/api/qdrant.py

from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from eduai.core.auth import verify_token
from eduai.services.qdrant_service import (
    list_collections,
    get_collection_detail,
    list_points,
    filter_points,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    prefix="/qdrant",
    tags=["Qdrant"],
)

# =====================================================
# SCHEMAS
# =====================================================

class QdrantFilterRequest(BaseModel):
    file_hash: Optional[str] = Field(
        default=None,
        description="Hash của file gốc",
    )
    section_id: Optional[str] = Field(
        default=None,
        description="ID của section",
    )
    chunk_id: Optional[int] = Field(
        default=None,
        ge=0,
        description="ID của chunk",
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Số lượng point trả về",
    )
<<<<<<< HEAD
    qdrant_url: Optional[str] = Field(
        default=None,
        description="URL Qdrant Service (trống = mặc định theo env)",
    )
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56


# =====================================================
# ENDPOINTS
# =====================================================

@router.get("/collections")
def api_list_collections(
<<<<<<< HEAD
    qdrant_url: Optional[str] = Query(None, description="URL Qdrant Service (trống = mặc định)"),
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    user=Depends(verify_token),
):
    """
    Danh sách collections trong Qdrant
    (dùng cho Qdrant Inspector – read-only)
    """
    return {
<<<<<<< HEAD
        "collections": list_collections(qdrant_url=qdrant_url)
=======
        "collections": list_collections()
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    }


@router.get("/collections/{name}")
def api_get_collection_detail(
    name: str,
<<<<<<< HEAD
    qdrant_url: Optional[str] = Query(None, description="URL Qdrant Service (trống = mặc định)"),
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    user=Depends(verify_token),
):
    """
    Thông tin chi tiết của một collection
    """
<<<<<<< HEAD
    return get_collection_detail(name, qdrant_url=qdrant_url)
=======
    return get_collection_detail(name)
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56


@router.get("/collections/{name}/points")
def api_list_points(
    name: str,
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Số point mỗi lần load",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Offset cho scroll",
    ),
<<<<<<< HEAD
    qdrant_url: Optional[str] = Query(None, description="URL Qdrant Service (trống = mặc định)"),
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    user=Depends(verify_token),
):
    """
    Duyệt points theo dạng scroll (read-only)
    """
    return {
        "points": list_points(
            collection=name,
            limit=limit,
            offset=offset,
<<<<<<< HEAD
            qdrant_url=qdrant_url,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        )
    }


@router.post("/collections/{name}/filter")
def api_filter_points(
    name: str,
    req: QdrantFilterRequest,
    user=Depends(verify_token),
):
    """
    Filter points theo payload metadata
    """
    return {
        "points": filter_points(
            collection=name,
            file_hash=req.file_hash,
            section_id=req.section_id,
            chunk_id=req.chunk_id,
            limit=req.limit,
<<<<<<< HEAD
            qdrant_url=req.qdrant_url,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        )
    }
