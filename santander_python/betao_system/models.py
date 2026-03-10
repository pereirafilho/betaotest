from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass(frozen=True)
class GuiaBetao:
    guia: str
    veiculo: str
    volume_m3: float
    saida_central: time
    chegada_obra: time
    inicio_descarga: time
    fim_descarga: time


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: Optional[float] = None
