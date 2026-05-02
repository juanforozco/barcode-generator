import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os
import zipfile

st.title("🧾 Generador de Códigos de Barras")

os.makedirs("output", exist_ok=True)

# Código individual
st.header("Generar código individual")

codigo = st.text_input("Ingrese código")

if st.button("Generar código"):
    if codigo:
        barcode = Code128(codigo, writer=ImageWriter())
        filename = f"output/{codigo}"
        barcode.save(filename)
        st.success("Código generado")
        st.image(f"{filename}.png")

# Excel
st.header("Generar desde Excel")

archivo = st.file_uploader("Sube tu Excel")

if archivo:
    df = pd.read_excel(archivo)
    st.write(df)

    if st.button("Generar todos"):
        rutas = []

        for codigo in df["Código"]:
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
            st.download_button("Descargar ZIP", f, file_name="codigos.zip")
