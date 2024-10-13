from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PyPDF2 import PdfReader

app = Flask(__name__)

# Configuración de la API
genai.configure(api_key="AIzaSyBDyn0mYQVdopEdOPPHkF_jyBt6tg1ZdBA")  # Reemplaza con tu API key

# Rutas para guardar preguntas
preguntas_file_path = "preguntas.txt"
preguntas_frecuentes_file_path = "preguntas_frecuentes.txt"  # Archivo para preguntas frecuentes

# Cargar el contenido del PDF
def cargar_articulo(path):
    reader = PdfReader(path)
    contenido = ""
    for page in reader.pages:
        contenido += page.extract_text() + "\n"
    return contenido

# Cargar el texto del PDF
texto_pdf = cargar_articulo("reglamento.pdf")  # Asegúrate de que el PDF esté en la misma carpeta o da la ruta correcta

# Funciones para manejar preguntas
def guardar_pregunta(pregunta):
    with open(preguntas_file_path, 'a', encoding='utf-8') as f:
        f.write(pregunta + '\n')

def guardar_pregunta_frecuente(pregunta):
    with open(preguntas_frecuentes_file_path, 'a', encoding='utf-8') as f:
        f.write(pregunta + '\n')

def obtener_preguntas():
    # Cargar las preguntas desde el archivo
    try:
        with open(preguntas_frecuentes_file_path, 'r', encoding='utf-8') as f:
            preguntas = [pregunta.strip() for pregunta in f.readlines() if pregunta.strip()]
    except UnicodeDecodeError:
        print("Error al decodificar el archivo. Intentando leer con otra codificación.")
        # Intenta leer con otra codificación (por ejemplo, 'latin-1')
        with open(preguntas_frecuentes_file_path, 'r', encoding='latin-1') as f:
            preguntas = [pregunta.strip() for pregunta in f.readlines() if pregunta.strip()]
    return preguntas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    pregunta = data.get('pregunta', '').strip()

    # Asegúrate de que la pregunta no esté vacía
    if pregunta:
        print("Pregunta recibida:", pregunta)

        # Obtener todas las preguntas anteriores
        preguntas_frecuentes = obtener_preguntas()
        
        # Verificar si la pregunta está en las preguntas frecuentes
        if pregunta not in preguntas_frecuentes:
            # Guardar la pregunta en el archivo
            guardar_pregunta(pregunta)

            # Crear el prompt para detectar preguntas similares
            prompt_similar = (
                "He recibido la siguiente pregunta:\n\n"
                f"{pregunta}\n\n"
                "A continuación, te muestro un conjunto de preguntas previas:\n\n"
                f"{chr(10).join(preguntas_frecuentes)}\n\n"
                "Por favor, indícame si alguna de las preguntas anteriores es similar o "
                "equivalente a la nueva. Si es así, genera una pregunta más general que "
                "resuma solo las preguntas que son similares a la nueva, caso contrario solo dame la misma bien formulada, asegurate de darme solo la pregunta."
            )
            
            # Llamada a la IA para analizar similitud
            similar_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt_similar)
            nueva_pregunta = similar_response.text.strip()
            
            if nueva_pregunta and nueva_pregunta != pregunta:
                # Si la IA genera una nueva pregunta más general
                guardar_pregunta_frecuente(nueva_pregunta)
                print("Nueva pregunta bien formulada:", nueva_pregunta)

        # Generar respuesta basada en el contenido del PDF
        prompt_respuesta = f"Contexto: {texto_pdf}\n\n Revisa el documento de la Universidad Nacional de Loja y responde en español, además empieza diciendo: La UNL ofrece..: {pregunta}"
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt_respuesta)
        respuesta = response.text

        # Retornar solo la respuesta generada sin incluir la nueva pregunta
        return jsonify({'respuesta': respuesta})

    else:
        return jsonify({'respuesta': 'No se recibió ninguna pregunta.'}), 400

@app.route('/preguntas_frecuentes', methods=['GET'])
def get_preguntas_frecuentes():
    preguntas = obtener_preguntas()  # Llama a la función para obtener preguntas frecuentes
    return jsonify({'preguntas_frecuentes': preguntas}) 

if __name__ == '__main__':
    app.run(debug=True)
