from pathlib import Path
<<<<<<< HEAD
from typing import Any, Dict, List, Literal, Optional
=======
from typing import Dict, Any, List, Literal
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
from datetime import datetime
import json
import tempfile
import shutil

import numpy as np
from sentence_transformers import SentenceTransformer

<<<<<<< HEAD
from eduai.common.jsonio import write_json
from eduai.common.nas_io import (
    nas_safe_copy,
    nas_safe_mkdir,
    nas_safe_read_json,
)
=======
from eduai.common.jsonio import read_json, write_json
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56


EmbeddingStatus = Literal["EMBEDDED", "SKIPPED"]

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def run_embedding_pipeline(
    file_hash: str,
    processed_dir: Path,
    embeddings_root: Path,
    model_name: str = DEFAULT_MODEL_NAME,
    force: bool = False,
<<<<<<< HEAD
    parent_dir: Optional[str] = None,
) -> EmbeddingStatus:
    """
    parent_dir: thư mục cha (domain) — output sẽ là 400_embeddings/<parent_dir>/<file_hash>/
    Nếu không truyền: 400_embeddings/<file_hash>/ (giữ tương thích).
=======
) -> EmbeddingStatus:
    """
    FINAL – NAS SAFE – PRODUCTION GRADE
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    """

    # =====================================================
    # 1. Validate input
    # =====================================================
    chunks_file = processed_dir / "chunks.json"
    if not chunks_file.exists():
        raise RuntimeError(f"Missing chunks.json for {file_hash}")

<<<<<<< HEAD
    if parent_dir:
        out_dir = embeddings_root / parent_dir / file_hash
    else:
        out_dir = embeddings_root / file_hash
=======
    out_dir = embeddings_root / file_hash
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    final_path = out_dir / "embedding.npy"

    if final_path.exists() and not force:
        print(f"[400] Skip (already embedded): {file_hash}")
        return "SKIPPED"

    # =====================================================
<<<<<<< HEAD
    # 2. Load chunks (đọc từ NAS với retry)
    # =====================================================
    chunks: List[Dict[str, Any]] = nas_safe_read_json(chunks_file)
=======
    # 2. Load chunks
    # =====================================================
    chunks: List[Dict[str, Any]] = read_json(chunks_file)
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    texts = [c["text"].strip() for c in chunks if c.get("text")]

    if not texts:
        print(f"[400] No valid text chunks for {file_hash}, skip")
        return "SKIPPED"

    # =====================================================
    # 3. Load model & embed
    # =====================================================
    print(f"[400] Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    print(f"[400] Embedding {len(texts)} chunks for {file_hash}")
    vectors = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    ).astype("float32")

<<<<<<< HEAD
=======
    # =====================================================
    # 4. WRITE TO LOCAL FS FIRST (CRITICAL)
    # =====================================================
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        tmp_embedding = tmpdir / "embedding.npy"
        np.save(tmp_embedding, vectors)   # ✔ local FS, 100% safe

        # ---------- ensure target dir ----------
        out_dir.mkdir(parents=True, exist_ok=True)

        # ---------- atomic copy to NAS ----------
        shutil.copy2(tmp_embedding, final_path)

    # =====================================================
    # 5. Metadata
    # =====================================================
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    chunks_meta = [
        {
            "chunk_id": c.get("chunk_id"),
            "section_id": c.get("section_id"),
            "file_hash": file_hash,
            "token_estimate": c.get("token_estimate"),
        }
        for c in chunks
    ]

<<<<<<< HEAD
    # =====================================================
    # 4. Ghi toàn bộ ra LOCAL temp, rồi copy từng file lên NAS (có retry)
    #    Tránh Errno 35 "Resource deadlock avoided" trên NFS/Synology
    # =====================================================
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        np.save(tmpdir / "embedding.npy", vectors)
        write_json(tmpdir / "chunks_meta.json", chunks_meta)
        write_json(
            tmpdir / "model.json",
            {
                "model_name": model_name,
                "embedding_dim": int(vectors.shape[1]),
                "chunk_count": len(vectors),
                "created_at": datetime.utcnow().isoformat(),
                "pipeline": "400_embeddings",
            },
        )
        with (tmpdir / "embedding.jsonl").open("w", encoding="utf-8") as f:
            for meta, vec in zip(chunks_meta, vectors):
                f.write(
                    json.dumps(
                        {**meta, "vector": vec.tolist()},
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        nas_safe_mkdir(out_dir)
        nas_safe_copy(tmpdir / "embedding.npy", final_path)
        nas_safe_copy(tmpdir / "chunks_meta.json", out_dir / "chunks_meta.json")
        nas_safe_copy(tmpdir / "model.json", out_dir / "model.json")
        nas_safe_copy(tmpdir / "embedding.jsonl", out_dir / "embedding.jsonl")
=======
    write_json(out_dir / "chunks_meta.json", chunks_meta)

    write_json(
        out_dir / "model.json",
        {
            "model_name": model_name,
            "embedding_dim": int(vectors.shape[1]),
            "chunk_count": len(vectors),
            "created_at": datetime.utcnow().isoformat(),
            "pipeline": "400_embeddings",
        },
    )

    with (out_dir / "embedding.jsonl").open("w", encoding="utf-8") as f:
        for meta, vec in zip(chunks_meta, vectors):
            f.write(
                json.dumps(
                    {**meta, "vector": vec.tolist()},
                    ensure_ascii=False,
                )
                + "\n"
            )
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

    print(f"[400] Completed embedding for {file_hash}")
    return "EMBEDDED"
