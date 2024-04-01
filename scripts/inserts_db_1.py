# EN OBRAS!!! NO EJECUTAR!!
# Primero haré los inserts en bbdd de prueba (Elephant SQL)

from datetime import datetime
import psycopg2
import pandas as pd
import sys
sys.path.append("../")
# from utils import cred as cr
from utils import cred_2 as cr2
from utils import funciones as f
df_read = pd.read_csv('../csv_s/csv_mix_price_id_es/csv_2024-03-18.csv')

start_time = datetime.now()
# Las tablas de Suscripcion, plataformas y psn_region una vez hechos los primeros inserts los dejamos tal cual ya que no van a cambiar

'''
Variables para las funciones
'''

list_genero = ['Genero','genero','genero']
list_idioma = ['Idiomas','lang_disp','nombre_lang']
list_compania = ['Compañia','compania','nombre_compania']
list_id_carac = ['id_compania','id_lang','id_genero']
list_tab_int = ['id_juego','lang_disp_int','id_lang','genero_int','id_genero']

# Conexiones a la bbdd
conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()

# Compañia

f.inserts_comp_idiom_gen(cursor,conn,df_read,list_compania[0],list_compania[1],list_compania[2])

#Idioma

f.inserts_comp_idiom_gen(cursor,conn,df_read,list_idioma[0],list_idioma[1],list_idioma[2])

# Genero

f.inserts_comp_idiom_gen(cursor,conn,df_read,list_genero[0],list_genero[1],list_genero[2])

# Info_juego

contador = 0

for index, row in df_read.iterrows():
    id_juego = row['id_juego']
    
    # Verificar si el id_juego ya existe en la tabla info_juego
    cursor.execute("SELECT COUNT(*) FROM info_juego WHERE id_juego = %s", (id_juego,))
    if cursor.fetchone()[0] == 0:
        # Si el id_juego no existe en la tabla, entonces procede con la inserción
        companias = row['Compañia'].split(',')
        for compania in companias:
            compania = compania.strip()
            
            id_compania = f.obtener_id_carc(cursor,compania,list_id_carac[0],list_compania[1],list_compania[2])
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


# Tablas intermedias

#idioma
contador = 0

for index, row in df_read.iterrows():
    # Obtener los idiomas de la fila actual
    idiomas = row['Idiomas'].split(',')
    
    # Iterar sobre cada idioma
    for idioma in idiomas:
        idioma = idioma.strip()
                
        id_idioma = f.obtener_id_carc(cursor,idioma,list_id_carac[1],list_idioma[1],list_idioma[2])
        if id_idioma is not None:
            id_juego = row['id_juego']

            if not f.verificar_existencia(cursor, list_tab_int[0],list_tab_int[1],list_tab_int[2],id_juego, id_idioma):
                cursor.execute("INSERT INTO lang_disp_int (id_juego, id_lang) VALUES (%s, %s)", (id_juego, id_idioma))
                contador += 1
                print(f'Tabla intermedia idioma,{contador}')
                conn.commit()
            else:
                print(f"El combo (id_juego={id_juego}, id_lang={id_idioma}) ya existe en lang_disp_int, se omitirá la inserción.")

# Cerrar la conexión
print(f"Se han insertado en la tabla intermedia {contador} registros")


# Genero

contador = 0

for index, row in df_read.iterrows():
    # Obtener los generos de la fila actual
    generos = row['Genero'].split(',')
    
    # Iterar sobre cada genero
    for genero in generos:
        genero = genero.strip()
        
        id_genero = f.obtener_id_carc(cursor, genero,list_id_carac[2],list_genero[1],list_genero[2])  # Obtener el id del genero
        
        if id_genero is not None:
            id_juego = row['id_juego']
            if not f.verificar_existencia(cursor,list_tab_int[0],list_tab_int[3],list_tab_int[4], id_juego, id_genero):
                cursor.execute("INSERT INTO genero_int (id_juego, id_genero) VALUES (%s, %s)", (id_juego, id_genero))
                contador += 1
                print(f'Tabla intermedia género,{contador}')
                conn.commit()
            else:
                print(f"El combo (id_juego={id_juego}, id_genero={id_genero}) ya existe en genero_int, se omitirá la inserción.")


print(f'Número de géneros en tabla intermedia :{contador}')

contador = 0

for index, row in df_read.iterrows():
    id_sus = [1,4,7,2,5,8,3,6,9]
    for id_suscripcion in id_sus:
        if id_suscripcion in [1, 4, 7]:  # Sentencias para juegos store española
            col_precio = "Precio original ESP" if id_suscripcion == 1 else "Precio actual sin PSN ESP" if id_suscripcion == 4 else "Precio actual con PSN ESP"
        elif id_suscripcion in [2, 5, 8]:  # Sentencias para juegos store USA
            col_precio = "Precio original USA" if id_suscripcion == 2 else "Precio actual sin PSN USA" if id_suscripcion == 5 else "Precio actual con PSN USA"
        else:  # Sentencias para juegos store JP
            col_precio = "Precio original JP" if id_suscripcion == 3 else "Precio actual sin PSN JP" if id_suscripcion == 6 else "Precio actual con PSN JP"

        cursor.execute(
            f"INSERT INTO precio (id_suscripcion, precio, fecha_webs, id_juego) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM precio WHERE id_suscripcion = %s AND precio = %s AND fecha_webs = %s AND id_juego = %s) LIMIT 1",
            (id_suscripcion, row[col_precio], row["Día y hora"], row["id_juego"], id_suscripcion, row[col_precio], row["Día y hora"], row["id_juego"]))
        conn.commit()
        
        contador += 1
        print(f"Tabla precio {contador}")

print(f"ok inserts precios, n de inserts {contador}")


# Cerramos conexión
conn.close()

end_time = datetime.now()
total_time = end_time - start_time
print(f"Finalizado los inserts en {total_time} ")
