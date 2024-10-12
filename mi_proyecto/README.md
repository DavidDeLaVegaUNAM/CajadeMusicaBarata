
# GUI de Reproductor de Audio y Explorador de Archivos

Este proyecto es una aplicación gráfica desarrollada en **Python** utilizando **PyQt5** para la interfaz de usuario y **Pygame** para la reproducción de archivos de audio. La aplicación permite buscar archivos de audio en una base de datos, reproducirlos y controlar el progreso de la pista con una barra deslizante, además de ajustar el volumen.

## Características Principales

- **Explorador de Archivos**: El usuario puede seleccionar un directorio y minar archivos de audio, extrayendo metadatos como el título, artista, álbum, año, género y pista.
- **Reproducción de Audio**: Capacidad para reproducir, pausar, avanzar y retroceder en pistas de audio seleccionadas desde la base de datos.
- **Control de Volumen**: Se puede ajustar el volumen del audio en tiempo real mediante un control deslizante.
- **Barra de Progreso**: Visualiza el progreso de la reproducción y permite ajustar la posición de la pista.

## Requisitos

- Python 3.x
- PyQt5
- Pygame
- SQLite3

## Instalación

1. Clona el repositorio:

   git clone https://github.com/DavidDeLaVegaUNAM/CajadeMusicaBarata.git
   ```

2. Instala las dependencias necesarias:

   pip install -r requirements.txt


3. Ejecuta la aplicación:

   python3 main.py


## Estructura del Proyecto

El proyecto tiene la siguiente estructura:

```
├── app.py                    # Archivo principal de la GUI
├── db_manager.py             # Módulo para manejar la base de datos
├── miner.py                  # Módulo para extraer metadatos de archivos de audio
├── README.md                 # Documentación del proyecto
├── requirements.txt          # Dependencias del proyecto
└── assets                    # Recursos adicionales, si es necesario
```

## Descripción del Código

### Importaciones

El script hace uso de los siguientes módulos:

- **os**: Para interactuar con el sistema de archivos.
- **sqlite3**: Para gestionar la base de datos SQLite donde se almacenan los metadatos de las canciones.
- **pygame**: Para cargar y reproducir archivos de audio.
- **PyQt5**: Para crear la interfaz gráfica, incluyendo botones, deslizadores, tablas y diálogos.
- **db_manager.py**: Módulo que contiene funciones para obtener datos de la base de datos.
- **miner.py**: Módulo que contiene la lógica para extraer metadatos de los archivos de audio.

### Variables Globales

Se inicializa el mezclador de audio y se configuran varias variables globales:
- **volumen_actual**: Controla el nivel de volumen inicial (0.5 por defecto).
- **ruta_archivo_actual**: Almacena la ruta del archivo de audio que se está reproduciendo actualmente.
- **slider_progreso**: Control deslizante para mostrar y ajustar el progreso de la pista.
- **slider_ajustando**: Bandera para evitar conflictos mientras el usuario ajusta manualmente el progreso.

### Funciones Principales

#### `llenar_tabla(tabla, datos)`
Llena una tabla con los datos de los archivos de audio extraídos de la base de datos.

#### `mostrar_dialogo_archivos()`
Abre un cuadro de diálogo que permite al usuario seleccionar un directorio para minar y extraer metadatos de los archivos de audio en ese directorio.

#### `cargar_audio(ruta_archivo)`
Carga y reproduce un archivo de audio en la aplicación. Maneja errores si no es posible cargar el archivo.

#### `reproducir_pausar()`
Permite pausar o reanudar la reproducción de audio.

#### `saltar(segundos)`
Permite adelantar o retroceder la pista de audio en intervalos de tiempo específicos.

#### `cambiar_volumen(valor)`
Ajusta el volumen de la reproducción en función del valor del control deslizante.

#### `actualizar_progreso_audio()`
Actualiza el progreso de la barra deslizante según la posición actual de la pista.

#### `ajustar_progreso()`
Permite al usuario ajustar manualmente la posición de la pista mediante la barra de progreso.

#### `terminar_ajuste_progreso()`
Marca el final de la acción de ajuste manual del progreso.

### Interfaz Gráfica

#### `crear_ventana()`
Crea la ventana principal de la aplicación y organiza los componentes:

- **Tabla**: Despliega los archivos de audio y sus metadatos en columnas. La tabla se rellena con datos extraídos de la base de datos.
- **Campo de búsqueda**: Permite al usuario buscar canciones por título, artista o álbum.
- **Botones de control de audio**: Incluyen botones para pausar/reanudar, avanzar y retroceder la pista.
- **Slider de volumen**: Ajusta el nivel de volumen de la reproducción.
- **Slider de progreso**: Permite visualizar y ajustar la posición de la pista de audio.

### Temporizador

El temporizador se usa para actualizar constantemente la barra de progreso del audio en la interfaz gráfica.

timer.timeout.connect(actualizar_progreso_audio)


### Ejecución

El archivo principal de la aplicación contiene el siguiente bloque para ejecutar la interfaz gráfica:


if __name__ == '__main__':
    crear_ventana()




## Uso de la Aplicación

1. **Cargar Archivos de Audio**: Haz clic en el botón "Buscar..." para seleccionar una carpeta de audio. El programa extraerá automáticamente los metadatos de los archivos de audio compatibles.
2. **Reproducir Canciones**: Selecciona una canción de la tabla y haz clic en los botones de reproducción para escucharla.
3. **Controlar el Volumen**: Usa el control deslizante de volumen para ajustar el nivel de audio.
4. **Buscar Canciones**: Ingresa un título, artista o álbum en el campo de búsqueda para filtrar la tabla.



## Problemas
No sé si sea, pero totalmente funcional, ninguna clase.

Cuando carga la BD y depués se abre, mantiene la base de datos, sin embargo la parte de ruta aparece vacía, hay que dar click en Buscar para que agarre
nuevamente los datos y pueda reproducir música. 

Otro problema son los botones de +10 s y -10 s, no funcionan bien del todo, se regresan al comienzo de la canción, la barra de reproducción no avanza y no 
supe porqué. 

No alcancé a pedir el NP, ni modo pipipi