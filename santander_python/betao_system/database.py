from __future__ import annotations

import sqlite3
from pathlib import Path

from betao_system.utils import AppConfig, ensure_parent_dir


def _db_path() -> str:
    cfg = AppConfig()
    ensure_parent_dir(cfg.db_path)
    return cfg.db_path


def connect() -> sqlite3.Connection:
    """
    Abre ligação à base de dados principal (data/database.db).
    """
    return sqlite3.connect(_db_path(), check_same_thread=False)


def create_tables() -> None:
    """
    Cria as tabelas principais: programacao, guias, betonagens.
    """
    conn = connect()
    c = conn.cursor()

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS programacao(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        hora_inicio TEXT,
        frente TEXT,
        elemento TEXT,
        classe_resistencia TEXT,
        classe_exposicao TEXT,
        slump TEXT,
        agregado TEXT,
        volume REAL
    )
    """
    )

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS guias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_guia TEXT,
        veiculo TEXT,
        volume REAL,
        saida_central TEXT,
        chegada_obra TEXT,
        inicio_descarga TEXT,
        fim_descarga TEXT,
        motorista TEXT
    )
    """
    )

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS betonagens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        classe_betao TEXT,
        volume_total REAL
    )
    """
    )

    conn.commit()
    conn.close()
