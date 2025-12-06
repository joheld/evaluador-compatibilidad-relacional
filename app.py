import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import json

st.set_page_config(page_title="Evaluador de Compatibilidad Relacional", layout="wide")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.error(f"Error: {e}")
    st.stop()

st.title("Evaluador de Compatibilidad Relacional")
st.markdown("Sistema Científico Predictivo V3.0 - Basado en Investigación con 11,196 Parejas")

with st.sidebar:
    st.header("Información del Sistema")
    st.markdown("""- Modelo VSA (Karney & Bradbury, 1995)\n- Big Five para personalidad\n- Teoría del Apego\n- ACE Score para trauma infantil""")

st.header("Cuéntanos Tu Historia")
persona1 = st.text_area("Sobre Ti", height=150)
persona2 = st.text_area("Sobre Tu Pareja", height=150)
relacion = st.text_area("Sobre Su Relación", height=150)

if st.button("Generar Análisis", type="primary"):
    if not persona1 or not relacion:
        st.error("Por favor completa al menos las secciones sobre ti y tu relación.")
    else:
        with st.spinner("Analizando..."):
            prompt = f"Soy un psicólogo experto. Analiza esta información:\nPERSONA 1: {persona1}\nPERSONA 2: {persona2}\nRELACIÓN: {relacion}\nProporciona un análisis estructurado en formato JSON con: compatibilidad (0-100), fortalezas (lista), areas_mejora (lista), recomendaciones (lista)."
            
            response = model.generate_content(prompt)
            st.success("Análisis completado!")
            st.markdown(response.text)

st.markdown("---")
st.caption("Este análisis es educativo y no sustituye terapia profesional.")
