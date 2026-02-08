# frontend/streamlit/services/qdrant_service.py

import requests
from typing import List, Dict, Any, Optional

from config.settings import API_BASE


# =====================================================
# INTERNAL
# =====================================================

def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


# =====================================================
# COLLECTIONS
# =====================================================

<<<<<<< HEAD
def list_collections(token: str, qdrant_url: Optional[str] = None):
    params = {}
    if qdrant_url:
        params["qdrant_url"] = qdrant_url
    resp = requests.get(
        f"{API_BASE}/qdrant/collections",
        params=params,
=======
def list_collections(token: str):
    resp = requests.get(
        f"{API_BASE}/qdrant/collections",
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        headers=_headers(token),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["collections"]




def get_collection_detail(
    collection: str,
    token: str,
<<<<<<< HEAD
    qdrant_url: Optional[str] = None,
) -> Dict[str, Any]:
    params = {}
    if qdrant_url:
        params["qdrant_url"] = qdrant_url
    resp = requests.get(
        f"{API_BASE}/qdrant/collections/{collection}",
        params=params,
=======
) -> Dict[str, Any]:
    resp = requests.get(
        f"{API_BASE}/qdrant/collections/{collection}",
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        headers=_headers(token),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


# =====================================================
# POINTS – BROWSE
# =====================================================

def list_points(
    collection: str,
    token: str,
    *,
    limit: int = 50,
    offset: int = 0,
<<<<<<< HEAD
    qdrant_url: Optional[str] = None,
) -> List[Dict[str, Any]]:
    params = {"limit": limit, "offset": offset}
    if qdrant_url:
        params["qdrant_url"] = qdrant_url
    resp = requests.get(
        f"{API_BASE}/qdrant/collections/{collection}/points",
        params=params,
=======
) -> List[Dict[str, Any]]:
    resp = requests.get(
        f"{API_BASE}/qdrant/collections/{collection}/points",
        params={
            "limit": limit,
            "offset": offset,
        },
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        headers=_headers(token),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["points"]


# =====================================================
# POINTS – FILTER
# =====================================================

def filter_points(
    collection: str,
    token: str,
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
    payload = {
        "file_hash": file_hash,
        "section_id": section_id,
        "chunk_id": chunk_id,
        "limit": limit,
    }
<<<<<<< HEAD
    if qdrant_url:
        payload["qdrant_url"] = qdrant_url
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

    resp = requests.post(
        f"{API_BASE}/qdrant/collections/{collection}/filter",
        json=payload,
        headers=_headers(token),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["points"]
