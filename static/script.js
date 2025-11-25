// Elementos del DOM
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const emotionIndicator = document.getElementById('emotionIndicator');

// Mapeo de emociones a textos descriptivos
const EMOTION_LABELS = {
    'tristeza': '😢 Detecto tristeza',
    'ansiedad': '😰 Detecto ansiedad',
    'estres': '😓 Detecto estrés',
    'soledad': '😔 Detecto soledad',
    'miedo': '😨 Detecto miedo',
    'confusion': '🤔 Detecto confusión',
    'enojo': '😠 Detecto enojo',
    'cansancio': '😴 Detecto cansancio',
    'felicidad': '😊 Detecto felicidad',
    'gratitud': '🙏 Detecto gratitud',
    'motivacion': '💪 Necesitas motivación',
    'desesperanza': '💔 Detecto desesperanza',
    'saludos': '👋 Saludando',
    'despedida': '👋 Despedida',
    'animo': '✨ Dando ánimo',
    'general': '💭 Escuchando',
    'que_hacer': '🤔 Pregunta: ¿Qué hacer?',
    'sentirse_mejor': '💡 Pregunta: ¿Cómo sentirse mejor?',
    'por_que': '🤔 Pregunta: ¿Por qué?',
    'cuando': '🤔 Pregunta: ¿Cuándo?',
    'ayuda_practica': '💡 Buscando consejos prácticos',
    'no_se_que_hacer': '🤔 Sensación de estar perdido/a'
};

// Función para agregar mensaje al chat
function agregarMensaje(texto, esUsuario, emocion = null) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(esUsuario ? 'user-message' : 'bot-message');
    
    if (!esUsuario && emocion) {
        messageDiv.classList.add(emocion);
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = texto;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll automático hacia abajo
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para mostrar indicador de escritura
function mostrarEscribiendo() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot-message');
    typingDiv.id = 'typing-indicator';
    
    const typingContent = document.createElement('div');
    typingContent.classList.add('typing-indicator');
    typingContent.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(typingContent);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para quitar indicador de escritura
function quitarEscribiendo() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Función para mostrar emoción detectada
function mostrarEmocion(emocion) {
    const label = EMOTION_LABELS[emocion] || '💭 Escuchando';
    emotionIndicator.textContent = label;
    emotionIndicator.classList.add('show');
    
    setTimeout(() => {
        emotionIndicator.classList.remove('show');
    }, 3000);
}

// Función para enviar mensaje
async function enviarMensaje() {
    const mensaje = userInput.value.trim();
    
    if (mensaje === '') return;
    
    // Deshabilitar input mientras se procesa
    userInput.disabled = true;
    sendBtn.disabled = true;
    
    // Agregar mensaje del usuario
    agregarMensaje(mensaje, true);
    userInput.value = '';
    
    // Mostrar indicador de escritura
    mostrarEscribiendo();
    
    try {
        // Enviar mensaje al servidor
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mensaje: mensaje })
        });
        
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        
        const data = await response.json();
        
        // Simular delay de escritura
        setTimeout(() => {
            quitarEscribiendo();
            agregarMensaje(data.respuesta, false, data.emocion);
            mostrarEmocion(data.emocion);
            
            // Rehabilitar input
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }, 800);
        
    } catch (error) {
        console.error('Error:', error);
        quitarEscribiendo();
        agregarMensaje('Lo siento, hubo un error. Por favor intenta de nuevo.', false);
        
        // Rehabilitar input
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Event listeners
sendBtn.addEventListener('click', enviarMensaje);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !userInput.disabled) {
        enviarMensaje();
    }
});

// Enfocar el input al cargar
userInput.focus();
