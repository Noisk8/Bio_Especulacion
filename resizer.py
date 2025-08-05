import os
import subprocess
import sys
from pathlib import Path

def resize_images_with_ffmpeg(input_folder, output_folder, width=512, height=512):
    """
    Redimensiona todas las imágenes de una carpeta usando FFmpeg
    
    Args:
        input_folder (str): Ruta de la carpeta con las imágenes originales
        output_folder (str): Ruta de la carpeta donde guardar las imágenes redimensionadas
        width (int): Ancho deseado en píxeles
        height (int): Alto deseado en píxeles
    """
    
    # Extensiones de imagen soportadas
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    # Crear carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Obtener lista de archivos de imagen
    input_path = Path(input_folder)
    image_files = [f for f in input_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"No se encontraron imágenes en la carpeta: {input_folder}")
        return
    
    print(f"Encontradas {len(image_files)} imágenes para redimensionar...")
    
    # Procesar cada imagen
    for i, image_file in enumerate(image_files, 1):
        input_path = str(image_file)
        output_path = os.path.join(output_folder, image_file.name)
        
        # Comando FFmpeg para redimensionar
        # -y: sobrescribir archivo de salida si existe
        # scale=512:512 redimensiona a 500x500 píxeles
        cmd = [
            'ffmpeg',
            '-y',  # Sobrescribir sin preguntar
            '-i', input_path,  # Archivo de entrada
            '-vf', f'scale={width}:{height}',  # Filtro de video para redimensionar
            '-q:v', '2',  # Calidad alta (1-31, menor número = mejor calidad)
            output_path  # Archivo de salida
        ]
        
        try:
            # Ejecutar comando FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[{i}/{len(image_files)}] ✓ {image_file.name} redimensionada correctamente")
            else:
                print(f"[{i}/{len(image_files)}] ✗ Error procesando {image_file.name}")
                print(f"Error: {result.stderr}")
                
        except FileNotFoundError:
            print("Error: FFmpeg no está instalado o no se encuentra en el PATH")
            print("Instala FFmpeg desde: https://ffmpeg.org/download.html")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado procesando {image_file.name}: {e}")
    
    print(f"\n¡Proceso completado! Las imágenes redimensionadas están en: {output_folder}")

def main():
    """Función principal del script"""
    
    # Configuración - Modifica estas rutas según tus necesidades
    input_folder = "C:\\Users\\johan\OneDrive\\Documents\\wikimedia_descarga_biodiversidad\\biodiversidad_colombia\\imagenes"  # Carpeta con imágenes originales
    output_folder = "C:\\Users\\johan\\OneDrive\\Documents\\wikimedia_descarga_biodiversidad\\DataSetBio512x512"    # Carpeta para imágenes redimensionadas
    
    # Dimensiones deseadas
    width = 512
    height = 512
    
    print("=== Script de Redimensionamiento de Imágenes con FFmpeg ===")
    print(f"Carpeta de entrada: {input_folder}")
    print(f"Carpeta de salida: {output_folder}")
    print(f"Tamaño objetivo: {width}x{height} píxeles")
    print("-" * 50)
    
    # Verificar que la carpeta de entrada existe
    if not os.path.exists(input_folder):
        print(f"Error: La carpeta '{input_folder}' no existe.")
        print("Crea la carpeta y coloca las imágenes que quieres redimensionar.")
        return
    
    # Redimensionar imágenes
    resize_images_with_ffmpeg(input_folder, output_folder, width, height)

if __name__ == "__main__":
    main()
