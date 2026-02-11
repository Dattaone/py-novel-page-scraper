from pathlib import Path
import sys

APP_NAME = "Novel Scraper"

def _is_frozen()->bool:
    return hasattr(sys, "frozen", False)

def _get_base_path()->Path:
    """
    Da una ruta segura:
    -En .exe: carpeta del usuario sin necesidad de permisos.
    - En .py: carpeta del proyecto
    """
    if _is_frozen():
        return Path.home() / APP_NAME
    else:
        return Path(__file__).resolve().parents[2] # sube 2 niveles

BASE_DIR = _get_base_path()

#Salidas
OUTPUT_DIR = BASE_DIR / "output"
AUTO_SAVE_TXT = OUTPUT_DIR / "auto_save.txt"


def ensure_dirs():
    for path in (
        OUTPUT_DIR,
        AUTO_SAVE_TXT
    ):
        path.mkdir(parents=True, exist_ok=True)

ensure_dirs()