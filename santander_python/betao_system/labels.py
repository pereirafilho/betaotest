from __future__ import annotations

from typing import Union

from reportlab.pdfgen import canvas


APP_TITLE = "Sistema de Controle de Betonagem"

MENU_LABEL = "Menu"
MENU_OPTIONS = ["Programação semanal", "Registar guia", "Calcular cubos"]

PROGRAMACAO_TITLE = "Importar Programação"
REGISTAR_GUIA_TITLE = "Registar Guia de Betão"
CALCULAR_CUBOS_TITLE = "Cálculo de Provetes"


def gerar_etiquetas(inicio: int, quantidade: int, nome_arquivo: Union[str, bytes] = "etiquetas.pdf") -> None:
    """
    Gera um PDF simples com etiquetas:
    'Amostra <n>' em cada linha.
    """
    c = canvas.Canvas(nome_arquivo)

    y = 800
    for i in range(quantidade):
        numero = inicio + i
        texto = f"Amostra {numero}"
        c.drawString(100, y, texto)
        y -= 30

    c.save()

