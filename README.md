# **Bio_Especulación 🍁🌴🪴**

### Requerimientos 

* una cuenta de [**Gmail**](https://mail.google.com/mail/u/0/#inbox) (Con más dee 5 GB de espcio en el drive)

* Una cuenta de [**Hugging Face**](https://huggingface.co/)

* [**Token de Huging Face**](https://huggingface.co/settings/tokens)

* [**Python**](https://www.python.org/)

* [**Ffmpeg**](https://ffmpeg.org/)



## Proceso de Fine - Tuning 

🌋 Descargar un lote de fotos de [**Biodiversidad en Colombia**](https://commons.wikimedia.org/wiki/Campaign:Biodiversidad_en_Colombia_2025) 
Elije las que más te gusten, con las que quieras crear tus personajes espcultavos, _este sera el material con el que nuestro modelo de va entrenar para, es decir con el que va tomar como referencia para generar las imagenes_

Guardalas en una carpeta 🗂️

Lo recomendado es convertir las imagenes a un tamaño homogeniozado, por ejemplo **500 x 500**, para hacer esto en lote, te recomendamos usar este [**Script Redimensionador**](https://github.com/Noisk8/Bio_Especulacion/Tools/Redimensionar.py) escrito en **python** que utiliza la libreria [**ffmpeg**](https://ffmpeg.org/) 


#### Linux 🐧

~~~
wget https://github.com/Noisk8/Bio_Especulacion/Tools/Redimensionar.py

chmod +x Redimensionar.py
~~~


### Windows 🪟





## Entrenamiento del Molde 🧗‍♀️

[**BiodiversidadColombiana.ipynb**](https://colab.research.google.com/drive/1wtAYBG3Org3mpgXFheY24tf15yTWYOge?authuser=1#scrollTo=-8JWf-fxfGka)

Para Entrenar nuestro molde Vamos a usando LoRA para ahorro de memoria, y un molde base de Stable Difussion 

Cargamos el resuoltado del entrenamiento .ckpt y lo ponemos en el drive e una carpetra que recuerdes 




## Creación de Animación 

[Deforum Stable Difusion](https://colab.research.google.com/github/deforum-art/deforum-stable-diffusion/blob/main/Deforum_Stable_Diffusion.ipynb#scrollTo=232_xKcCfIj9)

Dentro del Colab vamos a llamar el molde que entrenamos 

~~~
models_path_gdrive: /content/drive/MyDrive/AI/models{carpeta donde está la carpeta}
~~~

~~~
model_checkpoint: Custom 
~~~

~~~
custom_config_path: /content/drive/MyDrive/AI/models/{ruta ezacta del molde}
~~~


