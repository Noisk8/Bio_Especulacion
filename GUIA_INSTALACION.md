# 📚 Guía Completa de Instalación

## 🖥️ Tabla de Contenidos
1. [Instalación en Windows](#-instalación-en-windows)
2. [Instalación en macOS](#-instalación-en-macos)
3. [Instalación en Linux](#-instalación-en-linux)
4. [Verificación de la Instalación](#-verificación-de-la-instalación)
5. [Solución de Problemas Comunes](#-solución-de-problemas-comunes)
6. [Configuración del Entorno de Desarrollo](#-configuración-del-entorno-de-desarrollo)

---

## 🪟 Instalación en Windows

### 1. Instalar Python
1. **Descargar Python**:
   - Ve a [python.org/downloads](https://www.python.org/downloads/)
   - Haz clic en "Download Python" (versión 3.10 o superior)
   
2. **Ejecutar el instalador**:
   - Marca la casilla "Add Python to PATH" (IMPORTANTE)
   - Haz clic en "Install Now"
   - Marca "Disable path length limit" al final de la instalación

3. **Verificar la instalación**:
   - Presiona `Win + R`, escribe `cmd` y presiona Enter
   - Ejecuta:
     ```
     python --version
     pip --version
     ```
   - Deberías ver las versiones instaladas

### 2. Instalar FFmpeg

#### Opción A: Usando Chocolatey (recomendado)
1. **Instalar Chocolatey**:
   - Abre PowerShell como Administrador
   - Ejecuta:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
     ```
   - Cierra y vuelve a abrir PowerShell

2. **Instalar FFmpeg**:
   ```powershell
   choco install ffmpeg
   ```

#### Opción B: Instalación Manual
1. **Descargar FFmpeg**:
   - Ve a [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)
   - Descarga "ffmpeg-release-essentials.7z"
   
2. **Extraer archivos**:
   - Usa 7-Zip para extraer el archivo descargado
   - Copia la carpeta `ffmpeg-x.x.x-essentials_build\bin` a `C:\ffmpeg`
   
3. **Configurar PATH**:
   - Busca "Variables de entorno" en el menú de inicio
   - Haz clic en "Variables de entorno"
   - En "Variables del sistema", selecciona "Path" → "Editar"
   - Haz clic en "Nuevo" y agrega `C:\ffmpeg\bin`
   - Haz clic en "Aceptar" en todas las ventanas

---

##  Instalación en macOS

### 1. Instalar Homebrew
1. Abre Terminal (Aplicaciones → Utilidades → Terminal)
2. Ejecuta:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Sigue las instrucciones en pantalla
4. Al finalizar, ejecuta los comandos que te indique para agregar Homebrew al PATH

### 2. Instalar Python y FFmpeg
```bash
# Actualizar Homebrew
brew update

# Instalar Python
brew install python

# Instalar FFmpeg
brew install ffmpeg
```

### 3. Verificar instalaciones
```bash
python3 --version
pip3 --version
ffmpeg -version
```

---

## 🐧 Instalación en Linux (Ubuntu/Debian)

### 1. Actualizar paquetes
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalar Python y herramientas de desarrollo
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev
```

### 3. Instalar FFmpeg
```bash
sudo apt install -y ffmpeg
```

### 4. Verificar instalaciones
```bash
python3 --version
pip3 --version
ffmpeg -version
```

---

## ✅ Verificación de la Instalación

### Verificar Python y pip
```bash
# En Windows
python --version
pip --version

# En macOS/Linux
python3 --version
pip3 --version
```

### Verificar FFmpeg
```bash
ffmpeg -version
```

### Instalar dependencias de Python
```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar paquetes necesarios
pip install --upgrade pip
pip install pillow imageio numpy requests tqdm opencv-python
```

---

## 🐛 Solución de Problemas Comunes

### 1. "No se reconoce 'python' como un comando"
- Verifica que Python esté en el PATH
- En Windows, reinstala Python marcando "Add Python to PATH"
- En Linux/macOS, usa `python3` en lugar de `python`

### 2. Errores de permisos
Si ves errores como "Permission denied":
- En Windows: Ejecuta la terminal como administrador
- En Linux/macOS: Usa `sudo` o instala en un entorno virtual

### 3. FFmpeg no funciona
- Verifica que esté en el PATH
- Prueba reiniciando la terminal
- En Windows, asegúrate de haber cerrado y vuelto a abrir el símbolo del sistema después de instalar

### 4. Problemas con pip
Si `pip` no funciona, intenta:
```bash
python -m pip install --upgrade pip
```

---
