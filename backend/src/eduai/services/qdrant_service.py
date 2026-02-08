from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

<<<<<<< HEAD
from eduai.core.config import get_qdrant_url, QDRANT_API_KEY


# =====================================================
# CLIENT (singleton khi không override url)
=======
from eduai.core.config import QDRANT_URL, QDRANT_API_KEY


# =====================================================
# CLIENT (singleton-ish)
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
# =====================================================

_client: Optional[QdrantClient] = None


<<<<<<< HEAD
def get_client(qdrant_url: Optional[str] = None) -> QdrantClient:
    """Client Qdrant. Nếu qdrant_url truyền vào thì dùng URL đó (không cache); không thì dùng mặc định từ env."""
    global _client
    if qdrant_url and (s := qdrant_url.strip()):
        url = s if s.startswith("http://") or s.startswith("https://") else f"http://{s}"
        return QdrantClient(url=url, api_key=QDRANT_API_KEY)
    if _client is None:
        _client = QdrantClient(
            url=get_qdrant_url(None),
=======
def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(
            url=QDRANT_URL,
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
            api_key=QDRANT_API_KEY,
        )
    return _client


# =====================================================
# COLLECTIONS
# =====================================================

<<<<<<< HEAD
def list_collections(qdrant_url: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Danh sách collections trong Qdrant
    """
    client = get_client(qdrant_url)
=======
def list_collections() -> List[Dict[str, Any]]:
    """
    Danh sách collections trong Qdrant
    """
    client = get_client()
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    resp = client.get_collections()

    return [
        {
            "name": c.name,
        }
        for c in resp.collections
    ]


<<<<<<< HEAD
def _infer_payload_schema(client: QdrantClient, collection: str, sample_size: int = 200) -> Dict[str, str]:
    """
    Suy luận schema payload từ mẫu points (key -> kiểu: string, integer, number, boolean, array, object).
    """
    schema: Dict[str, str] = {}
    try:
        points, _ = client.scroll(
            collection_name=collection,
            limit=sample_size,
            with_payload=True,
            with_vectors=False,
        )
    except Exception:
        return {}

    def type_name(v: Any) -> str:
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "boolean"
        if isinstance(v, int):
            return "integer"
        if isinstance(v, float):
            return "number"
        if isinstance(v, str):
            return "string"
        if isinstance(v, list):
            return "array"
        if isinstance(v, dict):
            return "object"
        return "string"

    for p in points:
        payload = p.payload or {}
        for key, val in payload.items():
            t = type_name(val)
            if key not in schema:
                schema[key] = t
            elif schema[key] != t:
                # Nhiều kiểu khác nhau → dùng union hoặc "string" an toàn
                schema[key] = "string"
    return schema


def get_collection_detail(name: str, qdrant_url: Optional[str] = None) -> Dict[str, Any]:
    client = get_client(qdrant_url)
=======
def get_collection_detail(name: str) -> Dict[str, Any]:
    client = get_client()
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    info = client.get_collection(name)

    vectors = {}
    params = info.config.params.vectors

    # Trường hợp 1: single vector
    if hasattr(params, "size"):
        vectors = {
            "default": {
                "size": params.size,
                "distance": str(params.distance),
            }
        }

    # Trường hợp 2: named vectors
    elif isinstance(params, dict):
        for k, v in params.items():
            vectors[k] = {
                "size": v.size,
                "distance": str(v.distance),
            }

<<<<<<< HEAD
    payload_schema = _infer_payload_schema(client, name) if info.points_count else {}

=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    return {
        "name": name,
        "status": info.status,
        "vectors": vectors,   # ✅ JSON-safe
        "points_count": info.points_count,
        "indexed_vectors_count": info.indexed_vectors_count,
        "segments_count": info.segments_count,
<<<<<<< HEAD
        "payload_schema": payload_schema,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    }




# =====================================================
# POINTS – BROWSE
# =====================================================

def list_points(
    collection: str,
    *,
    limit: int = 50,
    offset: int = 0,
<<<<<<< HEAD
    qdrant_url: Optional[str] = None,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
) -> List[Dict[str, Any]]:
    """
    Duyệt points theo offset/limit (debug, inspector)
    """
<<<<<<< HEAD
    client = get_client(qdrant_url)
=======
    client = get_client()
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

    points, _ = client.scroll(
        collection_name=collection,
        limit=limit,
        offset=offset,
        with_payload=True,
        with_vectors=False,  # inspector: không cần vector
    )

    return [_serialize_point(p) for p in points]


# =====================================================
# POINTS – FILTER
# =====================================================

def filter_points(
    collection: str,
    *,
    file_hash: Optional[str] = None,
    section_id: Optional[str] = None,
    chunk_id: Optional[int] = None,
    limit: int = 50,
<<<<<<< HEAD
    qdrant_url: Optional[str] = None,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
) -> List[Dict[str, Any]]:
    """
    Filter points theo metadata payload
    """
    must: List[qmodels.FieldCondition] = []

    if file_hash:
        must.append(
            qmodels.FieldCondition(
                key="file_hash",
                match=qmodels.MatchValue(value=file_hash),
            )
        )

    if section_id:
        must.append(
            qmodels.FieldCondition(
                key="section_id",
                match=qmodels.MatchValue(value=section_id),
            )
        )

    if chunk_id is not None:
        must.append(
            qmodels.FieldCondition(
                key="chunk_id",
                match=qmodels.MatchValue(value=chunk_id),
            )
        )

    flt = qmodels.Filter(must=must) if must else None

<<<<<<< HEAD
    client = get_client(qdrant_url)
=======
    client = get_client()
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

    points, _ = client.scroll(
        collection_name=collection,
        scroll_filter=flt,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    return [_serialize_point(p) for p in points]


# =====================================================
# INTERNAL
# =====================================================

def _serialize_point(p) -> Dict[str, Any]:
    """
    Chuẩn hoá point để trả về API / UI
    """
    return {
        "id": p.id,
        "score": getattr(p, "score", None),
        "payload": p.payload or {},
    }
