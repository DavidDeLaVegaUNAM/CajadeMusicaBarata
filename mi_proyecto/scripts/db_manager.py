import sqlite3

def crear_base_datos(ruta_bd='music_library.db'):
    conn = sqlite3.connect(ruta_bd)
    cursor = conn.cursor()

   #Crear tabla por primera vez
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS types (
        id_type INTEGER PRIMARY KEY,
        description TEXT
    );

    INSERT OR IGNORE INTO types VALUES(0,'Person');
    INSERT OR IGNORE INTO types VALUES(1,'Group');
    INSERT OR IGNORE INTO types VALUES(2,'Unknown');

    CREATE TABLE IF NOT EXISTS performers (
        id_performer INTEGER PRIMARY KEY,
        id_type INTEGER,
        name TEXT,
        FOREIGN KEY (id_type) REFERENCES types(id_type)
    );

    CREATE TABLE IF NOT EXISTS persons (
        id_person INTEGER PRIMARY KEY,
        stage_name TEXT,
        real_name TEXT,
        birth_date TEXT,
        death_date TEXT
    );

    CREATE TABLE IF NOT EXISTS groups (
        id_group INTEGER PRIMARY KEY,
        name TEXT,
        start_date TEXT,
        end_date TEXT
    );

    CREATE TABLE IF NOT EXISTS in_group (
        id_person INTEGER,
        id_group INTEGER,
        PRIMARY KEY (id_person, id_group),
        FOREIGN KEY (id_person) REFERENCES persons(id_person),
        FOREIGN KEY (id_group) REFERENCES groups(id_group)
    );

    CREATE TABLE IF NOT EXISTS albums (
        album_id INTEGER PRIMARY KEY,
        path TEXT,
        name TEXT,
        year INTEGER
    );

    CREATE TABLE IF NOT EXISTS rolas (
        id_rola INTEGER PRIMARY KEY,
        id_performer INTEGER,
        id_album INTEGER,
        path TEXT,
        title TEXT,
        track INTEGER,
        year INTEGER,
        genre TEXT,
        FOREIGN KEY (id_performer) REFERENCES performers(id_performer),
        FOREIGN KEY (id_album) REFERENCES albums(id_album)
    );
    ''')

    conn.commit()
    conn.close()

def obtener_datos_de_bd(query=None, ruta_bd='music_library.db'):
    conn = sqlite3.connect(ruta_bd)
    cursor = conn.cursor()

    if query is None:
        query = '''
        SELECT r.title, p.name, a.name, r.year, r.genre, r.track
        FROM rolas r
        JOIN performers p ON r.id_performer = p.id_performer
        JOIN albums a ON r.id_album = a.album_id
        '''
    
    cursor.execute(query)
    datos = cursor.fetchall()
    conn.close()
    return datos
