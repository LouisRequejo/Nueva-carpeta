# ChatBot de Ánimo 💙

Una aplicación web interactiva creada con Flask para dar ánimo y apoyo emocional a quienes lo necesitan.

## ✨ Características

- 💬 **Chat interactivo** con respuestas motivacionales y empáticas
- 🎨 **Interfaz moderna** y responsive con animaciones suaves
- 🧠 **Detección inteligente de emociones** - Identifica 13 estados emocionales diferentes
- 💙 **Respuestas personalizadas** según el estado emocional detectado
- 🌈 **Indicador visual** de la emoción detectada
- ⚡ **Respuesta en tiempo real** con indicador de escritura
- 🌐 **Desplegable en la nube** fácilmente con PythonAnywhere

## 🎭 Emociones Detectadas

El chatbot puede identificar y responder a:

- 👋 **Saludos y despedidas**
- 😢 **Tristeza** - Brinda consuelo y comprensión
- 😰 **Ansiedad** - Ofrece técnicas de calma y apoyo
- 😓 **Estrés** - Sugiere pausas y autocuidado
- 😔 **Soledad** - Acompaña y valida sentimientos
- 😨 **Miedo** - Da seguridad y ánimo
- 🤔 **Confusión** - Ayuda a ordenar pensamientos
- 😠 **Enojo** - Valida la emoción y ofrece espacio
- 😴 **Cansancio** - Recuerda la importancia del descanso
- 😊 **Felicidad** - Celebra los momentos positivos
- 🙏 **Gratitud** - Reciproca el agradecimiento
- 💪 **Necesidad de motivación** - Impulsa a seguir adelante
- 💔 **Desesperanza** - Ofrece apoyo crítico y recursos

## 🚀 Instalación Local

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona el repositorio** (o descarga los archivos)
```bash
git clone https://github.com/TU_USUARIO/chatbot-animo.git
cd chatbot-animo
```

2. **Crea un entorno virtual** (recomendado)
```bash
python -m venv venv
```

3. **Activa el entorno virtual**

En Windows:
```bash
venv\Scripts\activate
```

En Mac/Linux:
```bash
source venv/bin/activate
```

4. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecuta la aplicación**
```bash
python app.py
```

6. **Abre tu navegador** y ve a:
```
http://127.0.0.1:5000
```

## 📁 Estructura del Proyecto

```
chatbot-animo/
│
├── app.py                 # Aplicación Flask principal con lógica del chatbot
├── wsgi.py               # Configuración WSGI para deployment
├── requirements.txt      # Dependencias del proyecto
├── deploy.sh            # Script de despliegue automático
├── GUIDE.md             # Guía completa de despliegue en PythonAnywhere
├── .gitignore           # Archivos a ignorar en Git
│
├── templates/
│   └── index.html       # Plantilla HTML del chat
│
└── static/
    ├── style.css        # Estilos y diseño visual
    └── script.js        # Lógica del frontend
```

## 🌐 Desplegar en PythonAnywhere

Para hacer tu chatbot accesible desde internet, sigue la guía completa en **[GUIDE.md](GUIDE.md)**.

### Resumen Rápido:

1. Crea una cuenta en [PythonAnywhere](https://www.pythonanywhere.com/)
2. Sube tu proyecto (vía Git o manualmente)
3. Configura la aplicación web
4. ¡Listo! Tu chatbot estará en línea en `https://TU_USUARIO.pythonanywhere.com`

### Script Automático

También puedes usar el script `deploy.sh` para automatizar el despliegue:

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🛠️ Personalización

### Agregar Más Respuestas

Edita el diccionario `RESPUESTAS` en `app.py`:

```python
RESPUESTAS = {
    'nueva_emocion': [
        "Primera respuesta para esta emoción",
        "Segunda respuesta alternativa",
        "Tercera opción de respuesta"
    ],
    # ... más emociones
}
```

### Agregar Nuevas Palabras Clave

Edita el diccionario `PALABRAS_CLAVE` en `app.py`:

```python
PALABRAS_CLAVE = {
    'nueva_emocion': ['palabra1', 'palabra2', 'palabra3'],
    # ... más palabras
}
```

### Cambiar Colores de la Interfaz

Edita `static/style.css` para personalizar los colores:

```css
.chat-header {
    background: linear-gradient(135deg, #TU_COLOR1 0%, #TU_COLOR2 100%);
}
```

## 📊 Funcionalidades Técnicas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: RESTful endpoint `/chat` para procesamiento de mensajes
- **Detección**: Sistema de puntuación por palabras clave
- **Responsive**: Funciona en móviles, tablets y escritorio

## 🔒 Consideraciones de Seguridad

- Este chatbot NO reemplaza ayuda profesional
- Incluye mensaje de advertencia para situaciones de crisis
- Detecta desesperanza y sugiere buscar ayuda profesional
- No almacena conversaciones (privacidad por defecto)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Siéntete libre de:

- Reportar bugs
- Sugerir nuevas características
- Agregar más respuestas empáticas
- Mejorar la detección de emociones
- Traducir a otros idiomas

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Úsalo libremente para ayudar a las personas.

## 💙 Recursos de Ayuda

Si tú o alguien que conoces está en crisis:

- **España**: Teléfono de la Esperanza: 717 003 717
- **México**: SAPTEL: 55 5259 8121
- **Argentina**: Centro de Asistencia al Suicida: 135
- **Colombia**: Línea 106
- **Internacional**: https://findahelpline.com/

## 🙏 Agradecimientos

Creado con el objetivo de brindar un poco de luz a quienes lo necesitan. Si este chatbot ayuda aunque sea a una persona, habrá valido la pena.

---

**¡Que este pequeño chatbot pueda alegrar el día de alguien! 💙✨**
