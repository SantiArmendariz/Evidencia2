

import numpy as np
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Insertamos título
st.write(''' # ODS 4: Educación de calidad ''')

# Insertamos texto con formato
st.markdown("""
Optimización de Recursos para el Fortalecimiento Educativo.
""")

# Insertamos una imagen
st.image("IndiaEducacion.jpg", caption="Impacto de diversos factores sobre la tasa de graduación")

# Sidebar
st.sidebar.header("Presupuesto")

# Definimos los parámetros del deslizador de presupuesto
presupuesto = st.sidebar.slider(
    "Presupuesto",
    10000000000,
    45000000000,
    30000000000
)

# Sliders de porcentajes
st.sidebar.header("Porcentaje de Becas")
porcentaje_becas = st.sidebar.slider(
    "Porcentaje de Becas",
    0.0,
    1.0,
    0.2
)

st.sidebar.header("Porcentaje de Infraestructura")
porcentaje_infra = st.sidebar.slider(
    "Porcentaje de Infraestructura",
    0.0,
    1.0,
    0.5
)

st.sidebar.header("Porcentaje de Docentes")
porcentaje_docentes = st.sidebar.slider(
    "Porcentaje de Docentes",
    0.0,
    1.0,
    0.15
)

# Cargamos el archivo con los datos
datos = pd.read_csv('ODS4India (1).csv', encoding='latin-1')

# Seleccionamos las variables
X = pd.DataFrame(datos, columns=['Inversion'])
y = datos['Porcentaje']

# Creamos y entrenamos el modelo de regresión lineal
LR = LinearRegression()
LR.fit(X, y)

# Extraemos los coeficientes de la regresión
b1 = LR.coef_[0]
b0 = LR.intercept_

# Número estimado de estudiantes
numest = 28000000

# Presupuesto por alumno
prep_alumno = presupuesto / numest

# Calculamos el presupuesto asignado a cada rubro
presupuesto_becas = presupuesto * porcentaje_becas
presupuesto_infra = presupuesto * porcentaje_infra
presupuesto_docentes = presupuesto * porcentaje_docentes

# Validar restricciones sin mostrar distribución del presupuesto
if porcentaje_becas < 0.20:
    st.warning("El presupuesto de becas no cumple con el mínimo del 20%.")
elif porcentaje_infra > 0.50:
    st.warning("El presupuesto de infraestructura excede el tope del 50%.")
elif porcentaje_docentes < 0.15:
    st.warning("La capacitación docente está por debajo del 15% obligatorio.")
else:
    st.success("Combinación de presupuesto válida.")

# Presentamos el impacto alcanzado
st.subheader('Impacto alcanzado')

impacto = (
    b0
    + prep_alumno * b1
    + presupuesto_infra / 100000000 * 0.15
    + presupuesto_docentes / 100000000 * 0.14
)

st.metric("Impacto Proyectado ODS 4", f"+{float(impacto):.3f}%")

# Presentamos el tipo de filosofía
if porcentaje_becas >= 0.40:
    filosofia = "Bienestar Primero (Equidad y Movilidad Social)"
elif porcentaje_infra >= 0.45:
    filosofia = "Rendimiento Estructural (Desarrollo Sostenible)"
elif porcentaje_docentes >= 0.35:
    filosofia = "Efecto Multiplicador (Excelencia Académica)"
else:
    filosofia = "Gobernanza Equilibrada (Modelo Balanceado)"

st.subheader("Clasificación Estratégica del Modelo")
st.info(f"Su propuesta óptima califica como un enfoque de: **{filosofia}**")
