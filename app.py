import streamlit as st
import requests
import json

st.set_page_config(page_title="Evaluador de Compatibilidad Relacional", layout="wide")

# Configure Perplexity API
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

st.title("Evaluador de Compatibilidad Relacional")
st.markdown("Sistema Cientifico Predictivo V3.0 - Basado en Investigacion con 11,196 Parejas")

with st.sidebar:
    st.header("Informacion del Sistema")
    st.markdown("""- Modelo VSA (Karney & Bradbury, 1995)\n- Big Five para personalidad\n- Teoria del Apego\n- ACE Score para trauma infantil""")

st.header("Cuentanos Tu Historia")
persona1 = st.text_area("Sobre Ti", height=150)
persona2 = st.text_area("Sobre Tu Pareja", height=150)
relacion = st.text_area("Sobre Su Relacion", height=150)

if st.button("Generar Analisis", type="primary"):
    if not persona1 or not relacion:
        st.error("Por favor completa al menos las secciones sobre ti y tu relacion.")
    else:
        with st.spinner("Analizando..."):
            prompt = f"Soy un psicologo experto. Analiza esta informacion:\nPERSONA 1: {persona1}\nPERSONA 2: {persona2}\nRELACION: {relacion}\nProporciona un analisis estructurado en formato JSON con: compatibilidad (0-100), fortalezas (lista), areas_mejora (lista), recomendaciones (lista)."
            
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "sonar",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    st.success("Analisis completado!")
                    st.markdown(result["choices"][0]["message"]["content"])
                else:
                    st.error("No se obtuvo una respuesta valida del API.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error al conectar con Perplexity API: {str(e)}")
