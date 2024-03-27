import pandas as pd
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent # "fake_user_agent"
import psycopg2

def carga_driver():
    """

    Returns:
        _type_: _description_
    """
    service = Service(executable_path='../../psn_env/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    # options.add_argument('--start-maximized')  #SOLO EN PC SOBREMESA si fuera necesario.
    driver = webdriver.Chrome(service=service, options=options)
    return driver,service,options

def carga_pagina_inicial(driver:webdriver):
    '''
    En esta función estamos haciendo la carga de la página inicial donde más adelante,
    empezaremos a recoger información sobre todos los juegos de la plataforma
    
    argm:
        driver:webdriver
    
    ''' 
    timeout = 10


    try:
        butt_coo = EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/button/img'))
        WebDriverWait(driver, timeout).until(butt_coo)
    except TimeoutException:
        print("Timed out waiting for sort button to appear")

    rechazar_cookies = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/button/img')
    rechazar_cookies.click()
    driver.implicitly_wait(10)

    #vamos a la pestaña de explora

    try:
        expl_butt = EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div/ul/li[5]/a'))
        WebDriverWait(driver, timeout).until(expl_butt)
    except TimeoutException:
        print("Timed out waiting for sort button to appear")

    explora = driver.find_element(By.XPATH, '/html/body/div[3]/section/div/div/div/ul/li[5]/a')
    explora.click()
    

    #return

    # Si queremos ordenar en ascendente 
    # plat
    
    try:
        sort_butt = EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/div/section/div/div/div/div[4]/button'))
        WebDriverWait(driver, timeout).until(sort_butt)
    except TimeoutException:
        print("Timed out waiting for sort button to appear") 

    return
              
def pagina_concreta_carga(pagina:int,driver:webdriver):
    """Cargamos una página concreta para poder recuperar 
    la información que ha dado error y hemos perdido.

    Args:
        pagina (int): Pagina que queremos cargar
        driver (webdriver): driver 
    """
    pag = 1
    while pag != pagina:
        next_page = driver.find_element(By.XPATH,'/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/div/nav/button[2]')  
        next_page.click()
        pag += 1
        
    
def limpieza_df_es(df_webscrap:pd.DataFrame, df_webscrap_anterior:pd.DataFrame,var_dia:str,var_store:str)-> pd.DataFrame:
    """

    Args:
        df_webscrap (pd.DataFrame): Dataframe que estamos guardando con el web scrapping y queremos limpiar
        
    """
    

    #Aseguramos que no tenga titulos sin informacion
    
    lista_juegos_no_ok = list(df_webscrap["id_juego"][df_webscrap["Titulo"]=="No hay información"])
    for i in lista_juegos_no_ok:
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Titulo"]] = list(df_webscrap_anterior["Titulo"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Plataforma"]] = list(df_webscrap_anterior["Plataforma"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Genero"]] = list(df_webscrap_anterior["Genero"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Compañia"]] = list(df_webscrap_anterior["Compañia"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Lanzamiento"]] = list(df_webscrap_anterior["Lanzamiento"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Idiomas"]] = list(df_webscrap_anterior["Idiomas"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Calificación PSN"]] = list(df_webscrap_anterior["Calificación PSN"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Número de calificaciones"]] = list(df_webscrap_anterior["Número de calificaciones"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Calificación 5 estrellas"]] = list(df_webscrap_anterior["Calificación 5 estrellas"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Calificación 4 estrellas"]] = list(df_webscrap_anterior["Calificación 4 estrellas"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Calificación 3 estrellas"]] = list(df_webscrap_anterior["Calificación 3 estrellas"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Calificación 2 estrellas"]] = list(df_webscrap_anterior["Calificación 2 estrellas"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Calificación 1 estrella"]] = list(df_webscrap_anterior["Calificación 1 estrella"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Precio original sin PSN"]] = list(df_webscrap_anterior["Precio original sin PSN"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Precio actual sin PSN"]] = list(df_webscrap_anterior["Precio actual sin PSN"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Precio original con PSN"]] = list(df_webscrap_anterior["Precio original con PSN"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, ["Precio actual con PSN"]] = list(df_webscrap_anterior["Precio actual con PSN"][df_webscrap_anterior["id_juego"] == i])[0]
        df_webscrap.loc[df_webscrap["id_juego"] == i, "País Store"] = df_webscrap_anterior["País Store"][df_webscrap_anterior["id_juego"] == i]
    
    # Genero

    df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: x.split(','))
    df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: list(set(x)))
    df_webscrap["Genero"] = df_webscrap["Genero"].apply(lambda x: ','.join(x))

    # Fecha webscrap
    df_webscrap["Día y hora"] = pd.to_datetime(df_webscrap["Día y hora"])

    #Calificación del juego
    df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].str.replace("No hay información","0.00")
    df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].astype(float)

    #Fecha de lanzamiento
    df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace(r"^(.{1,6})$", "01/01/2024",regex=True)

    df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace("No hay información", "01/01/2000")
    df_webscrap["Lanzamiento"] = pd.to_datetime(df_webscrap["Lanzamiento"], dayfirst=True)

    #Idiomas
    df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: x.split(','))
    df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: list(set(x)))
    df_webscrap["Idiomas"] = df_webscrap["Idiomas"].apply(lambda x: ','.join(x))

    # Número calificaciones
    df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace("No hay información", "0 calificaciones").str.replace("Sin calificaciones", "0 calificaciones")

    df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.extract('(\d+)')

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


    # Calif_ estrellas
    df_webscrap["Calificación 5 estrellas"] = ((df_webscrap["Calificación 5 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
    df_webscrap["Calificación 4 estrellas"] = ((df_webscrap["Calificación 4 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
    df_webscrap["Calificación 3 estrellas"] = ((df_webscrap["Calificación 3 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
    df_webscrap["Calificación 2 estrellas"] = ((df_webscrap["Calificación 2 estrellas"]/100)*df_webscrap["Número de calificaciones"]).astype(int)
    df_webscrap["Calificación 1 estrella"] = ((df_webscrap["Calificación 1 estrella"]/100)*df_webscrap["Número de calificaciones"]).astype(int)

    #Precio actual sin Playstation Plus
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1")
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].str.replace(",",".")
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].astype(float)

    #Precio actual con Playstation Plus
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1")
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].str.replace(",",".")
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].astype(float)

    #Precio Original sin Playstation Plus
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1")
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].str.replace(",",".")
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].astype(float)

    #Precio Otiginal con Playstation Plus

    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.00").replace("Nodisponibleparacomprar","-1").replace('Anunciado',"-1")
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].str.replace(",",".")
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].fillna(df_webscrap["Precio original sin PSN"])
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].astype(float)


    df_webscrap.drop_duplicates(subset=['id_juego'], inplace=True)

    df_webscrap.to_csv(f"../csv_s/csv_limpio/{var_store}/csv_{var_dia}.csv",index=False)

    return 

def clean_mix_df(esp_df_clean:pd.DataFrame,usa_df_no_clean:pd.DataFrame,jap_df_no_clean:pd.DataFrame,var_dia:str):
    
    df_mix = esp_df_clean

    df_mix["Precio actual con PSN JP"] = jap_df_no_clean["Precio actual con PSN"]
    df_mix["Precio actual con PSN USA"] = usa_df_no_clean["Precio actual con PSN"]

    df_mix["Precio actual sin PSN JP"] = jap_df_no_clean["Precio actual con PSN"]
    df_mix["Precio actual sin PSN USA"] = usa_df_no_clean["Precio actual con PSN"]

    df_mix["Precio original JP"] = jap_df_no_clean["Precio original sin PSN"]
    df_mix["Precio original USA"] = usa_df_no_clean["Precio original sin PSN"]


    df_mix.rename(columns={'Precio original sin PSN':'Precio original ESP','Precio actual con PSN':'Precio actual con PSN ESP','Precio actual sin PSN':'Precio actual sin PSN ESP'},inplace=True)

    df_mix.drop(["País Store"],axis=1,inplace=True)
    df_mix.drop(['Precio original con PSN'],axis=1,inplace=True)

    df_mix = df_mix[['id_juego', 'Titulo', 'Día y hora', 'Plataforma', 'Genero', 'Compañia', 'Lanzamiento', 'Idiomas',
            'Calificación PSN', 'Número de calificaciones', 'Calificación 5 estrellas', 'Calificación 4 estrellas',
            'Calificación 3 estrellas', 'Calificación 2 estrellas', 'Calificación 1 estrella',
            'Precio original ESP', 'Precio actual sin PSN ESP',
            'Precio actual con PSN ESP', 'Precio original JP', 'Precio actual sin PSN JP', 'Precio actual con PSN JP',
            'Precio original USA', 'Precio actual sin PSN USA', 'Precio actual con PSN USA']]

    # df_mix["Día y hora"] = pd.to_datetime(df_mix["Día y hora"])
    # df_mix["Lanzamiento"] = pd.to_datetime(df_mix["Lanzamiento"], dayfirst=True)

    df_mix["Precio actual sin PSN JP"] = df_mix["Precio actual sin PSN JP"].str.replace("No hay información","0.00")
    df_mix["Precio actual sin PSN JP"] = df_mix["Precio actual sin PSN JP"].str.replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1")
    df_mix["Precio actual sin PSN JP"] = df_mix["Precio actual sin PSN JP"].str.replace('¥','')
    df_mix["Precio actual sin PSN JP"] = df_mix["Precio actual sin PSN JP"].str.replace(",","")
    df_mix["Precio actual sin PSN JP"] = df_mix["Precio actual sin PSN JP"].astype(float)

    df_mix["Precio actual con PSN JP"] = df_mix["Precio actual con PSN JP"].str.replace("No hay información","0.00")
    df_mix["Precio actual con PSN JP"] = df_mix["Precio actual con PSN JP"].replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1")
    df_mix["Precio actual con PSN JP"] = df_mix["Precio actual con PSN JP"].str.replace('¥','')
    df_mix["Precio actual con PSN JP"] = df_mix["Precio actual con PSN JP"].str.replace(",","")
    df_mix["Precio actual con PSN JP"] = df_mix["Precio actual con PSN JP"].astype(float)

    df_mix["Precio original JP"] = df_mix["Precio original JP"].str.replace("No hay información","0.00")
    df_mix["Precio original JP"] = df_mix["Precio original JP"].replace('無料','0.00').replace("含まれます","0.00").replace("購入できません","-1").replace('発表されました',"-1")
    df_mix["Precio original JP"] = df_mix["Precio original JP"].str.replace('¥','')
    df_mix["Precio original JP"] = df_mix["Precio original JP"].str.replace(",","")
    df_mix["Precio original JP"] = df_mix["Precio original JP"].astype(float)

    df_mix["Precio actual sin PSN USA"] = df_mix["Precio actual sin PSN USA"].str.replace("No hay información","0.00")
    df_mix["Precio actual sin PSN USA"] = df_mix["Precio actual sin PSN USA"].str.replace('Free','0.00').replace("Included","0.00").replace("Not available for purchase","-1").replace('Announced',"-1")
    df_mix["Precio actual sin PSN USA"] = df_mix["Precio actual sin PSN USA"].str.replace('$','')
    df_mix["Precio actual sin PSN USA"] = df_mix["Precio actual sin PSN USA"].astype(float)

    df_mix["Precio actual con PSN USA"] = df_mix["Precio actual con PSN USA"].str.replace("No hay información","0.00")
    df_mix["Precio actual con PSN USA"] = df_mix["Precio actual con PSN USA"].str.replace('Free','0.00').replace("Included","0.00").replace("Not available for purchase","-1").replace('Announced',"-1")
    df_mix["Precio actual con PSN USA"] = df_mix["Precio actual con PSN USA"].str.replace('$','')
    df_mix["Precio actual con PSN USA"] = df_mix["Precio actual con PSN USA"].astype(float)

    df_mix["Precio original USA"] = df_mix["Precio original USA"].str.replace("No hay información","0.00")
    df_mix["Precio original USA"] = df_mix["Precio original USA"].str.replace('Free','0.00').replace("Included","0.00").replace("Not available for purchase","-1").replace('Announced',"-1")
    df_mix["Precio original USA"] = df_mix["Precio original USA"].str.replace('$','')
    df_mix["Precio original USA"] = df_mix["Precio original USA"].astype(float)

    df_mix.to_csv(f"../csv_s/csv_mix_price_id_es/csv_{var_dia}.csv",index=False) # Convertimos a csv para pasar a bbdd

def numero_de_juegos(driver,numero=False):
    if numero != False:
       numero_juegos = numero
    elif numero == False:
        page_source = driver.page_source
        soup_numero_juegos = bs(page_source, 'html.parser')
        numero_juegos = soup_numero_juegos.find('div', class_= "ems-sdk-active-filters psw-m-b-8 psw-m-t-4").get_text()
        numero_juegos = re.findall(r"\d+",numero_juegos)
        numero_juegos = int(numero_juegos[0])
    else:
        print("No cargan los numeros de juegos")
    return numero_juegos

def conect_bbdd(database,host,user,password,port):
    
    conn = psycopg2.connect(database=database,
                        host=host,
                        user=user,
                        password=password,
                        port=port)
    return conn

def sql_query(query,conn):

    cursor = conn.cursor()

    # Ejecuta la query
    cursor.execute(query)

    # Almacena los datos de la query 
    ans = cursor.fetchall()

    # Obtenemos los nombres de las columnas de la tabla
    names = [description[0] for description in cursor.description]

    cursor.close()
    conn.close()

    return pd.DataFrame(ans,columns=names)
    
def verificar_valores_nulos(csv):
    df = pd.read_csv(csv)  
      
    if df.isnull().values.any():
        print(f"El archivo '{csv}' tiene valores nulos.")
    else:
        print(f"El archivo '{csv}' no tiene valores nulos.")