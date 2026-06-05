from pathlib import Path
from src.config import logging

DOC_DIR = Path(__file__).parent.parent / "doc"
DOC_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("TP1")
logger.addHandler(logging.FileHandler(DOC_DIR / "app.log", mode="a"))
