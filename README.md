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

### 📂 ¿Por qué trabajar con archivos abiertos como el de Wikimedia Commons?

Este proyecto se basa en un conjunto de más de 1300 imágenes de biodiversidad colombiana con licencias abiertas, alojadas en [Wikimedia Commons](https://commons.wikimedia.org/). Usar un dataset abierto no es solo una decisión técnica: es una postura.

Trabajar con archivos abiertos significa:

- 🧭 **Reapropiarse de los datos públicos**: Estamos usando imágenes construidas colectivamente y disponibles libremente para crear nuevas narrativas visuales.
- 🌎 **Ampliar el acceso y la redistribución**: Cualquier persona puede reutilizar, modificar y seguir experimentando con este archivo. No hay barreras ni permisos restrictivos.
- 💥 **Descentralizar la imaginación de la IA**: En lugar de entrenar modelos con imágenes genéricas o controladas por grandes plataformas, usamos contenido local, diverso y común.
- 🫱🏼‍🫲🏽 **Hacer comunidad desde los datos**: Lo abierto permite que lo que hacemos sea compartido, expandido, comentado, criticado y mejorado por otrxs.

Este archivo no es solo una colección de fotos: es un campo fértil para la creación, la pedagogía y la especulación desde el sur global. Entrenar una IA con estas imágenes es también un acto de imaginación política.

> 🌱 *La biodiversidad como código abierto para imaginar nuevas formas de vida.*


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

## Entrenamiento del Molde 🧗‍♀️

> [**🌋NOTA**]  
> Antes de ejecutar el Notebook debes tener  varias cosas listas 
> * Crea una carpeta 🗂️ llamada **Dreambooth_Bio** en el drive
> * Guarda las imagenes redimensionadas en la carpeta 🗂️ llamada **Dreambooth_Bio** en el drive
> * Crea el token 📝  token de hugging face, el token debe de ser con persmisos de ecritura


## [**📝Notebook**]([https://colab.research.google.com/drive/1wtAYBG3Org3mpgXFheY24tf15yTWYOge?authuser=1#scrollTo=-8JWf-fxfGka](https://colab.research.google.com/drive/1iXGiuIEBOjnSvb52b40Vkbdn0LO0RCR2?usp=sharing))









