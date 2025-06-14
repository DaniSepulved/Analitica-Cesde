import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

st.set_page_config(page_title="Panel Académico", layout="wide")
st.title("🎓 Panel de Análisis Académico")

st.markdown("""
Este panel te permite explorar el desempeño académico del sistema de notas. A continuación verás estadísticas clave como:
- **Promedios por asignatura**
- **Distribución de notas**
- **Top estudiantes**
- **Cantidad de estudiantes por asignatura**
""")

# --- Login ---
with st.sidebar:
    st.header("🔐 Autenticación")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")
    login = st.button("Iniciar sesión")

BASE_URL = "https://proyecto-notas-1.onrender.com/api"

def obtener_token(email, password):
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        res.raise_for_status()
        return res.json().get("token")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
        return None

def obtener_datos(endpoint, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
        res.raise_for_status()
        return pd.DataFrame(res.json())
    except Exception as e:
        st.error(f"Error al obtener {endpoint}: {e}")
        return pd.DataFrame()

if login and email and password:
    token = obtener_token(email, password)
    if token:
        st.success("✅ Autenticado correctamente")

        # --- Cargar datos ---
        estudiantes = obtener_datos("estudiantes", token)
        profesores = obtener_datos("profesores", token)
        asignaturas = obtener_datos("asignaturas", token)
        calificaciones = obtener_datos("calificaciones", token)

        # --- Preprocesamiento ---
        if 'asignatura' in calificaciones.columns:
            calificaciones['asignatura_id'] = calificaciones['asignatura'].apply(lambda x: x.get('id') if isinstance(x, dict) else x)
        if 'estudiante' in calificaciones.columns:
            calificaciones['estudiante_id'] = calificaciones['estudiante'].apply(lambda x: x.get('id') if isinstance(x, dict) else x)

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Promedios", "📈 Histograma", "🏅 Top Estudiantes", "📚 Estudiantes por Asignatura"])

        with tab1:
            st.subheader("Promedio de notas por asignatura")
            if not calificaciones.empty and 'asignatura_id' in calificaciones.columns:
                df_prom = calificaciones.groupby("asignatura_id")["nota"].mean().reset_index()
                df_prom = df_prom.merge(asignaturas, left_on="asignatura_id", right_on="id", how="left")

                top_n = st.slider("¿Cuántas asignaturas quieres ver?", 5, 30, 10)
                df_prom = df_prom.sort_values("nota", ascending=False).head(top_n)

                fig, ax = plt.subplots(figsize=(12, 6))
                sns.barplot(x="nombre", y="nota", data=df_prom, palette="crest", ax=ax)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
                ax.set_xlabel("Asignatura")
                ax.set_ylabel("Promedio")
                st.pyplot(fig)
            else:
                st.warning("No hay datos de calificaciones.")

        with tab2:
            st.subheader("Distribución general de calificaciones")
            fig, ax = plt.subplots()
            sns.histplot(calificaciones["nota"], bins=10, kde=True, ax=ax)
            ax.set_xlabel("Nota")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

        with tab3:
            st.subheader("Top 10 estudiantes por promedio")
            if not estudiantes.empty:
                df_top = calificaciones.groupby("estudiante_id")["nota"].mean().reset_index()
                df_top = df_top.merge(estudiantes, left_on="estudiante_id", right_on="id", how="left")
                df_top = df_top.sort_values("nota", ascending=False).head(10)
                st.table(df_top[["nombre", "nota"]])
            else:
                st.warning("No hay datos de estudiantes.")

        with tab4:
            st.subheader("🎯 Top 5 asignaturas con más estudiantes")
            st.markdown("Este gráfico muestra las **5 asignaturas** con mayor número de estudiantes registrados en el sistema.")

            if not calificaciones.empty and 'asignatura_id' in calificaciones.columns and 'estudiante_id' in calificaciones.columns:
                df_counts = calificaciones.groupby("asignatura_id")["estudiante_id"].nunique().reset_index(name="estudiantes")
                df_counts = df_counts.merge(asignaturas, left_on="asignatura_id", right_on="id", how="left")
                df_counts = df_counts.sort_values("estudiantes", ascending=False).head(5)

                fig, ax = plt.subplots()
                ax.pie(df_counts["estudiantes"],
                       labels=df_counts["nombre"],
                       autopct="%1.1f%%",
                       startangle=90,
                       colors=plt.cm.viridis.colors[:5])
                ax.axis("equal")  # Para que sea un círculo perfecto
                st.pyplot(fig)
            else:
                st.warning("No hay datos suficientes para generar la gráfica.")
