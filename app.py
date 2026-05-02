import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os
import zipfile

st.set_page_config(page_title="Licorera La Fortuna 56", layout="centered")

# 🔷 ESTILO
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    h1 {
        color: #facc15;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍻 Licorera La Fortuna 56")
st.markdown("### Generador de Códigos de Barras")

os.makedirs("output", exist_ok=True)

# 🔷 FUNCION NORMALIZAR COLUMNA
def encontrar_columna_codigo(df):
    for col in df.columns:
        if col.strip().lower() == "código" or col.strip().lower() == "codigo":
            return col
    return None

# 🔷 INDIVIDUAL
st.header("🔹 Generar código individual")

codigo = st.text_input("Ingrese código")

if st.button("Generar código"):
    if codigo:
        barcode = Code128(codigo, writer=ImageWriter())
        filename = f"output/{codigo}"
        barcode.save(filename)

        image_path = f"{filename}.png"

        st.success("Código generado")
        st.image(image_path)

        # 🔥 BOTON DESCARGA
        with open(image_path, "rb") as f:
            st.download_button(
                label="📥 Descargar código",
                data=f,
                file_name=f"{codigo}.png",
                mime="image/png"
            )

# 🔷 EXCEL
st.header("📊 Generar desde Excel")

archivo = st.file_uploader("Sube tu Excel")

if archivo:
    df = pd.read_excel(archivo)
    st.write(df)

    columna_codigo = encontrar_columna_codigo(df)

    if columna_codigo is None:
        st.error("❌ No se encontró columna 'Código'")
    else:
        if st.button("Generar todos"):
            rutas = []

            for codigo in df[columna_codigo]:
                if pd.isna(codigo):
                    continue

                codigo = str(codigo)
                filename = f"output/{codigo}"
                barcode = Code128(codigo, writer=ImageWriter())
                barcode.save(filename)
                rutas.append(f"{filename}.png")

            zip_path = "codigos.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in rutas:
                    zipf.write(file)

            st.success("Todos los códigos generados")

            with open(zip_path, "rb") as f:
                st.download_button("📦 Descargar ZIP", f, file_name="codigos.zip")
