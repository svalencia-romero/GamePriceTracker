import snowflake.connector
import snowflake.sqlalchemy
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append("../")
# from utils import cred as cr
from utils import cred_snow as cr_snw
from utils import funciones as f

start_time = datetime.now()
# Leer el DataFrame
date = input("¿Que fecha quieres insertar? (Formato : yyyy-mm-dd)")
df_read = pd.read_csv(f"../csv_s/csv_final_mix_to_db/csv_{date}.csv")



list_genero = ['Genero','genero','genero']
list_idioma = ['Idiomas','lang_disp','nombre_lang']
list_compania = ['Compañia','compania','nombre_compania']
list_id_carac = ['id_compania','id_lang','id_genero']
list_tab_int = ['id_juego','lang_disp_int','id_lang','genero_int','id_genero']

conn = snowflake.connector.connect(
    user=cr_snw.user,
    password=cr_snw.password,
    account=cr_snw.account,
    warehouse=cr_snw.warehouse,
    database=cr_snw.database,
    schema=cr_snw.schema
)
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


conn.commit()
cursor.close()
conn.close()

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla info_juego ----------------- #
# ------------------------------------------------------------------------ #

# Conexión a la base de datos utilizando SQLAlchemy
# engine = create_engine(f"postgresql://{cr_aws.user}:{cr_aws.password}@{cr_aws.host}:{cr_aws.port}/{cr_aws.database}")
engine = create_engine(
    f'snowflake://{cr_snw.user}:{cr_snw.password}@{cr_snw.account}/{cr_snw.database}/{cr_snw.schema}?warehouse={cr_snw.warehouse}')

# Pruebas de snow- -----------------------
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
print(f"Se insertan {len(df_rename_info_juegos[~df_rename_info_juegos['id_juego'].isin(df_id_juego_bbdd['id_juego'])])} juegos en info_juego")

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla compania_int ---------------- #
# ------------------------------------------------------------------------ #
datos_id_compan = []
# Conexión a la base de datos utilizando SQLAlchemy
engine = create_engine(
    f'snowflake://{cr_snw.user}:{cr_snw.password}@{cr_snw.account}/{cr_snw.database}/{cr_snw.schema}?warehouse={cr_snw.warehouse}')
# Leer el DataFrame


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

print(f"Número de inserts en plat_int {len(df_nuevo_plat_int[~df_nuevo_plat_int['id_juego'].isin(df_plat_bbdd['id_juego'])])}")

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla lang_disp_int ----------------- #
# ------------------------------------------------------------------------ #

datos_id_lang = []

# Leer el DataFrame


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

df_nuevo_lang_int = df_nuevo_lang_int[~df_nuevo_lang_int['id_juego'].isin(df_lang_bbdd['id_juego']) & ~df_nuevo_lang_int['id_lang'].isin(df_lang_bbdd['id_lang'])]

if not df_nuevo_lang_int.empty:
    df_nuevo_lang_int.to_sql(name='lang_disp_int', con=engine, if_exists='append', index=False)

print(f"Numero de inserts en lang_disp_int {len(df_nuevo_lang_int)}")

# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla genero_int ----------------- #
# ------------------------------------------------------------------------ #


datos_id_genero = []



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


# ------------------------------------------------------------------------ #
# ---------------- Insertar datos en la tabla precios ----------------- #
# ------------------------------------------------------------------------ #
df_esp_original = df_read[["id_juego","Día y hora","Precio original_es"]]
df_usa_original = df_read[["id_juego","Día y hora","Precio original_us"]]
df_jap_original = df_read[["id_juego","Día y hora","Precio original_jp"]]
df_esp_oferta = df_read[["id_juego","Día y hora","Oferta_es"]]
df_usa_oferta = df_read[["id_juego","Día y hora","Oferta_us"]]
df_jap_oferta = df_read[["id_juego","Día y hora","Oferta_jp"]]
df_esp_psplus = df_read[["id_juego","Día y hora","Oferta PSPlus_es"]]
df_usa_psplus = df_read[["id_juego","Día y hora","Oferta PSPlus_us"]]
df_jap_psplus = df_read[["id_juego","Día y hora","Oferta PSPlus_jp"]]
df_esp_otrapromo = df_read[["id_juego","Día y hora","Otra promo diferente a PSPLUS_es"]]
df_usa_otrapromo = df_read[["id_juego","Día y hora","Otra promo diferente a PSPLUS_us"]]
df_jap_otrapromo = df_read[["id_juego","Día y hora","Otra promo diferente a PSPLUS_jp"]]

df_esp_original  = df_esp_original.rename(columns={"Día y hora":"fecha_webs","Precio original_es":"precio"})
df_usa_original= df_usa_original.rename(columns={"Día y hora":"fecha_webs","Precio original_us":"precio"})
df_jap_original= df_jap_original.rename(columns={"Día y hora":"fecha_webs","Precio original_jp":"precio"})
df_esp_oferta = df_esp_oferta.rename(columns={"Día y hora":"fecha_webs","Oferta_es":"precio"})
df_usa_oferta = df_usa_oferta.rename(columns={"Día y hora":"fecha_webs","Oferta_us":"precio"})
df_jap_oferta = df_jap_oferta.rename(columns={"Día y hora":"fecha_webs","Oferta_jp":"precio"})
df_esp_psplus= df_esp_psplus.rename(columns={"Día y hora":"fecha_webs","Oferta PSPlus_es":"precio"})
df_usa_psplus= df_usa_psplus.rename(columns={"Día y hora":"fecha_webs","Oferta PSPlus_us":"precio"})
df_jap_psplus= df_jap_psplus.rename(columns={"Día y hora":"fecha_webs","Oferta PSPlus_jp":"precio"})
df_esp_otrapromo= df_esp_otrapromo.rename(columns={"Día y hora":"fecha_webs","Otra promo diferente a PSPLUS_es":"precio"})
df_usa_otrapromo= df_usa_otrapromo.rename(columns={"Día y hora":"fecha_webs","Otra promo diferente a PSPLUS_us":"precio"})
df_jap_otrapromo= df_jap_otrapromo.rename(columns={"Día y hora":"fecha_webs","Otra promo diferente a PSPLUS_jp":"precio"})

df_esp_original["id_suscripcion"] = 1
df_usa_original["id_suscripcion"] = 2
df_jap_original["id_suscripcion"] = 3
df_esp_oferta["id_suscripcion"] = 4
df_usa_oferta["id_suscripcion"] = 5
df_jap_oferta["id_suscripcion"] = 6
df_esp_psplus["id_suscripcion"] = 7
df_usa_psplus["id_suscripcion"] = 8
df_jap_psplus["id_suscripcion"] = 9
df_esp_otrapromo["id_suscripcion"] = 10
df_usa_otrapromo["id_suscripcion"] = 11
df_jap_otrapromo["id_suscripcion"] = 12

lista_precios = [df_esp_original,df_usa_original,df_jap_original,df_esp_oferta,df_usa_oferta,df_jap_oferta,df_esp_psplus,df_usa_psplus,df_jap_psplus,df_esp_otrapromo,df_usa_otrapromo,df_jap_otrapromo]

lista_precios = [df_esp_original,df_usa_original,df_jap_original,df_esp_oferta,df_usa_oferta,df_jap_oferta,df_esp_psplus,df_usa_psplus,df_jap_psplus,df_esp_otrapromo,df_usa_otrapromo,df_jap_otrapromo]
query = '''SELECT id_juego,fecha_webs,precio from precio'''
df_total_precios = pd.read_sql(query, engine)
df_total_precios

for clave,precios in enumerate(lista_precios):
    
    precios.to_sql(name='precio', con=engine, if_exists='append', index=False)
    
    print(f"Se han insertado {len(precios)} precios de la lista {clave+1}")
   


# Cerrar la conexión
engine.dispose()
end_time = datetime.now()
total_time = end_time - start_time
print(f"Finalizado los inserts en {total_time}")