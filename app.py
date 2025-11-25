from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

# Respuestas del chatbot organizadas por categorías expandidas
RESPUESTAS = {
    'saludos': [
        "¡Hola! Me alegra mucho verte por aquí 😊 ¿Cómo estás hoy?",
        "¡Hola! Es genial que hayas venido. Estoy aquí para ti. ¿Qué tal tu día?",
        "¡Hey! Qué bueno que estés aquí. ¿Cómo te sientes?",
        "¡Bienvenido/a! Estoy aquí para acompañarte. ¿Cómo va todo?"
    ],
    'tristeza': [
        "Entiendo que te sientas así. Es completamente válido sentirse triste a veces. Estoy aquí para acompañarte. 💙",
        "Lamento que estés pasando por un momento difícil. Recuerda que no estás solo/a. 🤗",
        "Tus sentimientos son válidos. Permítete sentir, pero también recuerda que eres fuerte. 💪",
        "Es normal tener días difíciles. Lo importante es que estás buscando apoyo, eso es muy valiente. 🌟",
        "Está bien llorar. Las lágrimas son una forma de liberar lo que llevamos dentro. Te acompaño. 💙"
    ],
    'ansiedad': [
        "Respira profundo. Inhala... exhala... Estás a salvo en este momento. 🌸",
        "La ansiedad puede ser abrumadora, pero recuerda: esto pasará. Estás siendo muy valiente. 💪",
        "Intenta enfocarte en el presente. ¿Qué puedes ver, oír o sentir ahora mismo? Ancláte al momento. 🍃",
        "Tu ansiedad es real, pero no define quién eres. Eres más fuerte que este sentimiento. ✨",
        "Está bien sentirse ansioso/a. ¿Has probado respirar contando hasta 4? Puede ayudarte a calmarte. 🌿"
    ],
    'estres': [
        "Suena como que has tenido mucho en tu plato. Recuerda tomar pausas, eres humano/a. 🌺",
        "El estrés puede ser agotador. ¿Qué tal si te tomas un momento para ti? Lo mereces. ☕",
        "A veces necesitamos bajar el ritmo. No tienes que hacer todo hoy. 🌸",
        "Prioriza tu bienestar. Las tareas pueden esperar, pero tu salud mental no. 💙",
        "Reconocer que estás estresado/a es el primer paso. ¿Hay algo que puedas delegar o posponer? 🌿"
    ],
    'soledad': [
        "No estás solo/a, aunque a veces lo parezca. Estoy aquí contigo en este momento. 💙",
        "La soledad puede doler, pero también es temporal. Hay personas que se preocupan por ti. 🤗",
        "A veces nos sentimos solos incluso rodeados de gente. Tu sentimiento es válido. 🌟",
        "Estoy aquí para acompañarte. Cuéntame lo que necesites, no tienes que cargar esto solo/a. 💫",
        "La conexión humana es importante. ¿Hay alguien de confianza con quien puedas hablar? Estoy aquí mientras tanto. 🌸"
    ],
    'miedo': [
        "El miedo es natural. Eres valiente por enfrentarlo y hablar de ello. 💪",
        "Está bien tener miedo. No significa que seas débil, significa que eres humano/a. 🌟",
        "¿Qué es lo que más te asusta? A veces ponerlo en palabras le quita un poco de poder. 💙",
        "Recuerda: has superado el 100% de tus días difíciles hasta ahora. Puedes con esto. ✨",
        "El miedo puede ser abrumador, pero no tiene que controlarte. Respira, estás a salvo. 🌸"
    ],
    'confusion': [
        "Es normal sentirse confundido/a a veces. No tienes que tener todas las respuestas ahora. 🌿",
        "La confusión puede ser incómoda, pero es parte del proceso de encontrar claridad. 💫",
        "Está bien no saber qué hacer. Tómate tu tiempo para ordenar tus pensamientos. 🌸",
        "A veces necesitamos dar un paso atrás para ver las cosas con más claridad. No te presiones. 💙",
        "La vida puede ser confusa. ¿Hay algo específico que te gustaría ordenar en tu mente? 🍃"
    ],
    'enojo': [
        "Es válido sentir enojo. ¿Qué te ha molestado? A veces expresarlo ayuda. 🌋",
        "El enojo es una emoción legítima. Lo importante es cómo lo manejamos. Respira hondo. 💪",
        "Está bien estar molesto/a. Tus sentimientos importan. ¿Quieres hablar de lo que pasó? 💙",
        "Sentir rabia es humano. Permítete sentirlo sin juzgarte. Estoy aquí para escucharte. 🌸",
        "El enojo nos dice que algo es importante para nosotros. ¿Qué te está diciendo el tuyo? 🔥"
    ],
    'cansancio': [
        "Entiendo que estés cansado/a. ¿Has pensado en tomar un pequeño descanso? Tu bienestar es importante. 🌸",
        "El descanso no es debilidad, es necesidad. Date permiso para cuidarte. 💆",
        "Parece que necesitas recargar energías. Recuerda ser amable contigo mismo/a. 🌿",
        "Tu cuerpo te está pidiendo descanso. Escúchalo, lo mereces. 😴",
        "El agotamiento es real. No eres flojo/a por necesitar descansar. Eres humano/a. 💙"
    ],
    'felicidad': [
        "¡Me encanta verte así de feliz! 🎉 ¡Disfruta este momento maravilloso!",
        "¡Qué alegría! Tu felicidad es contagiosa. 😊✨",
        "¡Eso es genial! Mereces toda la felicidad del mundo. 🌟",
        "¡Celebra estos momentos! Son los que hacen que la vida valga la pena. 🎊",
        "Tu alegría ilumina todo. ¡Sigue brillando! ☀️"
    ],
    'gratitud': [
        "¡De nada! Siempre estaré aquí cuando me necesites. 😊",
        "Es un placer poder ayudarte. Cuídate mucho. 💙",
        "Para eso estoy aquí. ¡Ánimo y adelante! 🌟",
        "Me alegra haber podido acompañarte. Vuelve cuando quieras. 🤗"
    ],
    'motivacion': [
        "¡Tú puedes con esto y mucho más! Confía en ti mismo/a. 💪✨",
        "Cada esfuerzo cuenta, por pequeño que sea. ¡Sigue adelante! 🚀",
        "Eres capaz de cosas increíbles. Sólo necesitas creer en ti. 🌟",
        "El éxito no es la ausencia de fracasos, sino la persistencia a pesar de ellos. ¡Adelante! 🎯",
        "Recuerda por qué empezaste. Ese fuego sigue en ti. ¡Aviva la llama! 🔥",
        "Cada día es una nueva oportunidad para ser la mejor versión de ti. ¡Vamos! 💫"
    ],
    'desesperanza': [
        "Sé que ahora parece oscuro, pero la luz volverá. Has sido fuerte antes, lo serás otra vez. 💙",
        "La desesperanza es temporal, aunque no lo parezca ahora. Por favor, aguanta un poco más. 🌟",
        "No estás solo/a en esto. Si te sientes muy mal, por favor busca ayuda profesional. Mereces apoyo. 💚",
        "Los momentos más oscuros vienen justo antes del amanecer. No te rindas. 🌅",
        "Tu vida tiene valor, incluso si ahora no puedes verlo. Por favor, habla con alguien de confianza. 💙"
    ],
    'despedida': [
        "¡Hasta pronto! Recuerda que siempre puedes volver. Cuídate mucho. 💙",
        "¡Adiós! Que tengas un excelente día. Siempre estaré aquí para ti. 😊",
        "¡Nos vemos! Recuerda que eres increíble. 🌟",
        "¡Que estés muy bien! Vuelve cuando necesites. 👋💙"
    ],
    'animo': [
        "¡Eres increíble! 💪 Recuerda que cada día es una nueva oportunidad para brillar.",
        "Sé que las cosas pueden ser difíciles, pero eres más fuerte de lo que crees. ¡Ánimo! ✨",
        "Tu valor no depende de tus logros, eres valioso/a simplemente por ser tú. 💙",
        "Los días difíciles no duran para siempre. Mañana será un nuevo día lleno de posibilidades. 🌅",
        "Está bien no estar bien todo el tiempo. Lo importante es que sigues adelante. 🌟",
        "Cada pequeño paso que das es un logro. ¡Estoy orgulloso/a de ti! 🎉",
        "Recuerda: después de la tormenta siempre sale el sol. Esto también pasará. ☀️"
    ],
    'general': [
        "Cuéntame más sobre eso. Estoy aquí para escucharte. 💙",
        "Entiendo. ¿Hay algo específico en lo que pueda ayudarte? 🤗",
        "Gracias por compartir eso conmigo. ¿Cómo puedo apoyarte mejor? 💫",
        "Estoy aquí para ti. Tómate tu tiempo y cuéntame lo que necesites. 🌸",
        "Te escucho. ¿Qué más hay en tu mente? 💙"
    ]
}

# Palabras clave expandidas para mejor detección
PALABRAS_CLAVE = {
    'saludos': ['hola', 'hey', 'buenos días', 'buenas tardes', 'buenas noches', 
                'qué tal', 'saludos', 'hi', 'hello', 'buenas'],
    'tristeza': ['triste', 'mal', 'deprimido', 'deprimida', 'solo', 'sola', 
                 'llorar', 'lloro', 'dolor', 'sufro', 'horrible', 'terrible',
                 'melancólico', 'melancólica', 'desanimado', 'desanimada'],
    'ansiedad': ['ansiedad', 'ansioso', 'ansiosa', 'nervioso', 'nerviosa', 
                 'preocupado', 'preocupada', 'pánico', 'angustia', 'inquieto',
                 'inquieta', 'temor', 'agobiado', 'agobiada', 'abrumado', 'abrumada'],
    'estres': ['estrés', 'estres', 'estresado', 'estresada', 'presión', 'presionado',
               'sobrepasado', 'sobrepasada', 'ocupado', 'ocupada', 'ajetreado', 'tensión'],
    'soledad': ['solo', 'sola', 'soledad', 'abandonado', 'abandonada', 'aislado',
                'aislada', 'nadie me entiende', 'incomprendido', 'incomprendida'],
    'miedo': ['miedo', 'asustado', 'asustada', 'terror', 'aterrado', 'aterrada',
              'pánico', 'temor', 'me da miedo', 'tengo miedo'],
    'confusion': ['confundido', 'confundida', 'confusión', 'no sé', 'perdido', 'perdida',
                  'desorientado', 'desorientada', 'dudas', 'indeciso', 'indecisa'],
    'enojo': ['enojado', 'enojada', 'enojo', 'molesto', 'molesta', 'furioso', 'furiosa',
              'rabia', 'ira', 'enfadado', 'enfadada', 'irritado', 'irritada', 'cabreado'],
    'cansancio': ['cansado', 'cansada', 'agotado', 'agotada', 'exhausto', 'exhausta',
                  'fatigado', 'fatigada', 'sueño', 'rendido', 'rendida'],
    'felicidad': ['feliz', 'alegre', 'contento', 'contenta', 'genial', 'excelente',
                  'maravilloso', 'bien', 'muy bien', 'fantástico', 'increíble', 'emocionado'],
    'gratitud': ['gracias', 'agradezco', 'agradecido', 'agradecida', 'graciasss',
                 'thank', 'muchas gracias', 'te agradezco'],
    'motivacion': ['motiva', 'motivación', 'ánimo', 'animo', 'ayuda', 'puedo',
                   'fuerza', 'lograr', 'conseguir', 'éxito', 'meta', 'objetivo'],
    'desesperanza': ['no puedo más', 'me quiero morir', 'sin esperanza', 'rendirme',
                     'no vale la pena', 'mejor morir', 'suicidarme', 'acabar con todo',
                     'no tiene sentido', 'desesperado', 'desesperada'],
    'despedida': ['adiós', 'adios', 'chao', 'hasta luego', 'me voy', 'bye',
                  'nos vemos', 'chau', 'hasta pronto']
}

def detectar_emocion(mensaje):
    """Detecta la emoción predominante en el mensaje del usuario"""
    mensaje_lower = mensaje.lower()
    
    # Priorizar detección de desesperanza (importante para seguridad)
    for palabra in PALABRAS_CLAVE['desesperanza']:
        if palabra in mensaje_lower:
            return 'desesperanza'
    
    # Contador de coincidencias por categoría
    puntuaciones = {}
    
    for categoria, palabras in PALABRAS_CLAVE.items():
        if categoria == 'desesperanza':  # Ya la verificamos
            continue
        puntuacion = 0
        for palabra in palabras:
            if palabra in mensaje_lower:
                # Palabras más largas tienen más peso
                puntuacion += len(palabra)
        if puntuacion > 0:
            puntuaciones[categoria] = puntuacion
    
    # Devolver la categoría con mayor puntuación
    if puntuaciones:
        return max(puntuaciones, key=puntuaciones.get)
    
    # Si el mensaje es muy corto, respuesta general
    if len(mensaje) < 20:
        return 'general'
    
    # Por defecto, dar ánimo
    return 'animo'

def obtener_respuesta(mensaje):
    """Obtiene una respuesta apropiada basada en el mensaje del usuario"""
    emocion = detectar_emocion(mensaje)
    respuestas = RESPUESTAS.get(emocion, RESPUESTAS['general'])
    return random.choice(respuestas)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    mensaje_usuario = request.json.get('mensaje', '')
    if not mensaje_usuario:
        return jsonify({'error': 'No se recibió mensaje'}), 400
    
    respuesta = obtener_respuesta(mensaje_usuario)
    emocion_detectada = detectar_emocion(mensaje_usuario)
    
    return jsonify({
        'respuesta': respuesta,
        'emocion': emocion_detectada
    })

if __name__ == '__main__':
    app.run(debug=True)
