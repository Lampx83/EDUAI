# src/eduai/ingesting/pipeline.py
from pathlib import Path
import sqlite3
<<<<<<< HEAD
from typing import Optional
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

from eduai.pipelines.ingesting.inbox_scanner import scan_inbox
from eduai.pipelines.ingesting.raw_ingestor import RawIngestor


def run_ingestion(
    inbox_root: Path,
    raw_root: Path,
<<<<<<< HEAD
    conn: sqlite3.Connection,
    only_domains: Optional[list[str]] = None,
    only_path_prefixes: Optional[list[str]] = None,
    force_rerun: bool = False,
) -> None:
    ingestor = RawIngestor(raw_root, conn)
    allowed_domains = set(only_domains) if only_domains else None
    allowed_prefixes = [p.strip().rstrip("/") for p in (only_path_prefixes or []) if p.strip()]

    # Chỉ quét thư mục được chọn (only_under); nếu không chọn thì quét toàn bộ
    for inbox_file in scan_inbox(inbox_root, only_under=allowed_prefixes if allowed_prefixes else None):
        if allowed_domains is not None and inbox_file.domain not in allowed_domains:
            continue
        if allowed_prefixes:
            try:
                rel = inbox_file.path.relative_to(inbox_root)
                rel_str = str(rel).replace("\\", "/")
                if not any(rel_str == p or rel_str.startswith(p + "/") for p in allowed_prefixes):
                    continue
            except ValueError:
                continue
        ingestor.ingest(inbox_file, force=force_rerun)
=======
    conn: sqlite3.Connection
) -> None:
    ingestor = RawIngestor(raw_root, conn)

    for inbox_file in scan_inbox(inbox_root):
        ingestor.ingest(inbox_file)
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
