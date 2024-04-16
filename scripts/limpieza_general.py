import pandas as pd

# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#

# Limpieza usa

date = input("¿Que fecha quieres limpiar? (Formato : yyyy-mm-dd)")


df_webscrap = pd.read_csv(f"../csv_s/csv_region/usa/brut/csv_{date}_usa.csv")

df_webscrap.drop(df_webscrap[df_webscrap["Precio original"] == "No hay información"].index,inplace=True)
df_webscrap.drop_duplicates(subset=["id_juego"], inplace=True)
df_webscrap.drop(df_webscrap[df_webscrap["Titulo"] == "No hay información"].index,inplace=True)

df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: x.split(','))
df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: list(set(x)))
df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: ','.join(x))

df_webscrap["Día y hora"] = pd.to_datetime(df_webscrap["Día y hora"])

df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].str.replace("No hay información","0.00")
df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].astype(float)

df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace(r"^(.{1,6})$", "01/01/2024",regex=True)
df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace("No hay información", "01/01/2000")
df_webscrap["Lanzamiento"] = pd.to_datetime(df_webscrap["Lanzamiento"])

df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: x.split(','))
df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: list(set(x)))
df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: ','.join(x))

df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace("No hay información", "0")
df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.extract('(\d+)') #en caso de necesitar 
df_webscrap["Número de calificaciones"].fillna(0,inplace=True)
df_webscrap["Número de calificaciones"]  = df_webscrap["Número de calificaciones"].astype(int)


#  Calificación 5 estrellas convertido a float
df_webscrap["Calificación 5 estrellas"] = df_webscrap["Calificación 5 estrellas"].str.replace("%",'').str.replace(".","")
df_webscrap["Calificación 5 estrellas"] = df_webscrap["Calificación 5 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 4 estrellas convertido a float
df_webscrap["Calificación 4 estrellas"] = df_webscrap["Calificación 4 estrellas"].str.replace("%",'').str.replace(".","")
df_webscrap["Calificación 4 estrellas"] = df_webscrap["Calificación 4 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 3 estrellas convertido a float
df_webscrap["Calificación 3 estrellas"] = df_webscrap["Calificación 3 estrellas"].str.replace("%",'').str.replace(".","")
df_webscrap["Calificación 3 estrellas"] = df_webscrap["Calificación 3 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 2 estrellas convertido a float
df_webscrap["Calificación 2 estrellas"] = df_webscrap["Calificación 2 estrellas"].str.replace("%",'').str.replace(".","")
df_webscrap["Calificación 2 estrellas"] = df_webscrap["Calificación 2 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 1 estrella convertido a float
df_webscrap["Calificación 1 estrella"] = df_webscrap["Calificación 1 estrella"].str.replace("%",'').str.replace(".","")
df_webscrap["Calificación 1 estrella"] = df_webscrap["Calificación 1 estrella"].str.replace("No hay información", "0").astype(int)

df_webscrap["Calificación 5 estrellas"] = ((df_webscrap["Calificación 5 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 4 estrellas"] = ((df_webscrap["Calificación 4 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 3 estrellas"] = ((df_webscrap["Calificación 3 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 2 estrellas"] = ((df_webscrap["Calificación 2 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 1 estrella"] = ((df_webscrap["Calificación 1 estrella"]/100)*df_webscrap["Número de calificaciones"]).astype(int)

df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace("No hay información","-1")
df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace('Free','0.00')
df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace('$','')
df_webscrap["Precio original"] = df_webscrap["Precio original"].astype(float)

df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace("No hay información","-1")
df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace('Free','0.00').replace("Included","0.00")
df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace('$','')
df_webscrap["Oferta"] = df_webscrap["Oferta"].astype(float)

df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace("No hay información","-1")
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace("Included","0.00").replace('Game Trial','0.5')
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace('$','')
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].astype(float)

df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace("No hay otra promoción","-1")
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace("Included","0.00").replace('Game Trial','0.5')
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace('$','')
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].astype(float)

df_webscrap.to_csv(f"../csv_s/csv_region/usa/clean/csv_{date}_usa.csv",index=False)



# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#

# Limpieza jp

df_webscrap = pd.read_csv(f"../csv_s/csv_region/jap/brut/csv_{date}_jap.csv")

df_webscrap.drop(df_webscrap[df_webscrap["Precio original"] == "No hay información"].index,inplace=True)
df_webscrap.drop_duplicates(subset=["id_juego"], inplace=True)
df_webscrap.drop(df_webscrap[df_webscrap["Titulo"] == "No hay información"].index,inplace=True)

df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: x.split(','))
df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: list(set(x)))
df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: ','.join(x))

df_webscrap["Día y hora"] = pd.to_datetime(df_webscrap["Día y hora"])

df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].str.replace("No hay información","0.00")
df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].astype(float)

df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace(r"^(.{1,6})$", "2024/01/01",regex=True)
df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace("No hay información", "2000/01/01")
df_webscrap["Lanzamiento"] = pd.to_datetime(df_webscrap["Lanzamiento"])

df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: x.split(','))
df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: list(set(x)))
df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: ','.join(x))

df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace("No hay información", "0")
df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.extract('(\d+)') #en caso de necesitar 
df_webscrap["Número de calificaciones"].fillna(0,inplace=True)
df_webscrap["Número de calificaciones"]  = df_webscrap["Número de calificaciones"].astype(int)


#  Calificación 5 estrellas convertido a float
df_webscrap["Calificación 5 estrellas"] = df_webscrap["Calificación 5 estrellas"].str.replace("％",'').str.replace(".","")
df_webscrap["Calificación 5 estrellas"] = df_webscrap["Calificación 5 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 4 estrellas convertido a float
df_webscrap["Calificación 4 estrellas"] = df_webscrap["Calificación 4 estrellas"].str.replace("％",'').str.replace(".","")
df_webscrap["Calificación 4 estrellas"] = df_webscrap["Calificación 4 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 3 estrellas convertido a float
df_webscrap["Calificación 3 estrellas"] = df_webscrap["Calificación 3 estrellas"].str.replace("％",'').str.replace(".","")
df_webscrap["Calificación 3 estrellas"] = df_webscrap["Calificación 3 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 2 estrellas convertido a float
df_webscrap["Calificación 2 estrellas"] = df_webscrap["Calificación 2 estrellas"].str.replace("％",'').str.replace(".","")
df_webscrap["Calificación 2 estrellas"] = df_webscrap["Calificación 2 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 1 estrella convertido a float
df_webscrap["Calificación 1 estrella"] = df_webscrap["Calificación 1 estrella"].str.replace("％",'').str.replace(".","")
df_webscrap["Calificación 1 estrella"] = df_webscrap["Calificación 1 estrella"].str.replace("No hay información", "0").astype(int)

df_webscrap["Calificación 5 estrellas"] = ((df_webscrap["Calificación 5 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 4 estrellas"] = ((df_webscrap["Calificación 4 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 3 estrellas"] = ((df_webscrap["Calificación 3 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 2 estrellas"] = ((df_webscrap["Calificación 2 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 1 estrella"] = ((df_webscrap["Calificación 1 estrella"]/100)*df_webscrap["Número de calificaciones"]).astype(int)

df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace("No hay información","-1")
df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1").replace('ゲームトライアル','0.5')
df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace('¥','')
df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace(",","")
df_webscrap["Precio original"] = df_webscrap["Precio original"].astype(float)

df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace("No hay información","-1")
df_webscrap["Oferta"] = df_webscrap["Oferta"].replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1").replace('ゲームトライアル','0.5')
df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace('¥','')
df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace(",","")
df_webscrap["Oferta"] = df_webscrap["Oferta"].astype(float)

df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace("No hay información","-1")
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1").replace('ゲームトライアル','0.5')
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace('¥','')
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace(",","")
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].astype(float)

df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace("No hay información","0.00").replace("No hay otra promoción","-1")
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1").replace('ゲームトライアル','0.5')
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace('¥','')
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace(",","")
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].astype(float)

df_webscrap.to_csv(f"../csv_s/csv_region/jap/clean/csv_{date}_jap.csv",index=False)

# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
# Limpieza csv esp

df_webscrap = pd.read_csv(f"../csv_s/csv_region/esp/brut/csv_{date}_esp.csv")

df_webscrap.drop(df_webscrap[df_webscrap["Precio original"] == "No hay información"].index,inplace=True)
df_webscrap.drop_duplicates(subset=["id_juego"], inplace=True)
df_webscrap.drop(df_webscrap[df_webscrap["Titulo"] == "No hay información"].index,inplace=True)

df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: x.split(','))
df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: list(set(x)))
df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: ','.join(x))

df_webscrap["Día y hora"] = pd.to_datetime(df_webscrap["Día y hora"])

df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].str.replace("No hay información","0.00")
df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].astype(float)

df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace(r"^(.{1,6})$", "01/01/2024",regex=True)
df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace("No hay información", "01/01/2000")
df_webscrap["Lanzamiento"] = pd.to_datetime(df_webscrap["Lanzamiento"], dayfirst=True)

df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: x.split(','))
df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: list(set(x)))
df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: ','.join(x))

df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace("No hay información", "0")
df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.extract('(\d+)') #en caso de necesitar 
df_webscrap["Número de calificaciones"].fillna(0,inplace=True)
df_webscrap["Número de calificaciones"]  = df_webscrap["Número de calificaciones"].astype(int)


#  Calificación 5 estrellas convertido a float
df_webscrap["Calificación 5 estrellas"] = df_webscrap["Calificación 5 estrellas"].str.replace(" %",'').str.replace(".","")
df_webscrap["Calificación 5 estrellas"] = df_webscrap["Calificación 5 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 4 estrellas convertido a float
df_webscrap["Calificación 4 estrellas"] = df_webscrap["Calificación 4 estrellas"].str.replace(" %",'').str.replace(".","")
df_webscrap["Calificación 4 estrellas"] = df_webscrap["Calificación 4 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 3 estrellas convertido a float
df_webscrap["Calificación 3 estrellas"] = df_webscrap["Calificación 3 estrellas"].str.replace(" %",'').str.replace(".","")
df_webscrap["Calificación 3 estrellas"] = df_webscrap["Calificación 3 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 2 estrellas convertido a float
df_webscrap["Calificación 2 estrellas"] = df_webscrap["Calificación 2 estrellas"].str.replace(" %",'').str.replace(".","")
df_webscrap["Calificación 2 estrellas"] = df_webscrap["Calificación 2 estrellas"].str.replace("No hay información", "0").astype(int)
#  Calificación 1 estrella convertido a float
df_webscrap["Calificación 1 estrella"] = df_webscrap["Calificación 1 estrella"].str.replace(" %",'').str.replace(".","")
df_webscrap["Calificación 1 estrella"] = df_webscrap["Calificación 1 estrella"].str.replace("No hay información", "0").astype(int)

df_webscrap["Calificación 5 estrellas"] = ((df_webscrap["Calificación 5 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 4 estrellas"] = ((df_webscrap["Calificación 4 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 3 estrellas"] = ((df_webscrap["Calificación 3 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 2 estrellas"] = ((df_webscrap["Calificación 2 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
df_webscrap["Calificación 1 estrella"] = ((df_webscrap["Calificación 1 estrella"]/100)*df_webscrap["Número de calificaciones"]).astype(int)


df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1").replace("Nohayinformacin","-1")
df_webscrap["Precio original"] = df_webscrap["Precio original"].str.replace(",",".")
df_webscrap["Precio original"] = df_webscrap["Precio original"].astype(float)


df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1").replace("Nohayinformacin","-1")
df_webscrap["Oferta"] = df_webscrap["Oferta"].str.replace(",",".")
df_webscrap["Oferta"] = df_webscrap["Oferta"].astype(float)


df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1").replace('Pruebadejuego','0.5').replace("Nohayinformacin","-1")
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].str.replace(",",".")
df_webscrap["Oferta PSPlus"] = df_webscrap["Oferta PSPlus"].astype(float)


df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1").replace('Pruebadejuego','0.5').replace("Nohayotrapromocin","-1").replace("Nohayinformacin","-1")
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].str.replace(",",".")
df_webscrap["Otra promo diferente a PSPLUS"] = df_webscrap["Otra promo diferente a PSPLUS"].astype(float)

df_webscrap.to_csv(f"../csv_s/csv_region/esp/clean/csv_{date}_esp.csv",index=False)

