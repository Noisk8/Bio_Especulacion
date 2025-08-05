#!/usr/bin/env python3
"""
Script para descargar imágenes aleatorias de Wikimedia Commons
Enfocado en biodiversidad de Colombia
"""

import requests
import random
import os
import json
from urllib.parse import unquote
import time
from typing import List, Dict, Optional

class WikimediaDownloader:
    def __init__(self, download_dir: str = "biodiversidad_colombia"):
        self.base_url = "https://commons.wikimedia.org/w/api.php"
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BiodiversidadColombiaDownloader/1.0 (https://example.com/contact)',
            'Accept-Language': 'es-ES,es;q=0.9'
        })
       
        # Palabras clave para filtrar imágenes relevantes
        self.keywords = {
            'especies': [
                'colombia', 'biodiversidad', 'fauna', 'flora', 'especie', 'animal', 'planta',
                'ave', 'pájaro', 'mamífero', 'anfibio', 'reptil', 'insecto', 'mariposa', 'orquídea',
                'bosque', 'selva', 'amazónica', 'andina', 'páramo', 'chocó', 'caribe', 'pacífico',
                'orinoquía', 'amazonía', 'páramo', 'endémic', 'nativo', 'silvestre', 'natural',
                'conservación', 'ecosistema', 'hábitat', 'reserva', 'parque', 'nacional', 'protegido'
            ],
            'cientificos': [
                'colombi', 'and', 'tropical', 'rainforest', 'biodiversity', 'wildlife', 'nature',
                'bird', 'mammal', 'amphibian', 'reptile', 'insect', 'butterfly', 'orchid', 'plant',
                'forest', 'jungle', 'amazon', 'andean', 'cloud forest', 'choco', 'caribbean',
                'pacific', 'orinoquia', 'amazonia', 'paramo', 'endemic', 'native', 'wild',
                'conservation', 'ecosystem', 'habitat', 'reserve', 'park', 'national', 'protected'
            ]
        }
       
        # Crear directorios necesarios
        os.makedirs(self.download_dir, exist_ok=True)
       
    def search_images_by_category(self, category: str, limit: int = 500) -> List[Dict]:
        """
        Busca imágenes por categoría en Wikimedia Commons con soporte para paginación
        """
        print(f"Buscando imágenes en la categoría: {category}")
       
        all_images = []
        continue_params = {}
       
        # Configurar parámetros iniciales
        params = {
            'action': 'query',
            'format': 'json',
            'generator': 'categorymembers',
            'gcmtitle': f'Category:{category}',
            'gcmlimit': min(limit, 500),  # Máximo 500 por solicitud
            'gcmtype': 'file',  # Solo archivos
            'prop': 'imageinfo',
            'iiprop': 'url|extmetadata|size|mime',
            'iiextmetadatafilter': 'Categories|ImageDescription|DateTimeOriginal|Artist|LicenseShortName|ObjectName',
            'iiextmetadatalanguage': 'es',
            'iiextmetadatamultilang': 1
        }
       
        try:
            while True:
                # Combinar parámetros base con los de continuación (si existen)
                request_params = {**params, **continue_params}
               
                # Hacer la solicitud
                response = self.session.get(self.base_url, params=request_params, timeout=30)
                response.raise_for_status()
                data = response.json()
               
                # Procesar resultados
                if 'query' in data and 'pages' in data['query']:
                    # Agregar las imágenes de esta página
                    page_images = list(data['query']['pages'].values())
                    all_images.extend(page_images)
                   
                    # Verificar si hemos alcanzado el límite
                    if len(all_images) >= limit:
                        all_images = all_images[:limit]  # Cortar al límite solicitado
                        break
               
                # Verificar si hay más resultados
                if 'continue' in data:
                    continue_params = data['continue']
                else:
                    break
                   
                # Pequeña pausa para ser respetuoso con el servidor
                time.sleep(1)
           
            print(f"Encontradas {len(all_images)} imágenes en la categoría {category}")
            return all_images
               
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar imágenes en la categoría {category}: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error al decodificar la respuesta JSON: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado al buscar en la categoría {category}: {e}")
            return []
   
    def search_images_by_keyword(self, keyword: str, limit: int = 500) -> List[Dict]:
        """
        Busca imágenes por palabra clave
        """
        print(f"Buscando imágenes con palabra clave: {keyword}")
       
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': f'{keyword} filetype:bitmap|drawing',
            'srnamespace': 6,  # Solo archivos
            'srlimit': min(limit, 500)
        }
       
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
           
            if 'query' in data and 'search' in data['query']:
                return data['query']['search']
            else:
                print(f"No se encontraron imágenes para: {keyword}")
                return []
               
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar imágenes: {e}")
            return []
   
    def get_image_info(self, filename: str) -> Optional[Dict]:
        """
        Obtiene información detallada de una imagen
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': filename,
            'prop': 'imageinfo',
            'iiprop': 'url|size|metadata|extmetadata',
            'iiurlwidth': 1024  # Tamaño máximo de descarga
        }
       
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
           
            if 'query' in data and 'pages' in data['query']:
                page = next(iter(data['query']['pages'].values()))
                if 'imageinfo' in page:
                    return page['imageinfo'][0]
           
            return None
           
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener información de {filename}: {e}")
            return None
   
    def is_relevant_image(self, image_info: Dict) -> bool:
        """
        Verifica si una imagen es relevante según las palabras clave.
        Maneja estructuras de metadatos inesperadas de manera segura.
        """
        try:
            # Extraer metadatos de manera segura
            extmetadata = image_info.get('imageinfo', [{}])[0].get('extmetadata', {})
            if not extmetadata:
                return False
           
            # Función auxiliar para extraer texto de manera segura
            def safe_get_text(data, *keys, default=''):
                result = data
                for key in keys:
                    if isinstance(result, dict):
                        result = result.get(key, {})
                    else:
                        return default
                return str(result) if result is not None else default
           
            # Obtener texto para analizar de manera segura
            title = safe_get_text(extmetadata, 'ObjectName', 'value', default='').lower()
            description = safe_get_text(extmetadata, 'ImageDescription', 'value', default='').lower()
            categories = safe_get_text(extmetadata, 'Categories', 'value', default='').lower()
           
            # Si no hay metadatos útiles, asumir que no es relevante
            if not any([title, description, categories]):
                return False
           
            # Combinar todo el texto para buscar palabras clave
            text_to_analyze = f"{title} {description} {categories}".lower()
           
            # Verificar palabras clave en español
            for keyword in self.keywords['especies']:
                if keyword and keyword.lower() in text_to_analyze:
                    return True
                   
            # Verificar palabras clave en inglés
            for keyword in self.keywords['cientificos']:
                if keyword and keyword.lower() in text_to_analyze:
                    return True
                   
            # Si no se encontraron palabras clave relevantes
            return False
           
        except Exception as e:
            print(f"Error al analizar metadatos: {str(e)[:100]}...")
            return False
       
    def create_descriptive_filename(self, image_info: Dict, filename: str) -> str:
        """
        Crea un nombre descriptivo para la imagen basado en metadatos
        """
        import re
       
        # Obtener descripción de los metadatos
        description = ""
        if 'extmetadata' in image_info:
            # Intentar obtener descripción de diferentes campos
            desc_fields = ['ImageDescription', 'ObjectName', 'Title']
            for field in desc_fields:
                if field in image_info['extmetadata']:
                    desc_value = image_info['extmetadata'][field].get('value', '')
                    if desc_value:
                        description = desc_value
                        break
       
        # Limpiar HTML tags si existen
        description = re.sub(r'<[^>]+>', '', description)
       
        # Si no hay descripción, usar el nombre del archivo
        if not description:
            description = filename.replace('File:', '').replace('.jpg', '').replace('.png', '').replace('.jpeg', '')
       
        # Extraer palabras clave relevantes
        keywords = []
       
        # Palabras clave en español e inglés para fauna y flora
        species_keywords = {
            # Anfibios
            'rana': 'rana', 'frog': 'rana', 'sapo': 'sapo', 'toad': 'sapo', 'anura': 'rana', 'bufonidae': 'sapo',
            'dendrobatidae': 'ranadardo', 'dendrobates': 'ranadardo', 'atelopus': 'sapito_arlequin', 'centrolenidae': 'ranacristal',
           
            # Aves
            'bird': 'ave', 'pajaro': 'ave', 'pájaro': 'ave', 'ave': 'ave', 'aves': 'ave', 'trochilidae': 'colibri',
            'colibri': 'colibri', 'hummingbird': 'colibri', 'ramphastos': 'tucan', 'toucan': 'tucan', 'tucan': 'tucan',
            'ara': 'guacamayo', 'macaw': 'guacamayo', 'guacamayo': 'guacamayo', 'pionus': 'loro', 'parrot': 'loro',
            'amazona': 'loro', 'psittacidae': 'loro', 'vultur': 'condor', 'condor': 'condor', 'sarcoramphus': 'condor',
            'eagle': 'aguila', 'aguila': 'aguila', 'spizaetus': 'aguila', 'buteo': 'gavilan', 'hawk': 'halcon',
            'falcon': 'halcon', 'halcon': 'halcon', 'tyrannus': 'tirano', 'tyrannidae': 'tirano', 'turdus': 'mirlo',
            'thrush': 'mirlo', 'saltator': 'saltador', 'tangara': 'tangara', 'thraupis': 'tangara', 'thraupidae': 'tangara',
           
            # Mariposas e insectos
            'mariposa': 'mariposa', 'butterfly': 'mariposa', 'lepidoptera': 'mariposa', 'morpho': 'morpho',
            'moth': 'polilla', 'polilla': 'polilla', 'lepidoptero': 'mariposa', 'heliconius': 'heliconius',
            'spider': 'araña', 'araneae': 'araña', 'tarantula': 'tarantula', 'theraphosidae': 'tarantula',
            'ant': 'hormiga', 'hormiga': 'hormiga', 'formicidae': 'hormiga', 'leafcutter': 'hormiga_cortadora',
            'beetle': 'escarabajo', 'coleoptera': 'escarabajo', 'dynastes': 'escarabajo_hercules', 'hercules': 'escarabajo_hercules',
            'dragonfly': 'libelula', 'odonata': 'libelula', 'libelula': 'libelula', 'bee': 'abeja', 'abeja': 'abeja',
            'apis': 'abeja', 'bombus': 'abejorro', 'bumblebee': 'abejorro', 'wasp': 'avispa', 'avispa': 'avispa',
           
            # Reptiles
            'serpiente': 'serpiente', 'snake': 'serpiente', 'culebra': 'serpiente', 'serpentes': 'serpiente',
            'bothrops': 'mapanare', 'lachesis': 'verrugosa', 'coral': 'coral', 'micrurus': 'coral', 'elapidae': 'coral',
            'lagarto': 'lagarto', 'lizard': 'lagarto', 'anolis': 'anolis', 'iguana': 'iguana', 'iguana_iguana': 'iguana_verde',
            'gecko': 'gecko', 'gekko': 'gecko', 'hemidactylus': 'gecko', 'tortuga': 'tortuga', 'turtle': 'tortuga',
            'testudines': 'tortuga', 'chelonia': 'tortuga_marina', 'caiman': 'caiman', 'crocodile': 'cocodrilo',
            'crocodylus': 'cocodrilo', 'cocodrilo': 'cocodrilo',
           
            # Mamíferos
            'mono': 'mono', 'monkey': 'mono', 'primate': 'primate', 'alouatta': 'mono_araguato', 'ateles': 'mono_araña',
            'cebus': 'mono_capuchino', 'saimiri': 'mono_titi', 'aotus': 'mico_nochero', 'saguinus': 'tamarin',
            'jaguar': 'jaguar', 'panthera': 'jaguar', 'panthera_onca': 'jaguar', 'leopardo': 'leopardo',
            'puma': 'puma', 'puma_concolor': 'puma', 'ocelot': 'ocelote', 'leopardus': 'ocelote', 'leopardus_pardalis': 'ocelote',
            'margay': 'margay', 'leopardus_wiedii': 'margay', 'tigrillo': 'tigrillo', 'oncilla': 'tigrillo',
            'oso': 'oso', 'bear': 'oso', 'tremarctos': 'oso_andino', 'tremarctos_ornatus': 'oso_andino',
            'oso_antioqueno': 'oso_andino', 'oso_de_anteojos': 'oso_andino', 'oso_frontino': 'oso_andino',
            'tapir': 'danta', 'tapirus': 'danta', 'tapirus_terrestris': 'danta', 'danta': 'danta',
            'venado': 'venado', 'deer': 'venado', 'mazama': 'venado', 'odocoileus': 'venado', 'peccary': 'zaino',
            'tayassu': 'zaino', 'pecari': 'zaino', 'zaino': 'zaino', 'chigüiro': 'chiguiro', 'capybara': 'chiguiro',
            'hydrochoerus': 'chiguiro', 'hydrochoerus_hydrochaeris': 'chiguiro',
           
            # Plantas
            'orquidea': 'orquidea', 'orquídea': 'orquidea', 'orchid': 'orquidea', 'orchidaceae': 'orquidea',
            'cattleya': 'orquidea_cattleya', 'cattleya_trianae': 'orquidea_cattleya', 'flor': 'flor', 'flower': 'flor',
            'tree': 'arbol', 'árbol': 'arbol', 'arbre': 'arbol', 'baum': 'arbol', 'planta': 'planta', 'plant': 'planta',
            'pflanzen': 'planta', 'plante': 'planta', 'bromelia': 'bromelia', 'bromeliaceae': 'bromelia',
            'guadua': 'guadua', 'guadua_angustifolia': 'guadua', 'ceiba': 'ceiba', 'ceiba_pentandra': 'ceiba',
            'palo_de_mango': 'mango', 'mangifera': 'mango', 'mango': 'mango', 'palma': 'palma', 'palm': 'palma',
            'arecaceae': 'palma', 'ceroxylon': 'palma_de_cera', 'ceroxylon_quindiuense': 'palma_de_cera',
            'quindio_wax_palm': 'palma_de_cera', 'frailejon': 'frailejon', 'espeletia': 'frailejon',
            'espeletia_grandiflora': 'frailejon', 'espeletia_uribei': 'frailejon',
           
            # Ecosistemas y hábitats
            'forest': 'bosque', 'jungle': 'selva', 'rainforest': 'selva_tropical', 'selva': 'selva',
            'amazon': 'amazonia', 'amazonia': 'amazonia', 'amazonas': 'amazonia', 'andes': 'andes', 'andino': 'andino',
            'paramo': 'paramo', 'páramo': 'paramo', 'mountain': 'montaña', 'montaña': 'montaña', 'mountain_forest': 'bosque_montano',
            'cloud_forest': 'bosque_nublado', 'bosque_nublado': 'bosque_nublado', 'manglar': 'manglar', 'mangrove': 'manglar',
            'wetland': 'humedal', 'humedal': 'humedal', 'river': 'rio', 'río': 'rio', 'waterfall': 'cascada', 'cascada': 'cascada',
            'lake': 'lago', 'laguna': 'laguna', 'lagoon': 'laguna', 'ocean': 'oceano', 'mar': 'mar', 'sea': 'mar',
            'coral': 'coral', 'coral_reef': 'arrecife_coralino', 'arrecife': 'arrecife', 'reef': 'arrecife',
           
            # Términos científicos comunes
            'biodiversidad': 'biodiversidad', 'biodiversity': 'biodiversidad', 'fauna': 'fauna', 'flora': 'flora',
            'wildlife': 'vida_silvestre', 'vida_silvestre': 'vida_silvestre', 'conservacion': 'conservacion',
            'conservation': 'conservacion', 'ecosistema': 'ecosistema', 'ecosystem': 'ecosistema',
            'endemico': 'endemico', 'endemic': 'endemico', 'nativo': 'nativo', 'native': 'nativo',
            'especie': 'especie', 'species': 'especie', 'habitat': 'habitat', 'paisaje': 'paisaje', 'landscape': 'paisaje',
            'naturaleza': 'naturaleza', 'nature': 'naturaleza', 'silvestre': 'silvestre', 'wild': 'silvestre',
            'tropical': 'tropical', 'neotropical': 'neotropical', 'colombia': 'colombia', 'colombian': 'colombia',
            'andes': 'andes', 'amazonia': 'amazonia', 'orinoquia': 'orinoquia', 'caribe': 'caribe',
            'pacifico': 'pacifico', 'pacific': 'pacifico', 'choco': 'choco', 'chocó': 'choco',
            'santander': 'santander', 'boyaca': 'boyaca', 'boyacá': 'boyaca', 'amazonas': 'amazonas',
            'guaviare': 'guaviare', 'guainia': 'guainia', 'guainía': 'guainia', 'vaupes': 'vaupes', 'vaupés': 'vaupes',
            'putumayo': 'putumayo', 'caqueta': 'caqueta', 'caquetá': 'caqueta', 'meta': 'meta', 'arauca': 'arauca',
            'vichada': 'vichada', 'guajira': 'guajira', 'magdalena': 'magdalena', 'cesar': 'cesar', 'cordoba': 'cordoba',
            'córdoba': 'cordoba', 'sucre': 'sucre', 'bolivar': 'bolivar', 'bolívar': 'bolivar', 'atlantico': 'atlantico',
            'atlántico': 'atlantico', 'santander': 'santander', 'norte_de_santander': 'norte_de_santander',
            'antioquia': 'antioquia', 'caldas': 'caldas', 'risaralda': 'risaralda', 'quindio': 'quindio',
            'quindío': 'quindio', 'tolima': 'tolima', 'huila': 'huila', 'cauca': 'cauca', 'nariño': 'nariño',
            'narinho': 'nariño', 'valle_del_cauca': 'valle_del_cauca', 'valle': 'valle_del_cauca',
            'choco_biogeografico': 'choco_biogeografico', 'chocó_biogeografico': 'choco_biogeografico',
            'choco_biogeográfico': 'choco_biogeografico', 'chocó_biogeográfico': 'choco_biogeografico'
        }
       
        # Buscar palabras clave en la descripción
        description_lower = description.lower()
        for keyword, spanish_word in species_keywords.items():
            if keyword in description_lower:
                keywords.append(spanish_word)
                break
       
        # Si no encontramos palabras clave específicas, usar palabras generales
        if not keywords:
            # Extraer sustantivos importantes
            words = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b', description)
            # Filtrar palabras comunes
            common_words = {'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'el', 'la', 'los', 'las', 'de', 'del', 'en', 'con', 'por', 'para', 'un', 'una', 'es', 'son', 'fue', 'fueron', 'y', 'o', 'pero', 'si', 'no', 'que', 'como', 'donde', 'cuando', 'colombia', 'colombian', 'biodiversity', 'biodiversidad', 'campaign', 'campaña', 'photo', 'foto', 'image', 'imagen'}
           
            for word in words[:3]:  # Tomar las primeras 3 palabras relevantes
                if len(word) > 2 and word.lower() not in common_words:
                    keywords.append(word.lower())
       
        # Crear nombre base
        if keywords:
            base_name = '_'.join(keywords[:2])  # Usar máximo 2 palabras clave
        else:
            # Fallback: usar parte del nombre original del archivo
            base_name = re.sub(r'[^\w\s-]', '', filename.replace('File:', ''))
            base_name = re.sub(r'[-\s]+', '_', base_name)
            base_name = base_name.lower()[:20]  # Limitar longitud
       
        # Limpiar caracteres especiales
        base_name = re.sub(r'[^\w_]', '', base_name)
        base_name = re.sub(r'_+', '_', base_name)
        base_name = base_name.strip('_')
       
        return base_name or 'biodiversidad'

    def safe_extract_metadata(self, data, *keys, default=''):
        """
        Extrae metadatos de manera segura, manejando estructuras anidadas.
        """
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, {})
            else:
                return default
        return result if result is not None else default

    def download_image(self, image_info: Dict, filename: str, counter: int) -> bool:
        """
        Descarga una imagen individual y guarda sus metadatos de manera segura.
        """
        try:
            # Validar la estructura de image_info
            if not isinstance(image_info, dict) or 'imageinfo' not in image_info:
                print("Estructura de metadatos inválida")
                return False
               
            # Obtener la información de la imagen de manera segura
            image_info_list = image_info.get('imageinfo', [{}])
            if not image_info_list or not isinstance(image_info_list, list):
                print("   No se encontró información de la imagen")
                return False
               
            first_image_info = image_info_list[0] if image_info_list else {}
            if not isinstance(first_image_info, dict):
                print("   Formato de información de imagen inválido")
                return False
           
            # Obtener la URL de la imagen
            image_url = self.safe_extract_metadata(first_image_info, 'url')
            if not image_url:
                print("   No se encontró URL para la imagen")
                return False
           
            # Obtener la extensión del archivo de manera segura
            file_extension = os.path.splitext(filename)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
           
            if not file_extension or file_extension not in valid_extensions:
                # Intentar obtener la extensión del tipo MIME si está disponible
                mime_type = self.safe_extract_metadata(first_image_info, 'mime', default='')
                if 'jpeg' in mime_type or 'jpg' in mime_type:
                    file_extension = '.jpg'
                elif 'png' in mime_type:
                    file_extension = '.png'
                elif 'gif' in mime_type:
                    file_extension = '.gif'
                elif 'webp' in mime_type:
                    file_extension = '.webp'
                else:
                    file_extension = '.jpg'  # Extensión por defecto
           
            # Crear un nombre de archivo descriptivo seguro
            try:
                descriptive_filename = self.create_descriptive_filename(image_info, filename)
                # Limpiar el nombre de archivo
                safe_filename = "".join([c if c.isalnum() or c in (' ', '_', '-', '.') else '_'
                                       for c in descriptive_filename])
                safe_filename = safe_filename.strip()
               
                # Asegurar que el nombre no esté vacío
                if not safe_filename:
                    safe_filename = f"imagen_{int(time.time())}_{counter}"
               
            except Exception as e:
                print(f"   Error al generar nombre descriptivo: {str(e)[:50]}...")
                safe_filename = f"imagen_{int(time.time())}_{counter}"
           
            # Asegurar la extensión correcta
            if not safe_filename.lower().endswith(file_extension.lower()):
                safe_filename += file_extension
           
            # Rutas de los archivos
            images_dir = os.path.join(self.download_dir, 'imagenes')
            metadata_dir = os.path.join(self.download_dir, 'metadatos')
           
            # Crear directorios si no existen
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(metadata_dir, exist_ok=True)
           
            # Ruta completa del archivo de imagen
            image_path = os.path.join(images_dir, safe_filename)
           
            # Verificar si el archivo ya existe y generar un nombre único
            base_name, ext = os.path.splitext(image_path)
            counter_suffix = 1
            while os.path.exists(image_path):
                image_path = f"{base_name}_{counter_suffix}{ext}"
                safe_filename = f"{os.path.splitext(os.path.basename(base_name))[0]}_{counter_suffix}{ext}"
                counter_suffix += 1
           
            # Descargar la imagen
            print(f"   Descargando imagen...")
            response = self.session.get(image_url, stream=True, timeout=30)
            response.raise_for_status()
           
            # Guardar la imagen
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filtrar keep-alive chunks
                        f.write(chunk)
           
            # Extraer metadatos de manera segura
            extmetadata = self.safe_extract_metadata(first_image_info, 'extmetadata', default={})
           
            # Preparar los metadatos con valores por defecto seguros
            metadata = {
                'titulo': self.safe_extract_metadata(extmetadata, 'ObjectName', 'value', default=''),
                'descripcion': self.safe_extract_metadata(extmetadata, 'ImageDescription', 'value', default=''),
                'autor': self.safe_extract_metadata(extmetadata, 'Artist', 'value', default=''),
                'licencia': self.safe_extract_metadata(extmetadata, 'LicenseShortName', 'value', default=''),
                'fecha': self.safe_extract_metadata(extmetadata, 'DateTimeOriginal', 'value', default=''),
                'categorias': self.safe_extract_metadata(extmetadata, 'Categories', 'value', default=''),
                'url_original': image_url,
                'nombre_archivo_original': filename,
                'nombre_archivo_descriptivo': safe_filename,
                'ancho': self.safe_extract_metadata(first_image_info, 'width', default=''),
                'alto': self.safe_extract_metadata(first_image_info, 'height', default=''),
                'tamaño_bytes': self.safe_extract_metadata(first_image_info, 'size', default=''),
                'tipo_mime': self.safe_extract_metadata(first_image_info, 'mime', default='')
            }
           
            # Nombre del archivo de metadatos
            metadata_filename = f"{os.path.splitext(safe_filename)[0]}_metadata.json"
            metadata_path = os.path.join(metadata_dir, metadata_filename)
           
            # Guardar metadatos en un archivo JSON
            try:
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"   Error al guardar metadatos: {str(e)[:50]}...")
           
            return True
           
        except requests.exceptions.RequestException as e:
            print(f"   Error de red: {str(e)[:100]}")
            return False
        except Exception as e:
            print(f"   Error inesperado: {str(e)[:100]}")
            import traceback
            print(f"   {traceback.format_exc()[:200]}...")
            return False
   
    def download_from_biodiversity_campaign(self, num_images: int = 50, min_relevance: float = 0.5):
        """
        Descarga imágenes específicamente de la campaña de biodiversidad de Colombia 2025,
        filtrando solo las imágenes relevantes según las palabras clave.
       
        Args:
            num_images: Número máximo de imágenes a descargar
            min_relevance: Umbral de relevancia mínimo (0-1) para considerar una imagen
        """
        print(f" Descargando hasta {num_images} imágenes relevantes de la Campaña: Biodiversidad en Colombia 2025")
        print("=" * 100)
       
        # Categoría específica de la campaña
        category = "Uploaded_via_Campaign:Biodiversidad_en_Colombia_2025"
       
        # Crear directorios necesarios
        os.makedirs(os.path.join(self.download_dir, 'imagenes'), exist_ok=True)
        os.makedirs(os.path.join(self.download_dir, 'metadatos'), exist_ok=True)
       
        # Obtener todas las imágenes de la categoría
        print(f" Buscando imágenes en la categoría: {category}")
        all_images = self.search_images_by_category(category, limit=500)
       
        if not all_images:
            print(" No se encontraron imágenes en la categoría especificada.")
            print("Por favor, verifica que la categoría existe y tiene imágenes.")
            return
       
        print(f" Encontradas {len(all_images)} imágenes en la campaña")
        print(" Filtrando imágenes relevantes...")
       
        # Filtrar imágenes relevantes
        relevant_images = []
        for img in all_images:
            if self.is_relevant_image(img):
                relevant_images.append(img)
               
                # Si ya tenemos suficientes imágenes relevantes, detener la búsqueda
                if len(relevant_images) >= num_images * 2:  # Buscar el doble para tener margen
                    break
       
        if not relevant_images:
            print(" No se encontraron imágenes relevantes en la categoría.")
            print("Puedes intentar ajustar las palabras clave en el código.")
            return
           
        print(f" Encontradas {len(relevant_images)} imágenes relevantes")
       
        # Limitar el número de imágenes al mínimo entre el solicitado y las disponibles
        num_to_download = min(num_images, len(relevant_images))
       
        # Si hay más imágenes relevantes que el límite, seleccionar aleatoriamente
        if len(relevant_images) > num_to_download:
            selected_images = random.sample(relevant_images, num_to_download)
        else:
            selected_images = relevant_images
       
        successful_downloads = 0
       
        print(f"\n Iniciando descarga de {len(selected_images)} imágenes relevantes...")
        print("-" * 100)
       
        for i, image_info in enumerate(selected_images, 1):
            # Extraer el nombre del archivo
            filename = image_info.get('title', '').replace('File:', '')
            if not filename:
                print(f" [{i:02d}/{len(selected_images):02d}] Nombre de archivo no válido")
                continue
               
            print(f"\n[{i:02d}/{len(selected_images):02d}] Procesando: {filename}")
           
            # Verificar si la imagen ya fue descargada
            base_name = os.path.splitext(filename)[0]
            if any(f.startswith(base_name) for f in os.listdir(os.path.join(self.download_dir, 'imagenes'))):
                print(f"    Ya existe, omitiendo...")
                successful_downloads += 1
                continue
           
            # Verificar relevancia nuevamente por si acaso
            if not self.is_relevant_image(image_info):
                print(f"     Imagen no relevante, omitiendo...")
                continue
           
            # Descargar la imagen
            if self.download_image(image_info, filename, i):
                successful_downloads += 1
                print(f"    Descargada exitosamente")
            else:
                print(f"    Error al descargar")
           
            # Pausa entre descargas para ser respetuoso con el servidor
            time.sleep(0.5)
       
        # Mostrar resumen detallado
        print("\n" + "=" * 100)
        print(" RESUMEN DETALLADO DE LA DESCARGA")
        print("=" * 100)
        print(f" Campaña: Biodiversidad en Colombia 2025")
        print(f" Directorio: {os.path.abspath(self.download_dir)}")
        print("-" * 100)
        print(f" Imágenes analizadas: {len(all_images)}")
        print(f" Imágenes relevantes encontradas: {len(relevant_images)}")
        print(f" Imágenes seleccionadas para descarga: {len(selected_images)}")
        print(f" Imágenes descargadas exitosamente: {successful_downloads}/{len(selected_images)}")
        print("-" * 100)
       
        # Mostrar estadísticas de palabras clave encontradas
        print("\n PALABRAS CLAVE ENCONTRADAS (las más comunes):")
        keyword_counts = {}
       
        # Contar palabras clave en las imágenes descargadas
        for img in selected_images:
            if self.is_relevant_image(img):
                extmetadata = img.get('imageinfo', [{}])[0].get('extmetadata', {})
                text = f"{extmetadata.get('ObjectName', {}).get('value', '')} {extmetadata.get('ImageDescription', {}).get('value', '')} {extmetadata.get('Categories', {}).get('value', '')}".lower()
               
                for keyword in self.keywords['especies'] + self.keywords['cientificos']:
                    if keyword.lower() in text:
                        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
       
        # Ordenar palabras clave por frecuencia (de mayor a menor)
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]  # Top 10
       
        if sorted_keywords:
            for keyword, count in sorted_keywords:
                print(f"   • {keyword}: {count} veces")
        else:
            print("   No se encontraron palabras clave en las imágenes descargadas.")
       
        # Mostrar sugerencias si hay pocas imágenes
        if successful_downloads < num_images // 2:
            print("\n SUGERENCIAS:")
            print("   • Intenta aumentar el número de imágenes a analizar (parámetro 'limit' en search_images_by_category)")
            print("   • Revisa las palabras clave en el código para asegurarte de que cubren todos los temas de interés")
            print("   • Verifica la conexión a internet si hay muchos errores de descarga")
       
        print("\n" + "=" * 100)
        print("¡Descarga completada!  Las imágenes y sus metadatos se han guardado en las carpetas 'imagenes' y 'metadatos'.")
        print("=" * 100)

    def download_random_images(self, search_terms: List[str], num_images: int = 50):
        """
        Descarga imágenes aleatorias basadas en términos de búsqueda
        """
        print(f"Iniciando descarga de {num_images} imágenes aleatorias...")
       
        all_images = []
       
        # Buscar imágenes por cada término
        for term in search_terms:
            print(f"\n--- Buscando por: {term} ---")
           
            # Intentar buscar por categoría primero
            category_results = self.search_images_by_category(term)
            if category_results:
                all_images.extend(category_results)
           
            # Buscar por palabra clave también
            keyword_results = self.search_images_by_keyword(term)
            if keyword_results:
                all_images.extend(keyword_results)
           
            time.sleep(1)  # Pausa entre búsquedas
       
        # Eliminar duplicados
        unique_images = []
        seen_titles = set()
        for img in all_images:
            title = img.get('title', '')
            if title not in seen_titles:
                unique_images.append(img)
                seen_titles.add(title)
       
        print(f"\nEncontradas {len(unique_images)} imágenes únicas")
       
        if not unique_images:
            print("No se encontraron imágenes. Intenta con otros términos de búsqueda.")
            return
       
        # Seleccionar aleatoriamente
        selected_images = random.sample(
            unique_images,
            min(num_images, len(unique_images))
        )
       
        print(f"Descargando {len(selected_images)} imágenes seleccionadas...")
       
        successful_downloads = 0
       
        for i, img in enumerate(selected_images, 1):
            filename = img.get('title', '')
            print(f"\n[{i}/{len(selected_images)}] Procesando: {filename}")
           
            # Obtener información detallada
            image_info = self.get_image_info(filename)
            if image_info:
                if self.download_image(image_info, filename, i):
                    successful_downloads += 1
           
            # Pausa entre descargas
            time.sleep(1)
       
        print(f"\n Descarga completada!")
        print(f"Imágenes descargadas exitosamente: {successful_downloads}/{len(selected_images)}")
        print(f"Ubicación: {os.path.abspath(self.download_dir)}")

def main():
    """
    Función principal
    """
    print(" Descargador de Imágenes - Campaña Biodiversidad en Colombia 2025 ")
    print("=" * 80)
   
    # Crear descargador
    downloader = WikimediaDownloader()
   
    # Descargar 50 imágenes aleatorias de la campaña específica
    downloader.download_from_biodiversity_campaign(num_images=50)
   
    print("\n ¡Proceso completado!")
    print(" Cada imagen incluye:")
    print("   • Archivo de imagen con nombre descriptivo")
    print("   • Archivo de metadatos con información detallada")
    print("   • Información de licencia y autor")

if __name__ == "__main__":
    main()