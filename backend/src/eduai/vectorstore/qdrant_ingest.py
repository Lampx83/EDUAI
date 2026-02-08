from pathlib import Path
<<<<<<< HEAD
from typing import List, Dict, Any, Optional
import tempfile
=======
from typing import List, Dict, Any
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
import uuid

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)

from eduai.common.jsonio import read_json
<<<<<<< HEAD
from eduai.common.nas_io import (
    nas_safe_copy,
    nas_safe_find_processed_dir,
)
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
from eduai.vectorstore.constants import COLLECTION_NAME


# =====================================================
# COLLECTION MANAGEMENT
# =====================================================

def ensure_collection(
    client: QdrantClient,
    vector_dim: int,
<<<<<<< HEAD
    collection_name: Optional[str] = None,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
) -> None:
    """
    Ensure Qdrant collection exists.
    If already exists → do nothing.
<<<<<<< HEAD
    collection_name: tên collection; None = dùng COLLECTION_NAME mặc định.
    """
    name = (collection_name or "").strip() or COLLECTION_NAME

    collections = client.get_collections().collections
    if any(c.name == name for c in collections):
        return

    client.create_collection(
        collection_name=name,
=======
    """

    collections = client.get_collections().collections
    if any(c.name == COLLECTION_NAME for c in collections):
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        vectors_config=VectorParams(
            size=vector_dim,
            distance=Distance.COSINE,
        ),
    )


# =====================================================
# INGEST EMBEDDINGS (FINAL, CORRECT VERSION)
# =====================================================

def ingest_file_embeddings(
    client: QdrantClient,
    file_hash: str,
    embeddings_dir: Path,
    processed_root: Path,
<<<<<<< HEAD
    collection_name: Optional[str] = None,
    parent_dir: Optional[str] = None,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
) -> int:
    """
    Ingest embeddings of one file into Qdrant.

<<<<<<< HEAD
    parent_dir: tên domain (thư mục cha trong 400_embeddings); nếu có thì tránh iterdir trên NAS.
    collection_name: tên collection; None = dùng COLLECTION_NAME mặc định.

    Source of truth:
    - Vectors + meta: 400_embeddings/<domain>/<file_hash> hoặc 400_embeddings/<file_hash>
    - Text chunks   : 300_processed/<domain>/<file_hash>/chunks.json hoặc 300_processed/<file_hash>/chunks.json
=======
    Source of truth:
    - Vectors + meta: 400_embeddings/<file_hash>
    - Text chunks   : 300_processed/<file_hash>/chunks.json
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

    Returns
    -------
    int
        Number of vectors ingested
    """
<<<<<<< HEAD
    coll_name = (collection_name or "").strip() or COLLECTION_NAME

    # --------------------------------------------------
    # Tìm processed_dir (có parent_dir thì không iterdir trên NAS)
    # --------------------------------------------------
    processed_dir = nas_safe_find_processed_dir(processed_root, file_hash, parent_dir=parent_dir)
    if not processed_dir:
        raise FileNotFoundError(
            f"Missing 300_processed dir for {file_hash}"
        )

    embeddings_file = embeddings_dir / "embedding.npy"
    meta_file = embeddings_dir / "chunks_meta.json"
    processed_chunks_file = processed_dir / "chunks.json"

    # --------------------------------------------------
    # Copy 3 file từ NAS sang temp local (trong container), rồi đọc từ temp — tránh Errno 35
    # --------------------------------------------------
    with tempfile.TemporaryDirectory(prefix="qdrant_ingest_") as tmp:
        tmp = Path(tmp)
        tmp_embed = tmp / "embedding.npy"
        tmp_meta = tmp / "chunks_meta.json"
        tmp_chunks = tmp / "chunks.json"
        nas_safe_copy(embeddings_file, tmp_embed)
        nas_safe_copy(meta_file, tmp_meta)
        nas_safe_copy(processed_chunks_file, tmp_chunks)

        vectors = np.load(tmp_embed)
        chunks_meta: List[Dict[str, Any]] = read_json(tmp_meta)
        chunks: List[Dict[str, Any]] = read_json(tmp_chunks)
=======

    # --------------------------------------------------
    # Paths
    # --------------------------------------------------

    embeddings_file = embeddings_dir / "embedding.npy"
    meta_file = embeddings_dir / "chunks_meta.json"
    processed_chunks_file = (
        processed_root / file_hash / "chunks.json"
    )

    if not embeddings_file.exists():
        raise FileNotFoundError(
            f"Missing embedding.npy for {file_hash}"
        )

    if not meta_file.exists():
        raise FileNotFoundError(
            f"Missing chunks_meta.json for {file_hash}"
        )

    if not processed_chunks_file.exists():
        raise FileNotFoundError(
            f"Missing 300_processed chunks.json for {file_hash}"
        )

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    vectors = np.load(embeddings_file)

    chunks_meta: List[Dict[str, Any]] = read_json(meta_file)
    chunks: List[Dict[str, Any]] = read_json(processed_chunks_file)
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

    if len(vectors) != len(chunks_meta):
        raise RuntimeError(
            f"Vector/meta count mismatch for {file_hash}: "
            f"{len(vectors)} vectors vs {len(chunks_meta)} meta"
        )

    # --------------------------------------------------
    # Build chunk_id → text map (SOURCE OF TRUTH)
    # --------------------------------------------------

    chunk_text_map = {
        c["chunk_id"]: c.get("text", "")
        for c in chunks
    }

    # --------------------------------------------------
    # Build Qdrant points
    # --------------------------------------------------

    points: List[PointStruct] = []

    for vec, meta in zip(vectors, chunks_meta):
        chunk_id = meta["chunk_id"]

        # Deterministic UUID (safe for re-run)
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{file_hash}:{chunk_id}"
            )
        )

        payload = {
            "file_hash": file_hash,
            "chunk_id": chunk_id,
            "section_id": meta.get("section_id"),
            "token_estimate": meta.get("token_estimate"),
            "text": chunk_text_map.get(chunk_id),  # 🔑 CRITICAL
            "source": "EDUAI",
        }

        points.append(
            PointStruct(
                id=point_id,
                vector=vec.tolist(),
                payload=payload,
            )
        )

    # --------------------------------------------------
    # Upsert to Qdrant
    # --------------------------------------------------

    client.upsert(
<<<<<<< HEAD
        collection_name=coll_name,
=======
        collection_name=COLLECTION_NAME,
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
        points=points,
    )

    return len(points)
