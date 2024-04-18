from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append("../")
# from utils import cred as cr
from utils import cred_2 as cr2
from utils import funciones as f

# Conexión a la base de datos utilizando SQLAlchemy
engine = create_engine(f"postgresql://{cr2.user}:{cr2.password}@{cr2.host}:{cr2.port}/{cr2.database}")
# Leer el DataFrame
df_read = pd.read_csv('../csv_s/csv_final_mix_to_db/csv_2024-04-10.csv')

# list_genero = ['Genero','genero','genero']
# list_idioma = ['Idiomas','lang_disp','nombre_lang']
# list_compania = ['Compañia','compania','nombre_compania']
# list_id_carac = ['id_compania','id_lang','id_genero']
# list_tab_int = ['id_juego','lang_disp_int','id_lang','genero_int','id_genero']

# conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
# cursor = conn.cursor()

# # Compañia

# f.inserts_comp_idiom_gen(cursor,conn,df_read,list_compania[0],list_compania[1],list_compania[2])

# #Idioma

# f.inserts_comp_idiom_gen(cursor,conn,df_read,list_idioma[0],list_idioma[1],list_idioma[2])

# # Genero

# f.inserts_comp_idiom_gen(cursor,conn,df_read,list_genero[0],list_genero[1],list_genero[2])

start_time = datetime.now()

# Insertar datos en la tabla info_juego

df_rename_info_juegos = df_read.rename(columns={
    'Titulo': 'nombre',
    'Compañia': 'nombre_compania',
    'Número de calificaciones': 'numero_calificaciones',
    'Calificación 5 estrellas': 'num_calificaciones_5_estrellas',
    'Calificación 4 estrellas': 'num_calificaciones_4_estrellas',
    'Calificación 3 estrellas': 'num_calificaciones_3_estrellas',
    'Calificación 2 estrellas': 'num_calificaciones_2_estrellas',
    'Calificación 1 estrella': 'num_calificaciones_1_estrellas',
    'Calificación PSN': 'calificacion_psn',
    'Lanzamiento': 'lanzamiento'
})

# Realizar una consulta a la tabla compania para obtener los id_compania correspondientes
query = "SELECT id_compania, nombre_compania FROM compania"
df_companias_bbdd = pd.read_sql(query, engine)

# Fusionar los datos con el DataFrame principal
df_merged = pd.merge(df_rename_info_juegos, df_companias_bbdd, on='nombre_compania', how='left')

# Insertar datos en la tabla info_juego
df_merged[~df_merged['id_juego'].isin(df_read['id_juego'])][['id_juego', 'nombre', 'id_compania', 'numero_calificaciones',
            'num_calificaciones_5_estrellas', 'num_calificaciones_4_estrellas',
            'num_calificaciones_3_estrellas', 'num_calificaciones_2_estrellas',
            'num_calificaciones_1_estrellas', 'calificacion_psn', 'lanzamiento']].to_sql('info_juego', con=engine, if_exists='append', index=False)

# Cerrar la conexión

engine.dispose()

end_time = datetime.now()
total_time = end_time - start_time
print(f"Finalizado los inserts en {total_time}")