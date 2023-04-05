import streamlit as st
import openai
import math

# Crear una columna izquierda en la interfaz de Streamlit
left_column = st.sidebar

# Añadir un título y una casilla de entrada para la clave API de OpenAI en la columna izquierda
left_column.title("Evaluador de Trabajos")
api_key = left_column.text_input("Ingrese su clave API de OpenAI:", type="password")
openai.api_key = api_key

# Configura tus claves de API de OpenAI aquí
openai.api_key = "tu_clave_api"

# Función para calificar ensayos
def calificar_ensayo(ensayo, ponderaciones, criterios):
    prompt = f"Calificar el siguiente ensayo basado en los siguientes criterios:\n\nEnsayo:\n{ensayo}\n\nCriterios:\n"

    for i, criterio in enumerate(criterios):
        prompt += f"{i + 1}. {criterio}: Ponderación {ponderaciones[i]}%\n"

    prompt += "\nPor favor, proporciona una calificación justificada para cada criterio y una calificación total."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Criterios de calificación
criterios = [
    "Contenido",
    "Comprensión",
    "Precisión",
    "Creatividad",
    "Organización",
    "Presentación",
    "Coherencia",
    "Habilidad técnica",
    "Investigación",
    "Participación",
]

st.title("Calificador de ensayos con GPT-4")
st.write("Por favor, ingrese el ensayo y ajuste las ponderaciones de los criterios de calificación.")

ensayo = st.text_area("Ensayo (min. 500 palabras):", max_chars=None)

ponderaciones = []
for criterio in criterios:
    ponderacion = st.slider(criterio, 0, 100, 10)
    ponderaciones.append(ponderacion)

if sum(ponderaciones) != 100:
    st.warning("La suma de las ponderaciones debe ser igual a 100.")
else:
    if len(ensayo.split()) < 500:
        st.warning("El ensayo debe tener al menos 500 palabras.")
    else:
        if st.button("Calificar ensayo"):
            st.write("Calificando el ensayo, por favor espere...")
            calificacion = calificar_ensayo(ensayo, ponderaciones, criterios)
            st.write(calificacion)
