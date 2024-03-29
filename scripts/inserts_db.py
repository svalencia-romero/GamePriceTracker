# EN OBRAS!!! NO EJECUTAR!!

import psycopg2
import pandas as pd
import sys
sys.path.append("../")
from utils import cred as cr
from utils import cred_2 as cr2
from utils import funciones as f
df = pd.read_csv('../csv_s/csv_mix_price_id_es/csv_2024-03-11.csv')

# Compañia

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()

for compania in df['Compañia'].str.split(',').explode().str.strip().unique():
    # Verificar si la compñaia ya existe en la tabla
    cursor.execute("SELECT COUNT(*) FROM compania WHERE nombre_compania = %s", (compania,))
    existe = cursor.fetchone()[0]
    
    # Si la compañía no existe, insertarlo en la tabla
    if existe == 0:
        cursor.execute("INSERT INTO compania (nombre_compania) VALUES (%s)", (compania,))
        conn.commit()
    else:
        print(f"Ya existe la compañia {compania}")

cursor.close()
conn.close()

#Idioma

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()

for idioma in df['Idiomas'].str.split(',').explode().str.strip().unique():
    # Verificar si el idioma ya existe en la tabla
    cursor.execute("SELECT COUNT(*) FROM lang_disp WHERE nombre_lang = %s", (idioma,))
    existe = cursor.fetchone()[0]
    
    # Si el idioma no existe, insertarlo en la tabla
    if existe == 0:
        cursor.execute("INSERT INTO lang_disp (nombre_lang) VALUES (%s)", (idioma,))
        print(f"Insertando {idioma}")
        conn.commit()
    else:
        print(f"Ya existe el idioma {idioma}")

cursor.close()
conn.close()

# Genero

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()

for genero in df['Genero'].str.split(',').explode().str.strip().unique():
    # Verificar si el género ya existe en la tabla
    cursor.execute("SELECT COUNT(*) FROM genero WHERE genero = %s", (genero,))
    existe = cursor.fetchone()[0]
    
    # Si el género no existe, insertarlo en la tabla
    if existe == 0:
        cursor.execute("INSERT INTO genero (genero) VALUES (%s)", (genero,))
        print(f"Insertando {genero}")
        conn.commit()
    else:
        print(f"Genero {genero}, ya existe en la bbdd")

cursor.close()
conn.close()


# Info_juego

contador = 0
def obtener_id_compania(cursor, compania):
    cursor.execute("SELECT id_compania FROM compania WHERE nombre_compania LIKE %s;", ('%' + compania + '%',))
    id_compania = cursor.fetchone()
    if id_compania:
        return id_compania[0]
    else:
        return None

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()
for index, row in df.iterrows():
    id_juego = row['id_juego']
    
    # Verificar si el id_juego ya existe en la tabla info_juego
    cursor.execute("SELECT COUNT(*) FROM info_juego WHERE id_juego = %s", (id_juego,))
    if cursor.fetchone()[0] == 0:
        # Si el id_juego no existe en la tabla, entonces procede con la inserción
        companias = row['Compañia'].split(',')
        for compania in companias:
            compania = compania.strip()
            
            id_compania = obtener_id_compania(cursor, compania)  # Obtener el id de la compañía
            cursor.execute("INSERT INTO info_juego (id_juego, nombre, id_compania, numero_calificaciones,num_calificaciones_5_estrellas, num_calificaciones_4_estrellas,num_calificaciones_3_estrellas, num_calificaciones_2_estrellas,num_calificaciones_1_estrellas,calificacion_psn,lanzamiento)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (id_juego, row['Titulo'], id_compania, row['Número de calificaciones'],
                            row['Calificación 5 estrellas'], row['Calificación 4 estrellas'],
                            row['Calificación 3 estrellas'], row['Calificación 2 estrellas'],
                            row['Calificación 1 estrella'], row['Calificación PSN'],row["Lanzamiento"]))
            print(f"Se añade {id_juego} ")
            contador += 1
            conn.commit()
            break # Pongo este break para que solo me obtenga la primera parte, hay ocasiones que las comas hace que tenga dos valores en vez uno como debería.
    else:
        print(f"El id_juego {id_juego} ya existe en la tabla info_juego")

# Cerrar la conexión
print(f"Se han añadido {contador} juegos")
conn.close()

# Tablas intermedias

#idioma
contador = 0
def obtener_id_idioma(cursor, idioma):
    cursor.execute("SELECT id_lang FROM lang_disp WHERE nombre_lang = %s", (idioma,))
    id_idioma = cursor.fetchone()
    if id_idioma:
        return id_idioma[0]
    else:
        return None

def verificar_existencia(cursor, id_juego, id_lang):
    cursor.execute("SELECT COUNT(*) FROM lang_disp_int WHERE id_juego = %s AND id_lang = %s", (id_juego, id_lang))
    count = cursor.fetchone()[0]
    return count > 0

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()
for index, row in df.iterrows():
    # Obtener los idiomas de la fila actual
    idiomas = row['Idiomas'].split(',')
    
    # Iterar sobre cada idioma
    for idioma in idiomas:
        idioma = idioma.strip()
        
        id_idioma = obtener_id_idioma(cursor, idioma)  # Obtener el id del idioma 
        
        if id_idioma is not None:
            id_juego = row['id_juego']

            if not verificar_existencia(cursor, id_juego, id_idioma):
                cursor.execute("INSERT INTO lang_disp_int (id_juego, id_lang) VALUES (%s, %s)", (id_juego, id_idioma))
                contador += 1
                conn.commit()
            else:
                print(f"El par (id_juego={id_juego}, id_lang={id_idioma}) ya existe en lang_disp_int, se omitirá la inserción.")

# Cerrar la conexión
print(f"Se han insertado en la tabla intermedia {contador} registros")
conn.close()

# Genero

contador = 0
def obtener_id_genero(cursor, genero):
    cursor.execute("SELECT id_genero FROM genero WHERE genero = %s", (genero,))
    id_genero = cursor.fetchone()
    if id_genero:
        return id_genero[0]
    else:
        return None

def verificar_existencia(cursor, id_juego, id_genero):
    cursor.execute("SELECT COUNT(*) FROM genero_int WHERE id_juego = %s AND id_genero = %s", (id_juego, id_genero))
    count = cursor.fetchone()[0]
    return count > 0

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()
for index, row in df.iterrows():
    # Obtener los generos de la fila actual
    generos = row['Genero'].split(',')
    
    # Iterar sobre cada genero
    for genero in generos:
        genero = genero.strip()
        
        id_genero = obtener_id_genero(cursor, genero)  # Obtener el id del genero
        
        if id_genero is not None:
            id_juego = row['id_juego']
            if not verificar_existencia(cursor, id_juego, id_genero):
                cursor.execute("INSERT INTO genero_int (id_juego, id_genero) VALUES (%s, %s)", (id_juego, id_genero))
                contador += 1
                conn.commit()
            else:
                print(f"El par (id_juego={id_juego}, id_genero={id_genero}) ya existe en genero_int, se omitirá la inserción.")

# Cerrar la conexión
print(contador)
conn.close()


