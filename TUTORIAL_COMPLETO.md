# 🦜 Tutorial Completo: Biodiversidad Especulativa de Colombia con Notebooks

## 📋 Tabla de Contenidos
1. [Introducción](#-introducción)
2. [Requisitos del Sistema](#-requisitos-del-sistema)
3. [Configuración Inicial](#-configuración-inicial)
4. [Uso del Notebook Principal](#-uso-del-notebook-principal)
5. [Generación de Imágenes](#-generación-de-imágenes)
6. [Creación de Animaciones](#-creación-de-animaciones)
7. [Solución de Problemas](#-solución-de-problemas)

## 🌟 Introducción
¡Bienvenido al proyecto de Biodiversidad Especulativa de Colombia! Este tutorial te guiará a través del proceso completo utilizando notebooks de Jupyter/Colab para crear criaturas imaginarias basadas en la biodiversidad colombiana.

## 💻 Requisitos del Sistema
- **Navegador Web**: Chrome, Firefox o Edge actualizado
- **Cuenta de Google**: Para usar Google Colab
- **Almacenamiento en Google Drive**: 15GB de espacio libre
- **Conexión a Internet**: Estable, mínimo 10Mbps

> 💡 No se requiere hardware potente ya que usaremos Google Colab con GPU gratuita

## ⚙️ Configuración Inicial

### 1. Preparar Google Drive
1. Ve a [Google Drive](https://drive.google.com)
2. Crea una carpeta llamada `Dreambooth_Bio`


### 2. Descargar Imagenes

Abre una terminal 

 ```bash
 python3 Tools/Descargar_Archivos.py
 ```


#### 2.1 Uso del Script de Redimensionamiento
El script `Tools/Redimensionar.py` procesa imágenes usando FFmpeg. Requiere FFmpeg instalado en el sistema.

**Sintaxis básica:**
```bash
python3 Tools/Redimensionar.py 
```

**Parámetros:**
- `--input`: (Opcional) Ruta a la carpeta con imágenes de entrada (por defecto: `biodiversidad_colombia/`)
- `--output`: (Opcional) Ruta para guardar imágenes redimensionadas (por defecto: `biodiversidad_colombia_500x500/`)
- `--width`: (Opcional) Ancho en píxeles (por defecto: 500)
- `--height`: (Opcional) Alto en píxeles (por defecto: 500)

**Ejemplo de uso:**
```bash
# Redimensionar a 500x500 píxeles (valores por defecto)
python Tools/Redimensionar.py

# Especificar carpetas personalizadas
python Tools/Redimensionar.py --input mis_imagenes --output imagenes_procesadas

# Especificar dimensiones personalizadas
python Tools/Redimensionar.py --width 800 --height 600
```

**Características:**
- Soporta formatos: .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp
- Mantiene la relación de aspecto original
- Calidad de compresión alta por defecto
- Muestra progreso detallado
- Manejo de errores integrado

**Requisitos previos:**
- Python 3.6+
- FFmpeg instalado y accesible desde la línea de comandos
- Permisos de escritura en la carpeta de salida

> 💡 Las imágenes procesadas se guardarán en `data/processed` listas para el entrenamiento.

### 3. Preparar las Imágenes para el Entrenamiento

1. Verifica que las imágenes estén en la carpeta `data/processed`
2. Las imágenes deben estar en formato JPG o PNG
3. Tamaño recomendado: 512x512 píxeles
4. Nombra las imágenes de manera descriptiva (ej: `rana_dorada_01.jpg`)

### 4. Acceder al Notebook
1. Abre el notebook en Google Colab:
   - [BiodiversidadColombiana.ipynb](https://colab.research.google.com/github/tu-usuario/biodiversidad-colombiana/blob/main/BiodiversidadColombiana.ipynb)
2. Haz clic en "Copiar en Drive" para guardar una copia en tu Google Drive

## 📓 Uso del Notebook Principal

### 1. Configuración Inicial
1. En la primera celda, conecta Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
   - Sigue el enlace para autenticarte
   - Copia el código de verificación en el cuadro

2. Configura las rutas (segunda celda):
   ```python
   # Ruta a tu carpeta en Google Drive
   dataset_dir = '/content/drive/MyDrive/Dreambooth_Bio/input_images'
   output_dir = '/content/drive/MyDrive/Dreambooth_Bio/output'
   ```

### 2. Instalación de Dependencias
Ejecuta la celda de instalación que incluye:
- Diffusers
- Transformers
- Aceleración de GPU
- Otras dependencias necesarias

### 3. Cargar y Preprocesar Imágenes
1. El notebook verificará automáticamente las imágenes en tu carpeta
2. Aplicará redimensionamiento a 512x512 píxeles
3. Mostrará un resumen de las imágenes cargadas

### 4. Configuración del Entrenamiento
Ajusta estos parámetros según necesites:
```python
{
    "learning_rate": 1e-6,           # Tasa de aprendizaje
    "max_train_steps": 1000,         # Número de pasos de entrenamiento
    "train_batch_size": 1,           # Tamaño de lote (reducir si hay errores de memoria)
    "gradient_accumulation_steps": 4, # Acumulación de gradientes
    "resolution": 512,               # Resolución de las imágenes
    "mixed_precision": "fp16",       # Precisión mixta para ahorrar memoria
    "use_8bit_adam": True           # Optimizador 8-bit para ahorrar memoria
}
```

## 🚀 Iniciar el Entrenamiento

### 1. Ejecutar el Entrenamiento
1. Desplázate a la sección "Entrenamiento del Modelo"
2. Ejecuta la celda de entrenamiento
3. El progreso se mostrará con una barra de progreso

### 2. Monitoreo
- El notebook mostrará:
  - Pérdida de entrenamiento
  - Tiempo por paso
  - Uso de memoria
- Se guardarán checkpoints automáticamente

## 🎨 Generación de Imágenes

### 1. Usar el Notebook de Generación
1. Abre el notebook de generación:
   - [BiodiversidadColombiana_Generacion.ipynb](enlace-al-notebook)
2. Conecta Google Drive como antes

### 2. Cargar el Modelo Entrenado
```python
# Ruta a tu modelo entrenado
model_path = "/content/drive/MyDrive/Dreambooth_Bio/modelo_entrenado"

# Cargar el pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    torch_dtype=torch.float16
).to("cuda")
```

### 3. Interfaz de Generación
Ejecuta la celda con la interfaz de widgets para:
- Escribir prompts descriptivos
- Ajustar parámetros:
  - Número de imágenes
  - Pasos de inferencia
  - Escala de guía
  - Semilla aleatoria

### 4. Ejemplos de Prompts
```
"Una criatura mágica con plumas de colores brillantes y alas de mariposa, fotografía macro detallada"
"Animal fantástico de la selva amazónica con piel de anfibio y cuernos de ciervo, iluminación dramática"
"Ser mitológico colombiano con características de orquídea y colibrí, estilo realista"
```

## 🎥 Creación de Animaciones

### 1. Usar el Notebook de Animación
1. Abre el notebook:
   - [BiodiversidadColombiana_Animacion.ipynb](enlace-al-notebook-animacion)
2. Sigue los pasos para:
   - Cargar imágenes generadas
   - Crear secuencias de animación
   - Exportar como GIF o video

### 2. Parámetros de Animación
- **Fotogramas por segundo (FPS)**: 24 para fluidez
- **Transiciones**: Suaves entre imágenes
- **Duración**: Ajustable según necesidades

### 3. Exportar Resultados
- Guarda las animaciones directamente en Google Drive
- Formatos soportados: GIF, MP4
- Resolución ajustable hasta 1024x1024px

## 🐛 Solución de Problemas Comunes

### 1. Error: "CUDA out of memory"
- Reduce el batch size a 1
- Usa `fp16` en la configuración
- Reinicia el entorno de ejecución

### 2. Google Colab se desconecta
- Guarda checkpoints frecuentemente
- Usa este código para reconectar automáticamente:
  ```python
  from google.colab import output
  
  def reconnect():
      print("Reconectando...")
      output.eval_js('google.colab.kernel.reconnect()')
  
  # Usar en celdas largas
  !sleep 300 && python -c "from google.colab import output; output.eval_js('google.colab.kernel.reconnect()')" &
  ```

### 3. Imágenes de baja calidad
- Aumenta los pasos de inferencia (50-100)
- Usa prompts más detallados
- Ajusta la escala de guía (7-9 es un buen rango)

### 4. Problemas con Google Drive
- Verifica los permisos de la carpeta
- Si falla la conexión, ejecuta de nuevo la celda de montaje
- Usa IDs de carpeta en lugar de rutas completas si es necesario

## 📚 Recursos Adicionales

### Documentación Oficial
- [🤗 Diffusers](https://huggingface.co/docs/diffusers/index)
- [DreamBooth Guide](https://huggingface.co/docs/diffusers/training/dreambooth)
- [Google Colab Tips](https://research.google.com/colaboratory/faq.html)

### Comunidad y Soporte
- [Foro de Hugging Face](https://discuss.huggingface.co/)
- [Subreddit de Stable Diffusion](https://www.reddit.com/r/StableDiffusion/)
- [Discord de IA Generativa](https://discord.gg/generative-ai)

### Mejores Prácticas
- Usa prompts detallados y específicos
- Experimenta con diferentes semillas aleatorias
- Guarda múltiples versiones de tus mejores resultados

¡Feliz creación de biodiversidad especulativa! 🌈🦜🌿

> 💡 ¿Neitas más ayuda? Abre un issue en nuestro [repositorio](https://github.com/tu-usuario/biodiversidad-colombiana) o únete a nuestra comunidad.
