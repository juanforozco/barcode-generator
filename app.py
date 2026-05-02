import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os
import zipfile
import base64

# 🔷 CONFIG
st.set_page_config(page_title="Licorera La Fortuna 56", layout="wide")

# 🔷 FUNCION PARA CARGAR IMAGEN
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# 🔷 CARGAR IMAGEN
img_base64 = get_base64_image("assets/fondo.jpg")

# 🔥 ESTILO GLOBAL
st.markdown(f"""
<style>

.stApp {{
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)),
                url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    background: rgba(0,0,0,0.6);
    padding: 2rem;
    border-radius: 20px;
}}

h1, h2, h3 {{
    color: #facc15;
}}

p, label {{
    color: white;
}}

.stButton>button {{
    background-color: #facc15;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}}

</style>
""", unsafe_allow_html=True)

# 🔷 HEADER PRO
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <h1 style='font-size:60px;'>🍻 LICORERA LA FORTUNA 56</h1>
    <p style='font-size:22px;'>Generador de códigos de barras</p>
</div>
""", unsafe_allow_html=True)

# 🔷 CREAR CARPETA OUTPUT
os.makedirs("output", exist_ok=True)

# 🔷 FUNCION BUSCAR COLUMNA
def encontrar_columna_codigo(df):
    for col in df.columns:
        if col.strip().lower() in ["codigo", "código"]:
            return col
    return None

# 🔷 LAYOUT
col1, col2 = st.columns(2)

# ==============================
# 🔹 CÓDIGO INDIVIDUAL
# ==============================
with col1:
    st.subheader("🔹 Generar código individual")

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
                    "📥 Descargar código",
                    f,
                    file_name=f"{codigo}.png",
                    mime="image/png"
                )

# ==============================
# 🔹 DESDE EXCEL
# ==============================
with col2:
    st.subheader("📊 Generar desde Excel")

    archivo = st.file_uploader("Sube tu Excel")

    if archivo:
        df = pd.read_excel(archivo)
        st.dataframe(df)

        col_codigo = encontrar_columna_codigo(df)

        if col_codigo is None:
            st.error("❌ No se encontró columna 'Código'")
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
                    st.download_button(
                        "📦 Descargar ZIP",
                        f,
                        file_name="codigos.zip"
                    )

# 🔷 FOOTER
st.markdown("---")
st.markdown("✨ Próximamente: Inventario | Ventas | Reportes")
