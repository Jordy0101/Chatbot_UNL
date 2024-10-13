function mostrarFlujo() {
    const canvaFlujo = document.getElementById('canva-flujo');
    
    // Alternar la clase 'mostrar' para mostrar u ocultar el iframe
    if (canvaFlujo.style.display === "none") {
        canvaFlujo.style.display = "block"; // Mostrar el iframe
        setTimeout(() => { // Esperar a que el display se haya establecido para aplicar opacidad
            canvaFlujo.style.opacity = "1"; // Cambiar a opacidad 1
        }, 10); // Timeout pequeño para asegurar que el navegador renderice el cambio de display antes de cambiar la opacidad
    } else {
        canvaFlujo.style.opacity = "0"; // Cambiar a opacidad 0
        setTimeout(() => { // Esperar a que la opacidad se haya establecido antes de ocultar el iframe
            canvaFlujo.style.display = "none"; // Ocultar el iframe
        }, 500); // Este tiempo debe coincidir con la duración de la transición de opacidad
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
