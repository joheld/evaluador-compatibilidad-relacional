import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Evaluador de Compatibilidad Relacional",
    layout="wide"
)

try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except Exception as e:
    st.error(f"Error al cargar la API key: {e}")
    st.stop()

st.markdown(
    """
    <style>
    .result-card {
        padding: 1rem 1.25rem;
        border-radius: 0.8rem;
        margin-bottom: 0.8rem;
        color: #333;
    }
    .fortaleza {background-color: #e8f7f1; color: #333;}
    .mejora {background-color: #fff4e5; color: #333;}
    .recomendacion {background-color: #e8f0ff; color: #333;}
    .cientifico {background-color: #f5f5f5; color: #1a1a1a; border-left: 4px solid #666;}
    .compat-box {
        padding: 1.5rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #ff9a9e, #fecfef);
        color: white;
    }
    .compat-score {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
    }
    .compat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #0084d4;
        padding: 12px 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💛 Evaluador de Compatibilidad Relacional")
st.markdown(
    "Sistema Científico Predictivo V3.0 · Basado en investigación con más de 11,000 parejas."
)

with st.sidebar:
    st.header("i️ Información del sistema")
    st.markdown(
        """
        - Modelo VSA (Karney & Bradbury, 1995)  
        - Big Five de personalidad  
        - Teoría del apego  
        - ACE Score para trauma infantil  
        """
    )

st.header("📏 Cuéntanos tu historia")

st.markdown(
    """
    <div class="info-box">
    <b>Para un análisis más preciso, incluye:</b>
    <ul style="margin-bottom: 0; margin-top: 8px;">
    <li>Rasgos de personalidad más importantes</li>
    <li>Valores fundamentales (qué es importante para ti)</li>
    <li>Expectativas relacionales y comunicación</li>
    <li>Experiencias relevantes en relaciones anteriores</li>
    <li>Miedos o inseguridades clave</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

col_p1, col_p2 = st.columns(2)
with col_p1:
    persona1 = st.text_area(
        "Sobre ti",
        height=180,
        placeholder="Ejemplo: Soy contador, organisé y responsable. Valoro la estabilidad y la honestidad. En relaciones anteriores, noté que necesito mucha comunicación clara. Me da ansiedad la incertidumbre. Me encanta planear el futuro. Soy introvertido pero leal con mis cercanos."
    )
with col_p2:
    persona2 = st.text_area(
        "Sobre tu pareja",
        height=180,
        placeholder="Ejemplo: Es artista, creativa y auténtica. Muy social, valora la libertad y la espontaneidad. Es emocional y expresa bien sus sentimientos. A veces es desorganizada. Aprecia la flexibilidad en planes. Tiene miedos de sentirse atrapada. Es añadosa con familia y amigos."
    )

relacion = st.text_area(
    "Sobre su relación",
    height=180,
    placeholder="Ejemplo: Llevamos 3 años. Nos atrae mucho, nos divertimos. Lo mejor es que nos hacemos reír. Lo retador: él necesita estructura, ella espontaneidad. A veces hay conflictos sobre planes. Ella teme que él sea demasiado rígido. Él siente que ella no es seria. Pero somos muy leales."
)

if st.button("✨ Generar análisis", type="primary"):
    if not persona1 or not relacion:
        st.error("Por favor completa al menos las secciones sobre ti y sobre su relación.")
    else:
        with st.spinner("Analizando compatibilidad emocional y relacional…"):
            prompt = f"""
Eres un psicólogo experto en relaciones de pareja con formación en teorías de compatibilidad relacional.

Analiza esta información de una pareja:
PERSONA 1: {persona1}
PERSONA 2: {persona2}
RELACIÓN: {relacion}

Responde UNICAMENTE con un JSON válido, sin explicación extra, con esta estructura:
{{
  "compatibilidad": <número 0-100>,  
  "fortalezas": ["fortaleza 1", "fortaleza 2", "fortaleza 3", "fortaleza 4"],
  "areas_mejora": ["area 1", "area 2", "area 3"],
  "recomendaciones": ["recomendación 1", "recomendación 2", "recomendación 3", "recomendación 4"],
  "analisis_cientifico": "Análisis directo, sin filtros, sobre: posibles conflictos inherentes, diferencias fundamentales no negociables, dinámicas psicológicas probématicas, patrones de comportamiento que causan fricción, riesgos realistas a largo plazo, incompatibilidades cruzadas. Habla con franqueza científica, sin adornos ni lenguaje suavizante."
}}

Se muy específico y fundamenta el número de compatibilidad en los detalles dados.
"""

            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "sonar",
                "messages": [{"role": "user", "content": prompt}],
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()

                if "choices" in result and len(result["choices"]) > 0:
                    st.success("¡Análisis completado!")

                    raw_content = result["choices"][0]["message"]["content"]

                    try:
                        data = json.loads(raw_content)

                        compatibilidad = data.get("compatibilidad")
                        fortalezas = data.get("fortalezas", [])
                        areas_mejora = data.get("areas_mejora", [])
                        recomendaciones = data.get("recomendaciones", [])
                        analisis_cientifico = data.get("analisis_cientifico", "")

                        # ====== SECCIÓN COMPATIBILIDAD ======
                        st.subheader("❤️ Nivel de compatibilidad")

                        col_c1, col_c2 = st.columns([1, 2])
                        with col_c1:
                            st.markdown(
                                f"""
                                <div class="compat-box">
                                    <p class="compat-score">{compatibilidad}</p>
                                    <p class="compat-label">puntos sobre 100</p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with col_c2:
                            if compatibilidad is not None:
                                if compatibilidad >= 80:
                                    txt = "Muy alta: bases sólidas para una relación estable y gratificante."
                                elif compatibilidad >= 60:
                                    txt = "Buena: hay potencial claro, con algunas áreas que requieren trabajo consciente."
                                elif compatibilidad >= 40:
                                    txt = "Media: hay conexión, pero también varios focos de tensión que conviene atender."
                                else:
                                    txt = "Baja: se requieren cambios significativos y acuerdos profundos para que funcione."
                                st.markdown(f"**Interpretación:** {txt}")
                            else:
                                st.markdown("_No se pudo calcular la compatibilidad numérica._")

                        st.markdown("---")

                        # ====== FORTALEZAS ======
                        st.subheader("🌱 Fortalezas de la relación")
                        if fortalezas:
                            for f in fortalezas:
                                st.markdown(
                                    f"""
                                    <div class="result-card fortaleza">
                                        ✅ {f}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.markdown("_No se identificaron fortalezas específicas._")

                        st.markdown("---")

                        # ====== ÁREAS DE MEJORA ======
                        st.subheader("⚠️ Áreas de mejora")
                        if areas_mejora:
                            for a in areas_mejora:
                                st.markdown(
                                    f"""
                                    <div class="result-card mejora">
                                        🔍 {a}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.markdown("_No se identificaron áreas críticas de mejora._")

                        st.markdown("---")

                        # ====== RECOMENDACIONES ======
                        st.subheader("🧠 Recomendaciones prácticas")
                        if recomendaciones:
                            for r in recomendaciones:
                                st.markdown(
                                    f"""
                                    <div class="result-card recomendacion">
                                        📌 {r}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.markdown("_No se generaron recomendaciones específicas._")

                        st.markdown("---")

                        # ====== ANÁLISIS CIENTÍFICO (SIN FILTROS) ======
                        st.subheader("🔌 Análisis Científico (Sin filtros)")
                        if analisis_cientifico:
                            st.markdown(
                                f"""
                                <div class="result-card cientifico">
                                    {analisis_cientifico}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown("_No se generó análisis científico._")

                    except json.JSONDecodeError:
                        st.warning("La respuesta no vino en JSON válido. Se muestra el texto bruto:")
                        st.markdown(raw_content)

                else:
                    st.error("No se obtuvo una respuesta válida del API.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error al conectar con Perplexity API: {str(e)}")
