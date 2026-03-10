from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class AppConfig:
    app_title: str = "Sistema de Controle de Betonagem"
    db_path: str = "data/database.db"
    uploads_dir: str = "uploads"


def read_excel(file) -> pd.DataFrame:
    """
    Read an uploaded Excel file into a DataFrame.

    `file` may be a Streamlit UploadedFile or a path-like.
    """
    return pd.read_excel(file, engine="openpyxl")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def require_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    required = [str(c).strip() for c in required]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def calcular_cubos(volume_m3: float) -> int:
    """
    Heurística simples:
    - mínimo: 0 se volume <= 0
    - caso contrário: 1 conjunto (6 cubos) a cada 50 m³, arredondando para cima
    """
    if volume_m3 <= 0:
        return 0
    conjuntos = math.ceil(volume_m3 / 50.0)
    return int(conjuntos) * 6
