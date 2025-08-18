# 📚 Guía Completa de Instalación

## 🖥️ Tabla de Contenidos
1. [Instalación en Windows](#-instalación-en-windows)
2. [Instalación en macOS](#-instalación-en-macos)
3. [Instalación en Linux](#-instalación-en-linux)
4. [Verificación de la Instalación](#-verificación-de-la-instalación)
5. [Solución de Problemas Comunes](#-solución-de-problemas-comunes)
6. [Configuración del Entorno de Desarrollo](#-configuración-del-entorno-de-desarrollo)

---
### Windows 🪟

🌋 Descargar un lote de fotos de [**Biodiversidad en Colombia**](https://commons.wikimedia.org/wiki/Campaign:Biodiversidad_en_Colombia_2025) 
La opción anterior sugiere la descarga manual, para hacer descargas automáticas usa el siguiente tutorial (recomendado para después de hacer pruebas, para tener datasets más grandes y poderlos asociar con metadata importante como el nombre de los autores)

✅ [**Requisitos previos**]
[**Tener Python instalado**](https://github.com/Noisk8/Bio_Especulacion/blob/main/GUIA_INSTALACION.md#-instalaci%C3%B3n-en-windows)

🧾 Paso a paso para usar el script en Windows

🟩 [**1. Crea una carpeta para tu proyecto**]
Por ejemplo:
~~~
C:\Users\TU_USUARIO\Documentos\BioEspeculacion\

~~~
Guarda ahí el archivo descargar.py (puedes ponerle el nombre que quieras). 

🟩 [**2. Abre la terminal (PowerShell o CMD)**]
Presiona Win + R, escribe cmd y dale Enter.
O busca "PowerShell" en el menú de inicio.

Navega hasta tu carpeta:
~~~
cd "C:\Users\TU_USUARIO\Documentos\BioEspeculacion"

~~~

🟩 [**3. Instala las librerías necesarias**]
Ejecuta esto en tu terminal:
~~~
pip install requests

~~~

🟩 [**3. 4. Ejecuta el script**]
Ahora ejecuta tu script:
~~~
python descargar.py

~~~
(usa el nombre exacto del archivo que guardaste)
Revisar que en el código puedes cambiar el número de imágenes que quieres descargar y las palabras clave con las que quieres filtrar la búsqueda

Busca esta línea de código para cambiar el número de imágenes a descargar: 
~~~
# Descargar 50 imágenes aleatorias de la campaña específica
  downloader.download_from_biodiversity_campaign(num_images=50)

~~~

[**Recomendaciones adicionales**]
Si quieres pausar o continuar otro día, simplemente vuelve a ejecutar el script. No volverá a descargar imágenes que ya existen.

Puedes adaptar este script para descargar por categorías diferentes si cambias esta línea:
~~~
category = "Uploaded_via_Campaign:Biodiversidad_en_Colombia_2025"

~~~

🪄 PASO A PASO PARA REDIMENSIONAR LAS IMÁGENES EN WINDOWS
✅ [**1. Instala FFmpeg**] (si aún no lo tienes)
FFmpeg es un programa externo que este script usa para redimensionar imágenes. Solo necesitas instalarlo una vez.

🔧 [**Instrucciones:**]
1. Descarga FFmpeg para Windows desde:
👉 https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

2. Extrae el archivo ZIP (por ejemplo, en C:\ffmpeg)
3. Agrega C:\ffmpeg\bin al [**PATH**] de tu sistema:
   - Busca en el menú de inicio: “Editar las variables de entorno del sistema”
   - Abre y haz clic en "Variables de entorno"
   - En "Path", haz clic en "Editar" → "Nuevo" → pega: C:\ffmpeg\bin
   - Acepta todo y reinicia tu terminal (CMD o PowerShell)
💡 Si ya lo tenías instalado, abre CMD y ejecuta:
~~~
ffmpeg -version

~~~
Si ves información, ¡está listo! Es decir, si no te sale error alguno

✅ [**2. Prepara tu script de Python**]
1. Descarga el script llamado resizer.py
2. Guarda ese archivo dentro de la misma carpeta donde tienes tus imágenes descargadas, o donde quieras.

✅ [**3. Actualiza las rutas del script**]
Busca estas líneas y reemplaza las rutas por las que tienes en tu computadora Windows:
~~~
input_folder = "C:\\ruta\\a\\tu\\carpeta\\imagenes"  # Carpeta con imágenes originales
output_folder = "C:\\ruta\\a\\tu\\carpeta\\redimensionadas"  # Carpeta para imágenes redimensionadas

~~~
✅ Asegúrate de que la ruta de entrada contenga imágenes

✅ [**4. Ejecuta el script desde la terminal (CMD o PowerShell)**]
1. Abre la terminal
2. Navega hasta la carpeta donde guardaste resizer.py:
~~~
cd C:\Users\TU_USUARIO\Documentos\BioEspeculacion

~~~
3. Ejecuta el script:
~~~
python resizer.py

~~~

✅ [**5. ¡Listo! Revisa tu carpeta de salida**]
Verás algo como esto en la terminal:
~~~
[1/50] ✓ rana_colombiana.jpg redimensionada correctamente
...
¡Proceso completado! Las imágenes redimensionadas están en: C:/Users/Johana/...

~~~

✅ [**Resultado esperado**]
- Tus imágenes estarán en la carpeta imagenes_512 (o la que hayas definido)
- Todas tendrán dimensiones de 512 x 512 píxeles, listas para entrenar modelos como Stable Diffusion o DreamBooth
- Las originales se mantienen intactas

## 🪟 Instalación en Windows opción 2

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
