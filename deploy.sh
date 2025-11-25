#!/bin/bash

# Script de despliegue para PythonAnywhere
# Ejecutar en la Bash Console de PythonAnywhere después de modificar las variables

# ========================================
# CONFIGURA ESTAS VARIABLES
# ========================================
USUARIO="chatbotpsicologia"  # Cambia esto por tu usuario de PythonAnywhere
REPO_URL="https://github.com/LouisRequejo/Nueva-carpeta.git"  # URL de tu repositorio
PROJECT_NAME="chatbot-animo"
PYTHON_VERSION="python3.9"

# ========================================
# NO MODIFICAR DESDE AQUÍ
# ========================================
PROJECT_DIR="/home/$USUARIO/$PROJECT_NAME"

echo "🚀 ============================================"
echo "   CHATBOT DE ÁNIMO - SCRIPT DE DESPLIEGUE"
echo "   ============================================"
echo ""

# Verificar si el directorio del proyecto existe
if [ -d "$PROJECT_DIR" ]; then
    echo "📦 Actualizando repositorio existente..."
    cd $PROJECT_DIR
    git pull origin main
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al actualizar el repositorio"
        exit 1
    fi
else
    echo "📦 Clonando repositorio por primera vez..."
    git clone $REPO_URL $PROJECT_DIR
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al clonar el repositorio"
        echo "💡 Verifica que la URL del repositorio sea correcta"
        exit 1
    fi
    
    cd $PROJECT_DIR
fi

echo "✅ Repositorio actualizado"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🐍 Creando entorno virtual..."
    $PYTHON_VERSION -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual"
        exit 1
    fi
    
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

echo ""

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar/actualizar dependencias
echo "📚 Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo "✅ Dependencias instaladas correctamente"
echo ""

# Verificar estructura de carpetas
echo "🔍 Verificando estructura del proyecto..."

if [ ! -d "templates" ]; then
    echo "⚠️  Advertencia: Carpeta 'templates' no encontrada"
else
    echo "✅ Carpeta templates/ existe"
fi

if [ ! -d "static" ]; then
    echo "⚠️  Advertencia: Carpeta 'static' no encontrada"
else
    echo "✅ Carpeta static/ existe"
fi

if [ ! -f "app.py" ]; then
    echo "❌ Error: archivo app.py no encontrado"
    exit 1
else
    echo "✅ Archivo app.py existe"
fi

if [ ! -f "wsgi.py" ]; then
    echo "⚠️  Advertencia: archivo wsgi.py no encontrado"
else
    echo "✅ Archivo wsgi.py existe"
fi

echo ""
echo "🎉 ============================================"
echo "   DESPLIEGUE COMPLETADO EXITOSAMENTE"
echo "   ============================================"
echo ""
echo "📋 SIGUIENTES PASOS:"
echo ""
echo "1. Ve a la pestaña 'Web' en PythonAnywhere"
echo "2. Si es la primera vez:"
echo "   - Crea una nueva web app (Manual configuration)"
echo "   - Configura el archivo WSGI"
echo "   - Configura el virtualenv: $PROJECT_DIR/venv"
echo "   - Configura archivos estáticos: /static/ -> $PROJECT_DIR/static"
echo ""
echo "3. Haz clic en 'Reload $USUARIO.pythonanywhere.com'"
echo ""
echo "🌐 Tu aplicación estará disponible en:"
echo "   https://$USUARIO.pythonanywhere.com"
echo ""
echo "📊 Para ver logs de errores:"
echo "   tail -f /var/log/$USUARIO.pythonanywhere.com.error.log"
echo ""
echo "✨ ¡Tu ChatBot de Ánimo está listo para ayudar a las personas! 💙"
echo ""
