import os
from pathlib import Path
from dotenv import load_dotenv


def _load_env_from_project_root() -> None:
    """
    Tìm file .env bằng cách đi ngược lên cây thư mục
    Bắt đầu từ vị trí file hiện tại.
    """
    current = Path(__file__).resolve()

    for parent in [current] + list(current.parents):
        env_file = parent / ".env"
        if env_file.exists():
<<<<<<< HEAD
            # override=True: .env ghi đè biến môi trường đã có (tránh /data từ Docker khi chạy dev)
            load_dotenv(dotenv_path=env_file, override=True)
=======
            load_dotenv(dotenv_path=env_file)
>>>>>>> 59e59ae0f1ae7f00b194320e3da9c0520b7f9c56
            return

    # Không raise ở đây – để fail-fast ở get_env()
    # Điều này giúp debug rõ ràng hơn


# Load .env ngay khi import module
_load_env_from_project_root()


def get_env(key: str, default: str | None = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


def get_path(key: str) -> Path:
    return Path(get_env(key)).expanduser().resolve()
