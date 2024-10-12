import os
import sqlite3
import pygame
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, 
                             QSlider, QLineEdit, QLabel)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QHeaderView
from db_manager import obtener_datos_de_bd
from miner import extraer_metadatos


pygame.mixer.init()

volumen_actual = 0.5
ruta_archivo_actual = None
timer = QTimer()

slider_progreso = None
slider_ajustando = False  # Variable para controlar si el usuario está ajustando el slider

def llenar_tabla(tabla, datos):
    tabla.setRowCount(0)  # Limpiar la tabla
    for num_fila, datos_fila in enumerate(datos):
        tabla.insertRow(num_fila)
        for num_columna, dato in enumerate(datos_fila):
            tabla.setItem(num_fila, num_columna, QTableWidgetItem(str(dato)))

def mostrar_dialogo_archivos():
    dialogo = QFileDialog()
    dialogo.setFileMode(QFileDialog.Directory)
    if dialogo.exec_():
        ruta_carpeta = dialogo.selectedFiles()[0]
        # Minar los archivos con barra de progreso
        minar_con_progreso(ruta_carpeta)

def cargar_audio(ruta_archivo):
    global ruta_archivo_actual
    if not ruta_archivo:  # Verificar que haya una ruta
        print("No se ha seleccionado ningún archivo.")
        return
    
    try:
        ruta_archivo_actual = ruta_archivo
        pygame.mixer.music.load(ruta_archivo_actual)
        pygame.mixer.music.set_volume(volumen_actual)  
        pygame.mixer.music.play()  
        print(f"Reproduciendo: {ruta_archivo_actual}")
    except pygame.error as e:
        print(f"Error al cargar el archivo: {e}")

def reproducir_pausar():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def saltar(segundos):
    pos_actual = pygame.mixer.music.get_pos() / 1000.0
    pygame.mixer.music.play(start=pos_actual + segundos)

def cambiar_volumen(valor):
    global volumen_actual
    volumen_actual = valor / 100.0
    pygame.mixer.music.set_volume(volumen_actual)

def actualizar_progreso_audio():
    global slider_progreso, slider_ajustando
    if ruta_archivo_actual and not slider_ajustando:
        duracion_total = pygame.mixer.Sound(ruta_archivo_actual).get_length()
        pos_actual = pygame.mixer.music.get_pos() / 1000.0
        if duracion_total > 0:  
            progreso = int((pos_actual / duracion_total) * 100) 
            slider_progreso.setValue(progreso)

def ajustar_progreso():
    global slider_progreso, slider_ajustando
    slider_ajustando = True  # Marcar que el usuario está ajustando el slider
    duracion_total = pygame.mixer.Sound(ruta_archivo_actual).get_length()
    nueva_pos = (slider_progreso.value() / 100.0) * duracion_total
    pygame.mixer.music.play(start=nueva_pos)

def terminar_ajuste_progreso():
    global slider_ajustando
    slider_ajustando = False  # Marcar que el ajuste del slider ha terminado

def crear_ventana():
    global slider_progreso
    app = QApplication([])

    ventana_principal = QMainWindow()
    ventana_principal.setWindowTitle('Caja Musical Barata')
    ventana_principal.setGeometry(200, 100, 800, 600)

    tabla = QTableWidget()
    tabla.setColumnCount(7)  # Aumentar a 7 columnas para incluir la ruta
    tabla.setHorizontalHeaderLabels(['Título', 'Artista', 'Álbum', 'Año', 'Género', 'Pista', 'Ruta'])

    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    datos = obtener_datos_de_bd()
    llenar_tabla(tabla, datos)

    campo_busqueda = QLineEdit()
    campo_busqueda.setPlaceholderText('Buscar por título, artista o álbum...')
    
    # Botón de búsqueda
    boton_buscar = QPushButton('Buscar')
    
    def buscar():
        texto_busqueda = campo_busqueda.text()
        query = f'''
            SELECT r.title, p.name, a.name, r.year, r.genre, r.track, r.path
            FROM rolas r
            JOIN performers p ON r.id_performer = p.id_performer
            JOIN albums a ON r.id_album = a.album_id
            WHERE r.title LIKE '%{texto_busqueda}%' OR p.name LIKE '%{texto_busqueda}%' OR a.name LIKE '%{texto_busqueda}%'
        '''
        datos = obtener_datos_de_bd(query=query)
        llenar_tabla(tabla, datos)

    boton_buscar.clicked.connect(buscar)

    # Botón para minar directorio
    boton_minar = QPushButton('Buscar...')
    boton_minar.clicked.connect(mostrar_dialogo_archivos)

    # Layout de búsqueda
    layout_busqueda = QHBoxLayout()
    layout_busqueda.addWidget(campo_busqueda)
    layout_busqueda.addWidget(boton_buscar)

    # Controles del reproductor de audio
    boton_reproducir_pausar = QPushButton('Pausa/Start')
    boton_atras = QPushButton('-10 s')
    boton_adelante = QPushButton('+10 s')

    slider_progreso = QSlider(Qt.Horizontal)
    slider_progreso.setValue(0)
    slider_progreso.setMaximum(100)

    slider_volumen = QSlider(Qt.Horizontal)
    slider_volumen.setRange(0, 100)
    slider_volumen.setValue(50)
    slider_volumen.setTickInterval(10)

    etiqueta_volumen = QLabel('Volumen')

    def seleccionar_archivo_audio(fila, columna):
        ruta_archivo = tabla.item(fila, 6)
        if ruta_archivo is not None:
            cargar_audio(ruta_archivo.text())

    boton_reproducir_pausar.clicked.connect(reproducir_pausar)
    boton_atras.clicked.connect(lambda: saltar(-10))
    boton_adelante.clicked.connect(lambda: saltar(10))
    slider_volumen.valueChanged.connect(cambiar_volumen)

    slider_progreso.sliderPressed.connect(ajustar_progreso)
    slider_progreso.sliderReleased.connect(terminar_ajuste_progreso)

    layout_reproductor = QHBoxLayout()
    layout_reproductor.addWidget(boton_atras)
    layout_reproductor.addWidget(boton_reproducir_pausar)
    layout_reproductor.addWidget(boton_adelante)
    layout_reproductor.addWidget(etiqueta_volumen)
    layout_reproductor.addWidget(slider_volumen)

    layout_principal = QVBoxLayout()
    layout_principal.addLayout(layout_busqueda)
    layout_principal.addWidget(boton_minar)
    layout_principal.addWidget(tabla)
    layout_principal.addLayout(layout_reproductor)
    layout_principal.addWidget(slider_progreso)

    contenedor = QWidget()
    contenedor.setLayout(layout_principal)
    ventana_principal.setCentralWidget(contenedor)

    tabla.cellClicked.connect(seleccionar_archivo_audio)

    ventana_principal.show()
    app.exec_()

timer.timeout.connect(actualizar_progreso_audio)

if __name__ == '__main__':
    crear_ventana()

