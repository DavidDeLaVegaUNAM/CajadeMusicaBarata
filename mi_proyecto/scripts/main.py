from db_manager import crear_base_datos
from miner import buscar_mp3
from gui import crear_ventana

def main():
  
    crear_base_datos('music_library.db')

    directorio_musica = '/ruta/a/musica'
    buscar_mp3(directorio_musica, 'music_library.db')

    crear_ventana()

if __name__ == '__main__':
    main()
