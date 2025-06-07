import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "https://proyecto-notas-1.onrender.com/api"


def obtener_token(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"email": email, "password": password}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        token = r.json().get("token") or r.json().get("accessToken")
        if not token:
            st.error("No se recibió token.")
            return None
        return token
    except Exception as e:
        st.error(f"Error al hacer login: {e}")
        return None

def obtener_datos(endpoint, token):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return pd.DataFrame(r.json())
    except Exception as e:
        st.error(f"Error obteniendo datos de {endpoint}: {e}")
        return pd.DataFrame()

st.title("Análisis académico - Sistema de Notas")

email = st.text_input("Email")
password = st.text_input("Contraseña", type="password")

if st.button("Conectar"):
    token = obtener_token(email, password)
    if token:
        st.success("¡Login exitoso!")

        estudiantes = obtener_datos("estudiantes", token)
        profesores = obtener_datos("profesores", token)
        asignaturas = obtener_datos("asignaturas", token)
        calificaciones = obtener_datos("calificaciones", token)

        # Mostrar info para debugging
        st.write("Columnas en calificaciones:", calificaciones.columns.tolist())
        if not calificaciones.empty:
            st.write("Ejemplo fila calificaciones:", calificaciones.iloc[0])

        # Extraer IDs si vienen anidados
        if 'asignatura_id' not in calificaciones.columns and 'asignatura' in calificaciones.columns:
            calificaciones['asignatura_id'] = calificaciones['asignatura'].apply(lambda x: x.get('id') if isinstance(x, dict) else x)
        if 'estudiante_id' not in calificaciones.columns and 'estudiante' in calificaciones.columns:
            calificaciones['estudiante_id'] = calificaciones['estudiante'].apply(lambda x: x.get('id') if isinstance(x, dict) else x)

        # Análisis promedio notas por asignatura
        if not calificaciones.empty and not asignaturas.empty:
            st.subheader("Promedio de notas por asignatura")
            if 'asignatura_id' in calificaciones.columns and 'nota' in calificaciones.columns:
                df_promedios = calificaciones.groupby("asignatura_id")["nota"].mean().reset_index()
                df_promedios = df_promedios.merge(asignaturas, left_on="asignatura_id", right_on="id", how="left")
                st.bar_chart(df_promedios.set_index("nombre")["nota"])
            else:
                st.warning("Las columnas esperadas no están presentes en calificaciones.")

        # Histograma de notas
        if not calificaciones.empty and 'nota' in calificaciones.columns:
            st.subheader("Histograma de todas las calificaciones")
            plt.hist(calificaciones["nota"], bins=10, edgecolor='black')
            plt.xlabel("Nota")
            plt.ylabel("Frecuencia")
            st.pyplot(plt.gcf())

        # Top estudiantes por promedio
        if not estudiantes.empty and not calificaciones.empty:
            st.subheader("Top estudiantes por promedio de notas")
            if 'estudiante_id' in calificaciones.columns and 'nota' in calificaciones.columns:
                df_top = calificaciones.groupby("estudiante_id")["nota"].mean().reset_index()
                df_top = df_top.merge(estudiantes, left_on="estudiante_id", right_on="id", how="left")
                df_top = df_top.sort_values("nota", ascending=False).head(10)
                st.table(df_top[["nombre", "nota"]])
            else:
                st.warning("Las columnas esperadas no están presentes en calificaciones.")

        # Cantidad estudiantes por asignatura
        if not calificaciones.empty:
            st.subheader("Cantidad de estudiantes por asignatura")
            if 'asignatura_id' in calificaciones.columns and 'estudiante_id' in calificaciones.columns:
                df_counts = calificaciones.groupby("asignatura_id")["estudiante_id"].nunique().reset_index(name="estudiantes")
                df_counts = df_counts.merge(asignaturas, left_on="asignatura_id", right_on="id", how="left")
                st.bar_chart(df_counts.set_index("nombre")["estudiantes"])
            else:
                st.warning("Las columnas esperadas no están presentes en calificaciones.")

