from flask import Flask, render_template, request, jsonify
import random
import re
from collections import Counter

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
        "Está bien llorar. Las lágrimas son una forma de liberar lo que llevamos dentro. Te acompaño. 💙",
        "Siento que estés pasando por esto. A veces la tristeza nos visita, pero no se quedará para siempre. 🌸",
        "Tu dolor es real y merece ser reconocido. No tienes que fingir que estás bien. 💙",
        "Entiendo que todo parezca oscuro ahora. Pero has sobrevivido a días difíciles antes, y lo harás de nuevo. 🌟",
        "La tristeza es parte de ser humano. No te hace débil sentirte así. Te hace real. 💫"
    ],
    'ansiedad': [
        "Respira profundo. Inhala... exhala... Estás a salvo en este momento. 🌸",
        "La ansiedad puede ser abrumadora, pero recuerda: esto pasará. Estás siendo muy valiente. 💪",
        "Intenta enfocarte en el presente. ¿Qué puedes ver, oír o sentir ahora mismo? Ancláte al momento. 🍃",
        "Tu ansiedad es real, pero no define quién eres. Eres más fuerte que este sentimiento. ✨",
        "Está bien sentirse ansioso/a. ¿Has probado respirar contando hasta 4? Puede ayudarte a calmarte. 🌿",
        "Reconozco tu ansiedad. Prueba esto: nombra 5 cosas que ves, 4 que tocas, 3 que oyes, 2 que hueles, 1 que saboreas. 🌺",
        "La ansiedad miente. Te dice que algo terrible pasará, pero estás aquí, ahora, y estás a salvo. 💙",
        "Tus preocupaciones son válidas, pero no tienen que controlarte. Respira, un momento a la vez. 🍃",
        "Es agotador sentir ansiedad. Recuerda que tu cuerpo está tratando de protegerte, aunque ahora no haya peligro real. 💫"
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
        "Te escucho. ¿Qué más hay en tu mente? 💙",
        "Puedes hablar con confianza. Este es un espacio seguro para ti. 🌟",
        "Tus palabras importan. Sigue compartiendo lo que sientes. 💫",
        "Estoy prestando atención. ¿Qué más te gustaría contarme? 🤗",
        "No hay prisa. Tómate el tiempo que necesites para expresarte. 🌸",
        "Lo que sientes es importante. Continúa, te estoy escuchando. 💙"
    ]
}

# Palabras clave expandidas para mejor detección
PALABRAS_CLAVE = {
    'saludos': ['hola', 'hey', 'buenos días', 'buenas tardes', 'buenas noches', 
                'qué tal', 'saludos', 'hi', 'hello', 'buenas', 'holi', 'que onda'],
    'tristeza': ['triste', 'mal', 'deprimido', 'deprimida', 'lloro', 'llorando',
                 'llorar', 'dolor', 'sufro', 'sufriendo', 'horrible', 'terrible',
                 'melancólico', 'melancólica', 'desanimado', 'desanimada', 'apagado',
                 'vacío', 'vacía', 'tristeza', 'pena', 'decaído', 'decaída'],
    'ansiedad': ['ansiedad', 'ansioso', 'ansiosa', 'nervioso', 'nerviosa', 
                 'preocupado', 'preocupada', 'pánico', 'angustia', 'inquieto',
                 'inquieta', 'temor', 'agobiado', 'agobiada', 'abrumado', 'abrumada',
                 'ataque de ansiedad', 'no puedo respirar', 'taquicardia', 'palpitaciones'],
    'estres': ['estrés', 'estres', 'estresado', 'estresada', 'presión', 'presionado',
               'sobrepasado', 'sobrepasada', 'ocupado', 'ocupada', 'ajetreado', 'tensión',
               'sobrecarga', 'demasiado', 'colapso', 'desbordado', 'desbordada'],
    'soledad': ['solo', 'sola', 'soledad', 'abandonado', 'abandonada', 'aislado',
                'aislada', 'nadie me entiende', 'incomprendido', 'incomprendida',
                'sin amigos', 'sin nadie', 'me siento solo', 'me siento sola'],
    'miedo': ['miedo', 'asustado', 'asustada', 'terror', 'aterrado', 'aterrada',
              'pánico', 'temor', 'me da miedo', 'tengo miedo', 'aterrorizado',
              'espantado', 'espantada', 'horrorizado'],
    'confusion': ['confundido', 'confundida', 'confusión', 'no sé', 'perdido', 'perdida',
                  'desorientado', 'desorientada', 'dudas', 'indeciso', 'indecisa',
                  'no entiendo', 'qué hago', 'qué debo hacer', 'no se que hacer'],
    'enojo': ['enojado', 'enojada', 'enojo', 'molesto', 'molesta', 'furioso', 'furiosa',
              'rabia', 'ira', 'enfadado', 'enfadada', 'irritado', 'irritada', 'cabreado',
              'cabreada', 'odio', 'frustrado', 'frustrada', 'harto', 'harta'],
    'cansancio': ['cansado', 'cansada', 'agotado', 'agotada', 'exhausto', 'exhausta',
                  'fatigado', 'fatigada', 'sueño', 'rendido', 'rendida', 'sin energía',
                  'sin fuerzas', 'colapsado', 'colapsada', 'destruido', 'destruida'],
    'felicidad': ['feliz', 'alegre', 'contento', 'contenta', 'genial', 'excelente',
                  'maravilloso', 'bien', 'muy bien', 'fantástico', 'increíble', 'emocionado',
                  'emocionada', 'super bien', 'de maravilla', 'radiante', 'eufórico'],
    'gratitud': ['gracias', 'agradezco', 'agradecido', 'agradecida', 'graciasss',
                 'thank', 'muchas gracias', 'te agradezco', 'mil gracias'],
    'motivacion': ['motiva', 'motivación', 'ánimo', 'animo', 'ayúdame', 'ayuda', 
                   'fuerza', 'lograr', 'conseguir', 'éxito', 'meta', 'objetivo',
                   'necesito ánimo', 'dame fuerzas', 'inspírame', 'impulso'],
    'desesperanza': ['no puedo más', 'me quiero morir', 'sin esperanza', 'rendirme',
                     'no vale la pena', 'mejor morir', 'suicidarme', 'acabar con todo',
                     'no tiene sentido', 'desesperado', 'desesperada', 'sin salida',
                     'ya no aguanto', 'quiero desaparecer', 'no hay salida'],
    'despedida': ['adiós', 'adios', 'chao', 'hasta luego', 'me voy', 'bye',
                  'nos vemos', 'chau', 'hasta pronto', 'me despido']
}

# Palabras comunes a ignorar (stop words en español)
STOP_WORDS = {
    'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
    'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
    'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
    'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
    'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
    'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
    'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
    'sí', 'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa',
    'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte',
    'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar',
    'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo',
    'decir', 'estos', 'trabajar', 'nombre', 'aquí', 'dar', 'allí', 'tienen',
    'tiene', 'puede', 'puedo', 'puedes', 'estoy', 'está', 'estás', 'son', 'soy',
    'eres', 'he', 'has', 'ha', 'hemos', 'han', 'ante', 'un', 'una', 'unos', 'unas'
}

# Patrones de preguntas y respuestas específicas
PATRONES_PREGUNTAS = {
    'que_hacer': {
        'palabras': ['qué puedo hacer', 'qué hago', 'qué debería hacer', 'qué me recomiendas',
                     'qué me aconsejas', 'cómo puedo', 'cómo hago', 'necesito ayuda con',
                     'como puedo', 'como hago', 'que deberia hacer', 'que hago para',
                     'ayudame a', 'ayúdame a', 'como me', 'cómo me'],
        'respuestas': [
            "Entiendo que buscas orientación. ¿Podrías contarme más sobre la situación específica? Así podré ayudarte mejor. 💙",
            "Es valioso que busques soluciones. Cuéntame más detalles sobre lo que estás enfrentando y exploremos opciones juntos. 🌟",
            "Me gustaría ayudarte a encontrar un camino. ¿Qué aspecto del problema te preocupa más en este momento? 💫",
            "Buscar ayuda es un gran paso. Háblame más sobre tu situación para poder darte un apoyo más específico. 🤗",
            "Veo que necesitas orientación. A veces ayuda dividir el problema en partes más pequeñas. ¿Por dónde quieres empezar? 🌸"
        ]
    },
    'sentirse_mejor': {
        'palabras': ['cómo puedo sentirme mejor', 'como puedo sentirme mejor', 'quiero sentirme mejor',
                     'cómo me siento mejor', 'como me siento mejor', 'como sentirme mejor',
                     'cómo sentirme mejor', 'para sentirme mejor', 'sentirme bien', 'estar mejor',
                     'mejorar mi estado', 'mejorarme', 'recuperarme'],
        'respuestas': [
            "Para sentirte mejor, prueba: 1) Sal a caminar 15-20 minutos (el movimiento ayuda), 2) Habla con alguien de confianza, 3) Haz algo que normalmente disfrutas, aunque no tengas ganas. ¿Cuál crees que podrías probar hoy? 💙",
            "Aquí hay estrategias que pueden ayudarte: • Ejercicio suave (caminar, estirarte), • Técnicas de respiración profunda, • Escuchar música que te guste, • Escribir lo que sientes, • Contactar a un amigo. ¿Alguna te llama la atención? 🌟",
            "Para mejorar tu estado emocional: 1) Cuida tu cuerpo (duerme bien, come saludable), 2) Practica gratitud (nombra 3 cosas positivas del día), 3) Limita redes sociales, 4) Busca apoyo profesional si lo necesitas. 💫",
            "Te recomiendo: • Sal de tu espacio actual (aunque sea al balcón), • Escucha música que te energice, • Haz algo creativo o manual, • Practica mindfulness 5 minutos, • Habla con alguien que te entienda. 🌸",
            "Algunas cosas que pueden ayudarte: 1) El método 5-4-3-2-1 (nombra 5 cosas que ves, 4 que tocas, 3 que oyes, 2 que hueles, 1 que saboreas), 2) Respiración 4-7-8, 3) Llama a alguien querido, 4) Haz una lista de logros recientes. 🤗"
        ]
    },
    'por_que': {
        'palabras': ['por qué me siento', 'por qué estoy', 'por qué me pasa', 'por qué siento',
                     'por qué tengo', 'no entiendo por qué', 'porque me siento', 'porque estoy',
                     'a qué se debe', 'cual es la razon', 'cuál es la razón'],
        'respuestas': [
            "Es natural preguntarse el porqué de nuestros sentimientos. A veces no hay una sola razón, y está bien. ¿Qué crees que podría estar influyendo? 💙",
            "Buscar entender nuestras emociones es importante. Los sentimientos pueden tener múltiples causas. ¿Hay algo que haya cambiado recientemente? 🌟",
            "Tus sentimientos son válidos, tengan o no una causa clara. ¿Quieres explorar qué situaciones los desencadenan? 💫",
            "A veces nuestras emociones nos hablan de necesidades no satisfechas. ¿Qué crees que tu emoción está tratando de decirte? 🌸"
        ]
    },
    'cuando': {
        'palabras': ['cuándo pasará', 'cuándo me sentiré', 'cuándo terminará', 'cuándo mejorará',
                     'hasta cuándo', 'cuando pasara', 'cuando me sentire', 'cuando terminara',
                     'cuando mejorare', 'cuanto tiempo', 'cuánto tiempo'],
        'respuestas': [
            "Sé que quisieras saber cuándo terminará esto. Aunque no tengo una fecha exacta, sé que los sentimientos difíciles son temporales. 💙",
            "Entiendo la necesidad de ver un final. Cada persona tiene su propio ritmo de sanación. Vas avanzando, aunque no siempre lo sientas. 🌟",
            "Es agotador no saber cuándo mejorará. Lo que sí sé es que estás dando pasos importantes al buscar apoyo. Eso cuenta. 💫",
            "Desear que termine el dolor es completamente normal. Cada día que enfrentas es progreso, aunque sea invisible. 🌸"
        ]
    },
    'ayuda_practica': {
        'palabras': ['dame un consejo', 'necesito un consejo', 'qué me sugieres', 'algún tip',
                     'alguna técnica', 'ejercicio', 'método', 'dame tips', 'dame consejos',
                     'que me sugieres', 'alguna recomendacion', 'alguna recomendación',
                     'tecnicas', 'técnicas', 'estrategias', 'herramientas'],
        'respuestas': [
            "Con gusto te comparto técnicas efectivas: 1) Respiración 4-7-8 (inhala 4seg, sostén 7seg, exhala 8seg), 2) Escribe tus pensamientos sin filtro, 3) La regla de los 2 minutos: haz algo productivo por solo 2 minutos. ¿Cuál te resuena? 💙",
            "Herramientas que pueden ayudarte: • Método 5-4-3-2-1 para ansiedad, • Journaling (escribir 3 páginas en la mañana), • Ejercicio físico aunque sea 10 minutos, • Meditación guiada (apps: Headspace, Calm). 🌟",
            "Te sugiero probar: 1) Box breathing (inhala 4, sostén 4, exhala 4, sostén 4), 2) Lista de cosas que SÍ puedes controlar hoy, 3) Pausa consciente de 5 minutos, 4) Pregúntate: '¿Qué necesito ahora mismo?' 💫",
            "Estrategias prácticas: • Movimiento (yoga, caminar, bailar), • Música que te guste, • Llamar a alguien de confianza, • Técnica RAIN (Reconoce, Acepta, Investiga, Nutre), • Permitirte descansar sin culpa. 🌸",
            "Ejercicios efectivos: 1) Gratitud: escribe 3 cosas buenas del día, 2) Visualización: imagina tu lugar seguro, 3) Grounding: toca algo frío/caliente, 4) Afirmaciones positivas, 5) Rutina matutina consistente. 🤗"
        ]
    },
    'no_se_que_hacer': {
        'palabras': ['no sé qué hacer', 'no se que hacer', 'estoy perdido', 'estoy perdida',
                     'me siento perdido', 'me siento perdida', 'no se por donde empezar',
                     'no sé por dónde empezar', 'estoy confundido', 'estoy confundida'],
        'respuestas': [
            "Entiendo esa sensación de estar perdido/a. Empecemos por algo pequeño: ¿qué es lo más urgente o lo que más te preocupa ahora mismo? A veces un paso a la vez es todo lo que necesitamos. 💙",
            "Es normal sentirse así cuando hay mucho en la mente. Te propongo: 1) Escribe todo lo que te preocupa, 2) Elige UNA cosa para enfocarte hoy, 3) Da un paso pequeño hacia eso. No necesitas resolver todo ahora. 🌟",
            "Cuando no sabes por dónde empezar, pregúntate: '¿Qué haría mi yo más sabio/a?' o '¿Qué le diría a un amigo en mi situación?' A veces esa perspectiva ayuda. 💫",
            "No necesitas tener todas las respuestas ahora. Está bien sentirse perdido/a. Prueba esto: 1) Respira profundo, 2) Identifica una necesidad básica (descanso, comida, conexión), 3) Atiéndela. Lo demás puede esperar. 🌸"
        ]
    }
}

def normalizar_texto(texto):
    """Normaliza el texto eliminando acentos y convirtiendo a minúsculas"""
    texto = texto.lower()
    # Reemplazar acentos comunes
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', '¿': '', '?': '', '¡': '', '!': ''
    }
    for orig, repl in reemplazos.items():
        texto = texto.replace(orig, repl)
    return texto

def extraer_palabras_significativas(mensaje):
    """Extrae palabras significativas eliminando stop words"""
    mensaje_normalizado = normalizar_texto(mensaje)
    palabras = re.findall(r'\b\w+\b', mensaje_normalizado)
    palabras_significativas = [p for p in palabras if p not in STOP_WORDS and len(p) > 2]
    return palabras_significativas

def detectar_patron_pregunta(mensaje):
    """Detecta si el mensaje coincide con patrones de preguntas específicas"""
    mensaje_lower = mensaje.lower()
    mensaje_normalizado = normalizar_texto(mensaje)
    
    # Revisar cada patrón en orden de especificidad
    for patron, datos in PATRONES_PREGUNTAS.items():
        for frase in datos['palabras']:
            frase_normalizada = normalizar_texto(frase)
            # Buscar tanto en el mensaje original como en el normalizado
            if frase in mensaje_lower or frase_normalizada in mensaje_normalizado:
                return patron
    
    return None

def calcular_similitud_palabras(palabras_mensaje, palabras_emocion):
    """Calcula similitud basada en palabras en común"""
    if not palabras_mensaje or not palabras_emocion:
        return 0
    
    # Contar coincidencias
    coincidencias = len(set(palabras_mensaje) & set(palabras_emocion))
    
    # Normalizar por el tamaño del mensaje
    similitud = coincidencias / max(len(palabras_mensaje), 1)
    
    return similitud

def detectar_emocion(mensaje):
    """Detecta la emoción predominante en el mensaje del usuario con PLN mejorado"""
    mensaje_lower = mensaje.lower()
    
    # 1. PRIORIDAD: Detectar patrones de preguntas
    patron_pregunta = detectar_patron_pregunta(mensaje)
    if patron_pregunta:
        return f'pregunta_{patron_pregunta}'
    
    # 2. Priorizar detección de desesperanza (importante para seguridad)
    for palabra in PALABRAS_CLAVE['desesperanza']:
        if palabra in mensaje_lower:
            return 'desesperanza'
    
    # 3. Extraer palabras significativas del mensaje
    palabras_mensaje = extraer_palabras_significativas(mensaje)
    
    # 4. Análisis con PLN: contador de coincidencias por categoría con pesos mejorados
    puntuaciones = {}
    
    for categoria, palabras in PALABRAS_CLAVE.items():
        if categoria == 'desesperanza':  # Ya la verificamos
            continue
        
        puntuacion = 0
        coincidencias = 0
        palabras_normalizadas = [normalizar_texto(p) for p in palabras]
        
        for palabra in palabras:
            palabra_normalizada = normalizar_texto(palabra)
            
            if palabra in mensaje_lower or palabra_normalizada in ' '.join(palabras_mensaje):
                coincidencias += 1
                # Peso basado en longitud de palabra
                peso_base = len(palabra)
                
                # Palabras completas valen más (no solo substring)
                palabras_msg = mensaje_lower.split()
                if palabra in palabras_msg or palabra_normalizada in palabras_mensaje:
                    peso_base *= 2.5
                
                # Primera palabra del mensaje tiene más peso
                if mensaje_lower.startswith(palabra):
                    peso_base *= 2
                
                # Frases exactas tienen mucho más valor
                if len(palabra.split()) > 1 and palabra in mensaje_lower:
                    peso_base *= 3
                
                puntuacion += peso_base
        
        # 5. Bonus por densidad de palabras emocionales
        if palabras_mensaje:
            similitud = calcular_similitud_palabras(palabras_mensaje, palabras_normalizadas)
            puntuacion *= (1 + similitud)
        
        # 6. Bonus por múltiples coincidencias en la misma categoría
        if coincidencias > 1:
            puntuacion *= (1 + coincidencias * 0.3)
        
        if puntuacion > 0:
            puntuaciones[categoria] = puntuacion
    
    # 7. Si encontramos emociones, devolver la más fuerte
    if puntuaciones:
        emocion_detectada = max(puntuaciones, key=puntuaciones.get)
        # Solo retornar si la confianza es razonable
        if puntuaciones[emocion_detectada] > 3:
            return emocion_detectada
    
    # 8. Para mensajes cortos sin palabras clave, analizar contexto
    if len(mensaje) < 30:
        # Detectar signos de pregunta (confusión/ayuda)
        if '?' in mensaje or mensaje_lower.startswith(('cómo', 'como', 'qué', 'que', 'cuál', 'cual')):
            return 'confusion'
        # Detectar exclamaciones (puede ser enojo o felicidad)
        if '!' in mensaje and mensaje.count('!') > 1:
            return 'felicidad' if any(word in mensaje_lower for word in ['jaja', 'jeje', 'jiji', 'wow', 'genial']) else 'enojo'
        # Si hay emoción detectada pero con baja confianza, usarla
        if puntuaciones:
            return max(puntuaciones, key=puntuaciones.get)
        # Mensaje corto sin contexto claro
        return 'general'
    
    # 9. Mensajes largos sin palabras clave reconocidas
    if len(palabras_mensaje) > 5:
        return 'general'
    
    # 10. Por defecto, dar ánimo
    return 'animo'

def obtener_respuesta(mensaje):
    """Obtiene una respuesta apropiada basada en el mensaje del usuario"""
    emocion = detectar_emocion(mensaje)
    
    # Verificar si es un patrón de pregunta específica
    if emocion.startswith('pregunta_'):
        patron = emocion.replace('pregunta_', '')
        respuestas = PATRONES_PREGUNTAS[patron]['respuestas']
        return random.choice(respuestas)
    
    # Respuesta normal basada en emoción
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
    
    # Limpiar el nombre de emoción para el frontend
    emocion_display = emocion_detectada.replace('pregunta_', '')
    
    return jsonify({
        'respuesta': respuesta,
        'emocion': emocion_display
    })

if __name__ == '__main__':
    app.run(debug=True)
