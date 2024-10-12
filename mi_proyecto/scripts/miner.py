import os
import sqlite3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from datetime import datetime

def extraer_metadatos(mp3_file, ruta_bd='music_library.db'):
    try:
        audio = MP3(mp3_file, ID3=ID3)
    except Exception as e:
        print(f"No se pudo procesar el archivo {mp3_file}: {e}")
        return
    
    # Verificar si el archivo tiene etiquetas ID3
    if not audio.tags:
        print(f"No se encontraron etiquetas ID3 en el archivo {mp3_file}")
        # Asignar valores predeterminados si no hay etiquetas
        titulo = 'Desconocido'
        artista = 'Desconocido'
        album = 'Desconocido'
        año = datetime.now().year
        genero = 'Desconocido'
        pista = 1
    else:
        # Convertir etiquetas ID3 a un formato usable
        def convertir_a_texto(etiqueta):
            if etiqueta:
                valor = etiqueta[0]
                if isinstance(valor, list):
                    valor = valor[0]
                return str(valor)
            return 'Desconocido'

        titulo = convertir_a_texto(audio.tags.getall('TIT2'))
        artista = convertir_a_texto(audio.tags.getall('TPE1'))
        album = convertir_a_texto(audio.tags.getall('TALB'))
        año = convertir_a_texto(audio.tags.getall('TDRC'))
        genero = convertir_a_texto(audio.tags.getall('TCON'))
        pista = convertir_a_texto(audio.tags.getall('TRCK'))

        # Valores por defecto si los campos están vacíos
        if año == 'Desconocido':
            año = datetime.now().year
        if pista == 'Desconocido':
            pista = 1

    # Insertar datos en la base de datos
    conn = sqlite3.connect(ruta_bd)
    cursor = conn.cursor()

    # Insertar artista (ignorar si ya existe)
    cursor.execute('''
        INSERT OR IGNORE INTO performers (id_type, name)
        VALUES (2, ?)
    ''', (artista,))
    cursor.execute('SELECT id_performer FROM performers WHERE name = ?', (artista,))
    id_artista = cursor.fetchone()[0]

    # Insertar álbum (ignorar si ya existe)
    cursor.execute('''
        INSERT OR IGNORE INTO albums (path, name, year)
        VALUES (?, ?, ?)
    ''', (os.path.dirname(mp3_file), album, año))
    cursor.execute('SELECT album_id FROM albums WHERE name = ?', (album,))
    id_album = cursor.fetchone()[0]

    # Insertar pista en "rolas"
    cursor.execute('''
        INSERT INTO rolas (id_performer, id_album, path, title, track, year, genre)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_artista, id_album, mp3_file, titulo, pista, año, genero))

    conn.commit()
    conn.close()

def buscar_mp3(directorio, ruta_bd='music_library.db'):
    """Recorre el directorio actual y subdirectorios buscando archivos MP3."""
    for carpeta_raiz, subcarpetas, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith('.mp3'):
                extraer_metadatos(os.path.join(carpeta_raiz, archivo), ruta_bd)
