
# ------------ SOLO EJECUTAR LA PRIMERA VEZ QUE SE INICIALIZA LA BASE DE DATOS --------------------- #

from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append("../")
from utils import cred_2 as cr2
from utils import funciones as f

df_read = pd.read_csv('../csv_s/csv_final_mix_to_db/csv_2024-04-02.csv')


conn = f.conect_bbdd(cr2.database, cr2.host, cr2.user, cr2.password, cr2.port)
cursor = conn.cursor()

# ------------------------------------------------------------------------ #
# ------------------------ Insertar regiones inicial --------------------- #
# ------------------------------------------------------------------------ #

list_regions = ["ESP","USA","JAP"]
for index, region in enumerate(list_regions):
        # Insertar en la tabla psn_region
        cursor.execute(f"INSERT INTO psn_region (region) VALUES ('{region}');")
        print("Insertado en psn_region:", region)

conn.commit()

# ------------------------------------------------------------------------ #
# ------------------------ Insertar suscripcion -------------------------- #
# ------------------------------------------------------------------------ #
list_offer = ["precio_original","oferta","oferta_psplus","precio_otras_promos"]
    
query = f'''INSERT INTO suscripcion (nombre_suscripcion,id_region) VALUES ('{list_offer[0]}',1),
            ('{list_offer[0]}',2),
            ('{list_offer[0]}',3),
            ('{list_offer[1]}',1),
            ('{list_offer[1]}',2),
            ('{list_offer[1]}',3),
            ('{list_offer[2]}',1),
            ('{list_offer[2]}',2),
            ('{list_offer[2]}',3),
            ('{list_offer[3]}',1),
            ('{list_offer[3]}',2),
            ('{list_offer[3]}',3)'''
cursor.execute(query)

        
conn.commit()
# ------------------------------------------------------------------------ #
# ------------------------ Insertar plataforma --------------------------- #
# ------------------------------------------------------------------------ #
for plataforma in df_read['Plataforma'].str.split(',').explode().str.strip().unique():
    # Verificar genero
    cursor.execute("SELECT COUNT(*) FROM plataforma WHERE nombre_plataforma = %s", (plataforma,))
    existe = cursor.fetchone()[0]
    
    # Si no esta en la tabla,inserta
    if existe == 0:
        cursor.execute("INSERT INTO plataforma (nombre_plataforma) VALUES (%s)", (plataforma,))
        conn.commit()
        
print("Los datos se insertaron correctamente.")

