from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PyPDF2 import PdfReader

app = Flask(__name__)

# Cargar el contenido del PDF
def cargar_articulo(path):
    reader = PdfReader(path)
    contenido = ""
    for page in reader.pages:
        contenido += page.extract_text() + "\n"
    return contenido

# Cargar el texto del PDF
texto_pdf = cargar_articulo("reglamento.pdf")  # Asegúrate de que el PDF esté en la misma carpeta o da la ruta correcta

# Configurar la API con la clave
genai.configure(api_key="AIzaSyBDyn0mYQVdopEdOPPHkF_jyBt6tg1ZdBA")  # Reemplaza con tu API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    pregunta = data.get('pregunta', '')

    # Respuestas específicas sobre las preguntas frecuentes
    respuestas_frecuentes = {
        "¿Cuáles son los objetivos del reglamento académico?": "Los objetivos del Reglamento de Régimen Académico de la Universidad Nacional de Loja incluyen definir los principios, normas y disposiciones que regulan el funcionamiento académico en la universidad.",
        "¿Qué modalidades de estudio ofrece la universidad?": "La universidad ofrece modalidades de estudio presencial, semipresencial, a distancia y en línea, adaptándose a las necesidades de los estudiantes.",
        "¿Cómo se realiza la evaluación de los aprendizajes?": "La evaluación de los aprendizajes se basa en los criterios establecidos en el reglamento académico y los planes de estudio de cada carrera.",
        "¿Qué se necesita para la admisión y matrícula?": "Para la admisión y matrícula, es necesario cumplir con los requisitos establecidos en el reglamento de admisión de la universidad.",
    }

    respuesta = respuestas_frecuentes.get(pregunta, "")

    if respuesta:
        return jsonify({'respuesta': respuesta})
    
    # Si no es una pregunta frecuente, genera respuesta basada en el contenido del PDF
    prompt = f"Contexto: {texto_pdf}\n\n Revisa el documento y responde ademas empieza diciendo:La UNL ofrece..: {pregunta}"

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    respuesta = response.text

    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True)
