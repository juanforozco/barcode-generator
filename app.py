import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os
import zipfile

st.set_page_config(page_title="Licorera La Fortuna 56", layout="wide")

# 🔥 FONDO + ESTILO
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.9)),
                url("fondo.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

h1, h2, h3 {{
    color: #facc15;
}}

.stButton>button {{
    background-color: #facc15;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}}

.block-container {{
    background-color: rgba(0,0,0,0.75);
    padding: 2rem;
    border-radius: 15px;
}}

</style>
""", unsafe_allow_html=True)

st.title("🍻 LICORERA LA FORTUNA 56")
st.subheader("Generador de Códigos de Barras")

os.makedirs("output", exist_ok=True)

# 🔷 FUNCION COLUMNA FLEXIBLE
def encontrar_columna_codigo(df):
    for col in df.columns:
        if col.strip().lower() in ["codigo", "código"]:
            return col
    return None

# 🔷 COLUMNAS VISUALES
col1, col2 = st.columns(2)

# 🔹 INDIVIDUAL
with col1:
    st.header("🔹 Generar código individual")

    codigo = st.text_input("Ingrese código")

    if st.button("Generar código"):
        if codigo:
            barcode = Code128(codigo, writer=ImageWriter())
            filename = f"output/{codigo}"
            barcode.save(filename)

            path = f"{filename}.png"

            st.image(path)

            with open(path, "rb") as f:
                st.download_button(
                    "📥 Descargar",
                    f,
                    file_name=f"{codigo}.png"
                )

# 🔹 EXCEL
with col2:
    st.header("📊 Generar desde Excel")

    archivo = st.file_uploader("Sube tu Excel")

    if archivo:
        df = pd.read_excel(archivo)
        st.dataframe(df)

        col_codigo = encontrar_columna_codigo(df)

        if col_codigo is None:
            st.error("No se encontró columna Código")
        else:
            if st.button("Generar todos"):
                rutas = []

                for codigo in df[col_codigo]:
                    if pd.isna(codigo):
                        continue

                    codigo = str(codigo)
                    filename = f"output/{codigo}"
                    Code128(codigo, writer=ImageWriter()).save(filename)
                    rutas.append(f"{filename}.png")

                zip_path = "codigos.zip"
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for file in rutas:
                        zipf.write(file)

                with open(zip_path, "rb") as f:
                    st.download_button("📦 Descargar ZIP", f)

st.markdown("---")
st.markdown("✨ Próximamente: Inventario | Ventas | Reportes")
