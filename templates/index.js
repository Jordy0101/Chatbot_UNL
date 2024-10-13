function mostrarFlujo() {
    const canvaFlujo = document.getElementById('canva-flujo');
    if (canvaFlujo.style.display === "none") {
        canvaFlujo.style.display = "block";
    } else {
        canvaFlujo.style.display = "none";
    }
}

function hacerPregunta(pregunta) {
    document.getElementById('pregunta').value = pregunta;
    document.getElementById('send-btn').click();
}

document.getElementById('send-btn').onclick = async function() {
    const pregunta = document.getElementById('pregunta').value;
    const chatBox = document.getElementById('chat-box');

    // Mensaje del usuario
    chatBox.innerHTML += `<div class="message user-message"><p>${pregunta}</p></div>`;

    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pregunta }),
    });
    const data = await response.json();

    // Procesar el formato del texto para convertir los asteriscos en negritas y listas
    let formattedResponse = data.respuesta
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Convertir **texto** en <strong>texto</strong>
        .replace(/\* (.*?)\n/g, '<li>$1</li>') // Convertir * item en <li>item</li>
        .replace(/\n/g, '<br>'); // Convertir saltos de línea en <br>

    // Agregar el mensaje del chatbot con el formato HTML
    chatBox.innerHTML += `<div class="message"><p>${formattedResponse}</p></div>`;
    document.getElementById('pregunta').value = '';
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazarse hacia abajo
};
