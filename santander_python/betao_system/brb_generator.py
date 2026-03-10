from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Iterable, List

from reportlab.platypus import SimpleDocTemplate, Table

from betao_system.models import GuiaBetao


def gerar_brb_payload(guia: GuiaBetao) -> Dict[str, Any]:
    """
    Gera um payload (dict) com os campos da guia.
    Pode ser usado para gerar PDF/JSON mais tarde.
    """
    payload = asdict(guia)
    payload["volume_m3"] = float(payload["volume_m3"])
    return payload


def gerar_brb(nome_arquivo: str, dados: Iterable[Dict[str, Any]]) -> None:
    """
    Gera um PDF simples com uma tabela de guias.

    Espera uma lista/iterável de dicts com as chaves:
    'guia', 'veiculo', 'volume', 'saida', 'chegada', 'inicio', 'fim'.
    """
    tabela: List[List[Any]] = [
        ["Guia", "Veículo", "Volume", "Saída", "Chegada", "Início", "Fim"],
    ]

    for d in dados:
        tabela.append(
            [
                d.get("guia", ""),
                d.get("veiculo", ""),
                d.get("volume", ""),
                d.get("saida", ""),
                d.get("chegada", ""),
                d.get("inicio", ""),
                d.get("fim", ""),
            ]
        )

    pdf = SimpleDocTemplate(nome_arquivo)
    table = Table(tabela)
    pdf.build([table])

