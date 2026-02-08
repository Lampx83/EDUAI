from pathlib import Path
<<<<<<< HEAD
from typing import Optional
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56

from eduai.common.jsonio import write_json
from eduai.pipelines.staging.pdf_analyzer import analyze_pdf


def run_pdf_staging(
    file_hash: str,
    raw_pdf_path: Path,
    staging_root: Path,
<<<<<<< HEAD
    parent_dir: Optional[str] = None,
=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
) -> None:
    """
    Chạy pipeline staging cho PDF (200_staging).

<<<<<<< HEAD
    parent_dir: thư mục cha (domain) — output sẽ là 200_staging/<parent_dir>/<file_hash>/
    Nếu không truyền: 200_staging/<file_hash>/ (giữ tương thích).

=======
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    Sinh:
      - pdf_profile.json
      - validation.json
      - (tuỳ chọn) text_sample.txt
    """

<<<<<<< HEAD
    if parent_dir:
        staging_dir = staging_root / parent_dir / file_hash
    else:
        staging_dir = staging_root / file_hash
=======
    staging_dir = staging_root / file_hash
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
    staging_dir.mkdir(parents=True, exist_ok=True)

    # ---------- 1. Analyze PDF ----------
    profile = analyze_pdf(raw_pdf_path)

    write_json(
        staging_dir / "pdf_profile.json",
        profile,
    )

    # ---------- 2. Build validation ----------
    validation = {
        "file_type": "pdf",
        "requires_ocr": profile.get("is_scanned", False),
        "has_tables": profile.get("has_tables", False),
        "recommended_pipeline": ["pdf_text_extract"],
    }

    write_json(
        staging_dir / "validation.json",
        validation,
    )
