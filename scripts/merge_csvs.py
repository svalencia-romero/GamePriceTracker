import pandas as pd

date = input("¿Que fecha quieres limpiar? (Formato : yyyy-mm-dd)")

df_es = pd.read_csv(f"../csv_s/csv_region/esp/clean/csv_{date}_esp.csv")
df_us = pd.read_csv(f"../csv_s/csv_region/usa/clean/csv_{date}_usa.csv")
df_jp = pd.read_csv(f"../csv_s/csv_region/jap/clean/csv_{date}_jap.csv")

# Primero mezclamos la store Japonesa con la española y vemos si los ids coinciden y añadimos precios
df_merge = pd.merge(df_es,df_jp[['id_juego','Precio original', 'Oferta', 'Oferta PSPlus', 'Otra promo diferente a PSPLUS']],how='left', on= 'id_juego', suffixes=('','_jp'))

df_not_found = df_jp[~df_jp['id_juego'].isin(df_es['id_juego'])]
df_not_found = df_not_found.rename(columns= {'Precio original':'Precio original_jp','Oferta':'Oferta_jp','Oferta PSPlus':'Oferta PSPlus_jp','Otra promo diferente a PSPLUS':'Otra promo diferente a PSPLUS_jp'})
df_union = pd.concat([df_merge, df_not_found], ignore_index=True)

# Una vez tenemos la union de esp y jap, mezclamos estas dos con la de usa

df_merge = pd.merge(df_union,df_us[['id_juego','Precio original', 'Oferta', 'Oferta PSPlus', 'Otra promo diferente a PSPLUS']],how='left', on= 'id_juego', suffixes=('','_us'))

df_not_found = df_us[~df_us['id_juego'].isin(df_union['id_juego'])]
df_not_found = df_not_found.rename(columns= {'Precio original':'Precio original_us','Oferta':'Oferta_us','Oferta PSPlus':'Oferta PSPlus_us','Otra promo diferente a PSPLUS':'Otra promo diferente a PSPLUS_us'})
df_union = pd.concat([df_merge, df_not_found], ignore_index=True)

# Ya tendremos en df union mezcladas las 3 stores, ahora hay que limpiar los valores nulos de todas las columnas

df_union.fillna(-1,inplace=True) # Al final como tenemos en nuestra leyenda, si no hay valores de oferta es igual a -1

# Dejamos las columnas preparadas para la insercion en nuestra db
df_union = df_union.rename(columns= {'Precio original':'Precio original_es','Oferta':'Oferta_es','Oferta PSPlus':'Oferta PSPlus_es','Otra promo diferente a PSPLUS':'Otra promo diferente a PSPLUS_es'})
df_union.to_csv(f"../csv_s/csv_final_mix_to_db/csv_{date}.csv",index=False)