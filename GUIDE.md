# 🚀 Guía Completa para Subir el ChatBot a PythonAnywhere

Esta guía te llevará paso a paso para desplegar tu ChatBot de Ánimo en PythonAnywhere y hacerlo accesible desde internet.

---

## 📋 Requisitos Previos

1. Cuenta en [PythonAnywhere](https://www.pythonanywhere.com/) (la cuenta gratuita funciona perfectamente)
2. Tu proyecto debe estar listo localmente
3. (Opcional) Cuenta de GitHub para facilitar la subida

---

## 🎯 Método 1: Subir Usando GitHub (Recomendado)

### Paso 1: Crear Repositorio en GitHub

```bash
# En tu carpeta del proyecto, inicializa Git
git init
git add .
git commit -m "Initial commit - ChatBot de Ánimo"

# Crea un repositorio en GitHub y conecta tu proyecto
git remote add origin https://github.com/TU_USUARIO/chatbot-animo.git
git branch -M main
git push -u origin main
```

### Paso 2: Clonar en PythonAnywhere

1. Inicia sesión en [PythonAnywhere](https://www.pythonanywhere.com/)
2. Ve a **"Consoles"** y abre una **"Bash Console"**
3. Clona tu repositorio:

```bash
git clone https://github.com/TU_USUARIO/chatbot-animo.git
cd chatbot-animo
```

### Paso 3: Crear Entorno Virtual e Instalar Dependencias

```bash
# Crear entorno virtual
python3.10 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🎯 Método 2: Subir Archivos Directamente

### Paso 1: Subir Archivos Manualmente

1. Ve a **"Files"** en PythonAnywhere
2. Crea una carpeta llamada `chatbot-animo`
3. Sube todos tus archivos:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - Carpeta `templates/` con `index.html`
   - Carpeta `static/` con `style.css` y `script.js`

### Paso 2: Crear Entorno Virtual

Abre una **Bash Console** y ejecuta:

```bash
cd chatbot-animo

# Crear entorno virtual
python3.10 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## ⚙️ Configurar la Aplicación Web

### Paso 1: Crear Web App

1. Ve a la pestaña **"Web"**
2. Haz clic en **"Add a new web app"**
3. Selecciona **"Manual configuration"**
4. Elige **Python 3.10** (o la versión más reciente disponible)

### Paso 2: Configurar WSGI

1. En la sección **"Code"**, haz clic en el archivo **WSGI configuration file**
2. **BORRA TODO** el contenido del archivo
3. Reemplázalo con esto (ajusta TU_USUARIO):

```python
import sys
import os

# Reemplaza 'TU_USUARIO' con tu nombre de usuario de PythonAnywhere
project_home = '/home/TU_USUARIO/chatbot-animo'

if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Activar el entorno virtual
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application
```

4. Guarda el archivo (Ctrl + S o botón "Save")

### Paso 3: Configurar Entorno Virtual

1. En la sección **"Virtualenv"**, ingresa la ruta completa:
   ```
   /home/TU_USUARIO/chatbot-animo/venv
   ```
2. Haz clic en la marca de verificación ✓

### Paso 4: Configurar Archivos Estáticos

En la sección **"Static files"**, agrega:

| URL            | Directory                                          |
|----------------|---------------------------------------------------|
| `/static/`     | `/home/TU_USUARIO/chatbot-animo/static`          |

### Paso 5: Recargar la Aplicación

1. Ve al inicio de la página **"Web"**
2. Haz clic en el botón verde **"Reload TU_USUARIO.pythonanywhere.com"**

---

## 🌐 Acceder a Tu ChatBot

Tu aplicación estará disponible en:
```
https://TU_USUARIO.pythonanywhere.com
```

Por ejemplo, si tu usuario es `maria123`, será:
```
https://maria123.pythonanywhere.com
```

---

## 🔧 Script Bash Automatizado (Opcional)

Crea un archivo `deploy.sh` para automatizar el despliegue:

```bash
#!/bin/bash

# Script de despliegue para PythonAnywhere
# Ejecutar en la Bash Console de PythonAnywhere

echo "🚀 Iniciando despliegue del ChatBot de Ánimo..."

# Variables (CAMBIA ESTAS)
USUARIO="TU_USUARIO"
REPO_URL="https://github.com/TU_USUARIO/chatbot-animo.git"
PROJECT_DIR="/home/$USUARIO/chatbot-animo"

# Clonar o actualizar repositorio
if [ -d "$PROJECT_DIR" ]; then
    echo "📦 Actualizando repositorio..."
    cd $PROJECT_DIR
    git pull origin main
else
    echo "📦 Clonando repositorio..."
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🐍 Creando entorno virtual..."
    python3.10 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Despliegue completado!"
echo "🌐 Recuerda recargar tu app en: https://www.pythonanywhere.com/user/$USUARIO/webapps/"
```

Para usar el script:

```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 🔍 Verificación y Troubleshooting

### Verificar que Todo Funciona

1. **Logs de Error**: Ve a **"Web"** → **"Log files"** → **"Error log"**
2. **Consola de Bash**: Prueba la app localmente:
   ```bash
   cd chatbot-animo
   source venv/bin/activate
   python app.py
   ```

### Problemas Comunes

#### Error 404 - No se encuentra la página
- Verifica que el archivo WSGI esté configurado correctamente
- Asegúrate de que la ruta del proyecto sea correcta
- Recarga la aplicación web

#### Error 500 - Error del servidor
- Revisa el **Error log** en la pestaña "Web"
- Verifica que todas las dependencias estén instaladas
- Comprueba que los archivos `templates/` y `static/` estén en su lugar

#### La aplicación no carga los estilos
- Verifica la configuración de archivos estáticos
- Asegúrate de que la carpeta `static/` esté correctamente ubicada
- Recarga la aplicación

#### ImportError o ModuleNotFoundError
```bash
# En Bash Console
cd chatbot-animo
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

## 🔄 Actualizar la Aplicación

Cuando hagas cambios:

### Si usas GitHub:
```bash
# En Bash Console de PythonAnywhere
cd chatbot-animo
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # Si hay nuevas dependencias
```

Luego recarga la app en la pestaña "Web".

### Si subes manualmente:
1. Sube los archivos modificados en la pestaña "Files"
2. Recarga la aplicación en la pestaña "Web"

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real
```bash
# En Bash Console
tail -f /var/log/TU_USUARIO.pythonanywhere.com.error.log
```

### Ver Accesos
```bash
tail -f /var/log/TU_USUARIO.pythonanywhere.com.access.log
```

---

## 🎉 ¡Listo!

Tu ChatBot de Ánimo ahora está en línea y accesible desde cualquier lugar del mundo. Comparte el enlace con quienes puedan necesitar un poco de ánimo.

### Funcionalidades Implementadas:
- ✅ Detección de 13 emociones diferentes
- ✅ Respuestas personalizadas y empáticas
- ✅ Interfaz moderna y responsive
- ✅ Indicador visual de emoción detectada
- ✅ Animaciones suaves
- ✅ Indicador de escritura
- ✅ Advertencia de crisis

### Próximos Pasos (Opcionales):
- 🔒 Agregar HTTPS (incluido gratis en PythonAnywhere)
- 📊 Agregar analytics básicos
- 🌍 Agregar más idiomas
- 💾 Guardar historial de conversaciones (opcional)
- 🤖 Integrar IA más avanzada (OpenAI, etc.)

---

## 📞 Recursos Adicionales

- [Documentación de PythonAnywhere](https://help.pythonanywhere.com/)
- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Foro de PythonAnywhere](https://www.pythonanywhere.com/forums/)

**¡Mucho éxito con tu proyecto! 💙**
