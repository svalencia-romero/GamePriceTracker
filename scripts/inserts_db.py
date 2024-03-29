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

