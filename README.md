# **Bio_Especulación 🍁🌴🪴🐫🐑🐦‍🔥🦎🦠🌲🪴**

### Requerimientos 

* una cuenta de [**Gmail**](https://mail.google.com/mail/u/0/#inbox) (Con más dee 5 GB de espcio en el drive)

* Una cuenta de [**Hugging Face**](https://huggingface.co/)

* [**Token de Huging Face**](https://huggingface.co/settings/tokens)

* [**Python**](https://www.python.org/)

* [**Ffmpeg**](https://ffmpeg.org/)

### 🤔 ¿Por qué entrenar un modelo en lugar de usar Midjourney?

Aunque herramientas como Midjourney generan imágenes sorprendentes, este taller propone algo diferente: **entrenar nuestro propio modelo con imágenes de biodiversidad colombiana de acceso abierto**.

Esto nos permite:

- 🌱 **Crear desde nuestros propios archivos**, no desde una base de datos cerrada.
- 🧠 **Comprender cómo la inteligencia artificial construye una imagen**, no solo usarla como caja negra.
- 🧬 **Explorar estéticas nuevas y especulativas**, basadas en mezclas inesperadas de plantas, animales y formas naturales locales.
- 🔓 **Liberar el modelo entrenado**, para que otros puedan seguir creando con él.

Aquí **la imagen no es el fin, sino el medio** para experimentar con archivos abiertos, procesos de aprendizaje automático y creación colectiva.


## **Proceso de Fine - Tuning ⚙️**

🌋 Descargar un lote de fotos de [**Biodiversidad en Colombia**](https://commons.wikimedia.org/wiki/Campaign:Biodiversidad_en_Colombia_2025) 
Elije las que más te gusten, con las que quieras crear tus personajes espcultavos, _este sera el material con el que nuestro modelo de va entrenar para, es decir con el que va tomar como referencia para generar las imagenes_

Guardalas en una carpeta 🗂️

> [**🌋NOTA**]  
> Minimo **10 Fotos** 

Lo recomendado es convertir las imagenes a un tamaño homogeniozado, por ejemplo **500 x 500**, para hacer esto en lote, te recomendamos usar este [**Script Redimensionador**](https://github.com/Noisk8/Bio_Especulacion/Tools/Redimensionar.py) escrito en **python** que utiliza la libreria [**ffmpeg**](https://ffmpeg.org/) 


#### Linux 🐧



#### Decargar archivos 

~~~
wget https://raw.githubusercontent.com/Noisk8/Bio_Especulacion/refs/heads/main/Tools/Descargar_Archivos.py

chmod +x Descargar_Archivos.py

python Descargar_Archivos.py
~~~

#### Redimencionar Archivos 


~~~
wget https://raw.githubusercontent.com/Noisk8/Bio_Especulacion/refs/heads/main/Tools/Redimensionar.py

chmod +x Redimensionar.py

python Redimensionar.py
~~~




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


## Entrenamiento del Molde 🧗‍♀️

> [**🌋NOTA**]  
> Antes de ejecutar el Notebook debes tener  varias cosas listas 
> * Crea una carpeta 🗂️ llamada **Dreambooth_Bio** en el drive
> * Guarda las imagenes redimensionadas en la carpeta 🗂️ llamada **Dreambooth_Bio** en el drive
> * Crea el token 📝  token de hugging face, el token debe de ser con persmisos de ecritura


## [**📝Notebook**](https://colab.research.google.com/drive/1wtAYBG3Org3mpgXFheY24tf15yTWYOge?authuser=1#scrollTo=-8JWf-fxfGka)









