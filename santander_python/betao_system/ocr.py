from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import cv2
import pdfplumber
import pytesseract

from betao_system.models import OCRResult


def ocr_image_bytes(image_bytes: bytes, lang: str = "por") -> OCRResult:
    """
    OCR a single image (bytes) using Tesseract.

    Note: Requires the `tesseract` binary installed on the system.
    """
    from PIL import Image  # Pillow is already a dependency
    import io

    img = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(img, lang=lang)
    return OCRResult(text=text)


def extract_text_from_pdf(path: str, max_pages: Optional[int] = None) -> str:
    """
    Extract embedded text from a PDF (no OCR).
    For scanned PDFs, pair with `ocr_image_bytes` per page screenshot.
    """
    out = []
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages[: max_pages or len(pdf.pages)]
        for p in pages:
            out.append(p.extract_text() or "")
    return "\n\n".join(out).strip()


def ler_guia(caminho_imagem: str) -> Dict[str, str]:
    """
    Lê uma imagem de guia de betão e tenta extrair
    linhas contendo 'Guia', 'Motorista' e 'Volume'.
    """
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise ValueError(f"Não foi possível ler a imagem: {caminho_imagem}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gray)

    dados: Dict[str, str] = {}
    linhas = texto.split("\n")

    for l in linhas:
        if "Guia" in l and "guia" not in dados:
            dados["guia"] = l.strip()
        if "Motorista" in l and "motorista" not in dados:
            dados["motorista"] = l.strip()
        if "Volume" in l and "volume" not in dados:
            dados["volume"] = l.strip()

    return dados

