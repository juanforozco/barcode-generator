import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os
import zipfile
import base64

# ==============================
# 🔷 CONFIG
# ==============================
st.set_page_config(page_title="Licorera La Fortuna 56", layout="wide")

# ==============================
# 🔷 CARGAR IMAGEN BASE64
# ==============================
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

img_base64 = get_base64_image("assets/fondo.jpg")

# ==============================
# 🔥 ESTILOS
# ==============================
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
    margin-top: -50px;
}}

html, body, [class*="css"] {{
    font-family: 'Segoe UI', sans-serif;
}}

h1, h2, h3 {{
    color: #facc15;
}}

p, label {{
    color: white;
}}

.stButton > button {{
    background: linear-gradient(90deg, #facc15, #eab308);
    color: black;
    font-size: 16px;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}}

.stButton > button:hover {{
    transform: scale(1.05);
    background: linear-gradient(90deg, #eab308, #facc15);
}}

</style>
""", unsafe_allow_html=True)

# ==============================
# 🔷 HEADER PRO (HERO)
# ==============================
st.markdown("""
<div style='text-align:center; padding:40px 0;'>

    <h1 style='
        font-size:70px;
        color:#facc15;
        font-weight:bold;
        letter-spacing:2px;
        margin-bottom:10px;
    '>
        🍻 LICORERA LA FORTUNA 56
    </h1>

    <p style='
        font-size:22px;
        color:white;
        opacity:0.9;
    '>
        Generador de códigos de barras
    </p>

</div>
""", unsafe_allow_html=True)

# ==============================
# 🔷 SETUP
# ==============================
os.makedirs("output", exist_ok=True)

def encontrar_columna_codigo(df):
    for col in df.columns:
        if col.strip().lower() in ["codigo", "código"]:
            return col
    return None

# ==============================
# 🔷 LAYOUT
# ==============================
col1, col2 = st.columns(2)

# ==============================
# 🍬 INDIVIDUAL
# ==============================
with col1:
    st.markdown("## 🍬 Generar código individual")

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
# 🍺 EXCEL
# ==============================
with col2:
    st.markdown("## 🍺 Generar desde Excel")

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

# ==============================
# 🔷 FOOTER
# ==============================
st.markdown("---")
st.markdown("✨ Próximamente: Inventario | Ventas | Reportes")
