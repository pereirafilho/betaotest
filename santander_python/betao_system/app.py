from __future__ import annotations

import streamlit as st
import pandas as pd

from betao_system.utils import AppConfig, calcular_cubos, ensure_parent_dir
from betao_system.database import create_tables
from betao_system.ocr import ler_guia
from betao_system.brb_generator import gerar_brb


def main() -> None:
    cfg = AppConfig()
    st.set_page_config(page_title=cfg.app_title, layout="wide")
    ensure_parent_dir(cfg.db_path)
    ensure_parent_dir(f"{cfg.uploads_dir}/.keep")

    # garantir que as tabelas existem
    create_tables()

    st.title("Sistema de Controle de Betonagem")

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Programação semanal",
            "Pedido de betão",
            "Guias",
            "Cubos",
            "BRB",
            "Histórico",
        ],
    )

    if menu == "Programação semanal":
        arquivo = st.file_uploader("Importar Excel")

        if arquivo:
            df = pd.read_excel(arquivo)
            st.dataframe(df)

    elif menu == "Guias":
        imagem = st.file_uploader("Foto da guia", type=["jpg", "jpeg", "png"])

        if imagem:
            caminho = f"{cfg.uploads_dir}/guia.jpg"
            with open(caminho, "wb") as f:
                f.write(imagem.getbuffer())

            dados = ler_guia(caminho)
            st.write(dados)

    elif menu == "Cubos":
        volume = st.number_input("Volume betonado", min_value=0.0)

        if st.button("Calcular"):
            cubos = calcular_cubos(volume)
            st.success(f"Cubos necessários: {cubos}")

    elif menu == "BRB":
        if st.button("Gerar BRB"):
            dados = [
                {
                    "guia": "123",
                    "veiculo": "34-AB-12",
                    "volume": "8",
                    "saida": "07:30",
                    "chegada": "08:10",
                    "inicio": "08:15",
                    "fim": "08:25",
                }
            ]

            caminho_pdf = f"{cfg.uploads_dir}/brb.pdf"
            gerar_brb(caminho_pdf, dados)
            st.success("BRB gerado")
            st.download_button("Download BRB", open(caminho_pdf, "rb"), file_name="brb.pdf")

    elif menu == "Pedido de betão":
        st.info("Ecrã de 'Pedido de betão' ainda por implementar.")

    elif menu == "Histórico":
        st.info("Ecrã de 'Histórico' ainda por implementar.")


if __name__ == "__main__":
    main()
