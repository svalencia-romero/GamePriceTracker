from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append("../")
# from utils import cred as cr
from utils import cred_2 as cr2
from utils import funciones as f

# Leer el DataFrame
df_read = pd.read_csv('../csv_s/csv_final_mix_to_db/csv_2024-04-02.csv')

list_genero = ['Genero','genero','genero']
list_idioma = ['Idiomas','lang_disp','nombre_lang']
list_compania = ['Compañia','compania','nombre_compania']
list_id_carac = ['id_compania','id_lang','id_genero']
list_tab_int = ['id_juego','lang_disp_int','id_lang','genero_int','id_genero']

conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()
# ------------------------------------------------------------------------ #
# -------- Insertar datos en la tabla Compania, lang_disp, genero -------- #
# ------------------------------------------------------------------------ #

# # Compañia

f.inserts_comp_idiom_gen(cursor,conn,df_read,list_compania[0],list_compania[1],list_compania[2])

# #Idioma

f.inserts_comp_idiom_gen(cursor,conn,df_read,list_idioma[0],list_idioma[1],list_idioma[2])

# Genero

f.inserts_comp_idiom_gen(cursor,conn,df_read,list_genero[0],list_genero[1],list_genero[2])

start_time = datetime.now()

conn.commit()
cursor.close()
conn.close()
# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla compania_int ---------------- #
# ------------------------------------------------------------------------ #
datos_id_compan = []
# Conexión a la base de datos utilizando SQLAlchemy
engine = create_engine(f"postgresql://{cr2.user}:{cr2.password}@{cr2.host}:{cr2.port}/{cr2.database}")
# Leer el DataFrame
df_read = pd.read_csv('../csv_s/csv_final_mix_to_db/csv_2024-04-02.csv')

query = '''SELECT id_juego,compania.id_compania,nombre_compania FROM public.compania_int
        INNER JOIN compania ON compania_int.id_compania = compania.id_compania
        '''
df_compan_bbdd = pd.read_sql(query, engine)


query = '''SELECT id_compania,nombre_compania from compania'''
df_comp_orig = pd.read_sql(query, engine)


for index, row in df_read.iterrows():
    # Obtener los idiomas de la fila actual
    companias = row['Compañia'].split(',')
    for compania in companias:
        compania = compania.strip()
        id_compania = df_comp_orig["id_compania"][df_comp_orig["nombre_compania"] == compania].values
        id_juego = row["id_juego"]
        datos_id_compan.append({"id_juego":id_juego,"id_compania":int(id_compania[0])})
df_nuevo_com_int = pd.DataFrame(datos_id_compan)

nuevo_df = df_nuevo_com_int[~df_nuevo_com_int['id_juego'].isin(df_compan_bbdd['id_juego']) & ~df_nuevo_com_int['id_compania'].isin(df_compan_bbdd['id_compania'])]

if not nuevo_df.empty:
    nuevo_df.to_sql(name='compania_int', con=engine, if_exists='append', index=False)
    
print(f"Numero de inserts en compania_int {len(nuevo_df)}")

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla info_juego ----------------- #
# ------------------------------------------------------------------------ #

# Conexión a la base de datos utilizando SQLAlchemy
engine = create_engine(f"postgresql://{cr2.user}:{cr2.password}@{cr2.host}:{cr2.port}/{cr2.database}")

# Info Juego
df_rename_info_juegos = df_read.rename(columns={
    'Titulo': 'nombre',
    'Número de calificaciones': 'numero_calificaciones',
    'Calificación 5 estrellas': 'num_calificaciones_5_estrellas',
    'Calificación 4 estrellas': 'num_calificaciones_4_estrellas',
    'Calificación 3 estrellas': 'num_calificaciones_3_estrellas',
    'Calificación 2 estrellas': 'num_calificaciones_2_estrellas',
    'Calificación 1 estrella': 'num_calificaciones_1_estrellas',
    'Calificación PSN': 'calificacion_psn',
    'Lanzamiento': 'lanzamiento'
})
query = '''SELECT id_juego FROM info_juego'''
df_id_juego_bbdd = pd.read_sql(query, engine)

# Insertar datos en la tabla info_juego
df_rename_info_juegos[~df_rename_info_juegos['id_juego'].isin(df_id_juego_bbdd['id_juego'])][['id_juego', 'nombre', 'numero_calificaciones',
            'num_calificaciones_5_estrellas', 'num_calificaciones_4_estrellas',
            'num_calificaciones_3_estrellas', 'num_calificaciones_2_estrellas',
            'num_calificaciones_1_estrellas', 'calificacion_psn', 'lanzamiento']].to_sql('info_juego', con=engine, if_exists='append', index=False)

# Cerrar la conexión

engine.dispose()
# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla plat_int ------------------- #
# ------------------------------------------------------------------------ #

query = "SELECT id_plat,id_juego FROM public.plat_int"
df_plat_bbdd = pd.read_sql(query, engine)

datos_id_plat = []

for index, row in df_read.iterrows():
    if "PS4" in row["Plataforma"]:
        datos_id_plat.append({"id_juego": row["id_juego"], "id_plat": 1})
    if "PS5" in row["Plataforma"]:
        datos_id_plat.append({"id_juego": row["id_juego"], "id_plat": 2})
df_nuevo_plat_int = pd.DataFrame(datos_id_plat)

df_nuevo_plat_int[~df_nuevo_plat_int['id_juego'].isin(df_plat_bbdd['id_juego'])][['id_plat','id_juego']].to_sql('plat_int', con=engine, if_exists='append', index=False)

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla lang_disp_int ----------------- #
# ------------------------------------------------------------------------ #

datos_id_lang = []
# Conexión a la base de datos utilizando SQLAlchemy
engine = create_engine(f"postgresql://{cr2.user}:{cr2.password}@{cr2.host}:{cr2.port}/{cr2.database}")
# Leer el DataFrame
df_read = pd.read_csv('../csv_s/csv_final_mix_to_db/csv_2024-04-02.csv')

query = '''SELECT id_juego,lang_disp.id_lang,nombre_lang FROM public.lang_disp_int
        INNER JOIN lang_disp ON lang_disp_int.id_lang = lang_disp.id_lang
        '''
df_lang_bbdd = pd.read_sql(query, engine)
df_lang_bbdd

query = '''SELECT id_lang,nombre_lang from lang_disp'''
df_lang_orig = pd.read_sql(query, engine)


for index, row in df_read.iterrows():
    # Obtener los idiomas de la fila actual
    idiomas = row['Idiomas'].split(',')
    for idioma in idiomas:
        idioma = idioma.strip()
        id_lang = df_lang_orig["id_lang"][df_lang_orig["nombre_lang"] == idioma].values
        id_juego = row["id_juego"]
        datos_id_lang.append({"id_juego":id_juego,"id_lang":int(id_lang[0])})
df_nuevo_lang_int = pd.DataFrame(datos_id_lang)

nuevo_df = df_nuevo_lang_int[~df_nuevo_lang_int['id_juego'].isin(df_lang_bbdd['id_juego']) & ~df_nuevo_lang_int['id_lang'].isin(df_lang_bbdd['id_lang'])]

if not nuevo_df.empty:
    nuevo_df.to_sql(name='lang_disp_int', con=engine, if_exists='append', index=False)

print(f"Numero de inserts en lang_disp_int {len(nuevo_df)}")

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla genero_int ----------------- #
# ------------------------------------------------------------------------ #


datos_id_genero = []
# Conexión a la base de datos utilizando SQLAlchemy
engine = create_engine(f"postgresql://{cr2.user}:{cr2.password}@{cr2.host}:{cr2.port}/{cr2.database}")
# Leer el DataFrame
df_read = pd.read_csv('../csv_s/csv_final_mix_to_db/csv_2024-04-02.csv')

query = '''SELECT id_juego,genero.id_genero,genero FROM public.genero_int
        INNER JOIN genero ON genero_int.id_genero = genero.id_genero
        '''
df_genero_bbdd = pd.read_sql(query, engine)


query = '''SELECT id_genero,genero from genero'''
df_gen_orig = pd.read_sql(query, engine)


for index, row in df_read.iterrows():
    # Obtener los idiomas de la fila actual
    generos = row['Genero'].split(',')
    for genero in generos:
        genero = genero.strip()
        id_genero = df_gen_orig["id_genero"][df_gen_orig["genero"] == genero].values
        id_juego = row["id_juego"]
        datos_id_genero.append({"id_juego":id_juego,"id_genero":int(id_genero[0])})
df_nuevo_gen_int = pd.DataFrame(datos_id_genero)

nuevo_df = df_nuevo_gen_int[~df_nuevo_gen_int['id_juego'].isin(df_genero_bbdd['id_juego']) & ~df_nuevo_gen_int['id_genero'].isin(df_genero_bbdd['id_genero'])]

if not nuevo_df.empty:
    nuevo_df.to_sql(name='genero_int', con=engine, if_exists='append', index=False)
    
print(f"Numero de inserts en genero_int {len(nuevo_df)}")
engine.dispose()

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla precios ----------------- #
# ------------------------------------------------------------------------ #


# Cerrar la conexión

end_time = datetime.now()
total_time = end_time - start_time
print(f"Finalizado los inserts en {total_time}")