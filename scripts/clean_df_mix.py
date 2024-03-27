import sys
import pandas as pd
sys.path.append("../")
import time
from utils import funciones as f

decision = ""

while decision != "q":
    print('¿Qué operación quieres hacer?:','\n',
          '1 - Limpieza de datos de juegos españoles','\n',
          '2 - Fusión datos limpios esp, con usa y jap','\n',
          '3 - Comprobar valores nulos en un csv','\n',
          'q - Salir de script')
    time.sleep(3)
    decision = input(' 1 / 2 / 3 ')
    

    if decision == "1":
        var_dia = input("¿Que día quieres limpiar?: (year-mt-dy)")
        var_store = input("")
        try:
            df_webscrap_anterior = pd.read_csv("../csv_s/csv_sin_limpiar/csv_2024-03-25_es.csv" ) # tener un data set que este sin limpiar del día anterior 
            df_webscrap = pd.read_csv(f"../csv_s/csv_sin_limpiar/csv_{var_dia}_{var_store}.csv" )
            f.limpieza_df_es(df_webscrap,df_webscrap_anterior,var_dia,var_store)
            print("Limpieza realizda con exito")
        except:
            print("Limpieza con errores")

    elif decision == "2":
        
        var_dia = input("¿Que día quieres mezclar?: (year-mt-dy)")
        try:

            df_webscrap_es = pd.read_csv(f"../csv_s/csv_limpio/{var_store}/csv_{var_dia}.csv")
            df_webscrap_usa = pd.read_csv(f"../csv_s/csv_sin_limpiar/csv_{var_dia}_us.csv")
            df_webscrap_jp = pd.read_csv(f"../csv_s/csv_sin_limpiar/csv_{var_dia}_jp.csv")

            f.clean_mix_df(df_webscrap_es,df_webscrap_usa,df_webscrap_jp)
            print("Mezcla datos esp-usa-jap ok")
        except:
                print("Errores al mezclar")

    elif decision == "3":
        try:
            ruta = input("Especifica la ruta exacta de tu csv":)
            f.verificar_valores_nulos(ruta)
        except:
            print("Error en ruta")
    else:
        print("Elige algo que se pueda elegir")

print("Fin del script")
