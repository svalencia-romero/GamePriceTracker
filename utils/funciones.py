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
        
    
def limpieza_df(df_webscrap:pd.DataFrame)-> pd.DataFrame:
    """

    Args:
        df_webscrap (pd.DataFrame): Dataframe que estamos guardando con el web scrapping y queremos limpiar
        
    """
    
    # Genero
    df_webscrap["Genero"] = df_webscrap["Genero"].str.replace(" ","")
    df_webscrap["Genero"] = df_webscrap["Genero"].str.replace("Juegosderol","Rol").str.replace("Juegosdedisparos","Shooter").str.replace("Juegosdedisparos","Shooter")
    df_webscrap["Genero"] = df_webscrap["Genero"].str.split(r'[^A-zÀ-ÿ_ ]')
    
    #Plataforma
    df_webscrap["Plataforma"] = df_webscrap["Plataforma"].str.replace(" ","")
    df_webscrap["Plataforma"] = df_webscrap["Plataforma"].str.split(r'[^0-9A-zÀ-ÿ_ ]')
    
    #Numero de calificaciones
    df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace('[A-z]','0', regex = True)
    df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace(" calificaciones",'').str.replace(".","")
    df_webscrap["Número de calificaciones"] = df_webscrap["Número de calificaciones"].str.replace("No hay información", "0").astype(int)

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
    df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].str.replace("No hay información",'0') 

    #Precio actual sin Playstation Plus
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.02").replace("Nodisponibleparacomprar","0.01").replace('Anunciado',"0.03")
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].str.replace(",",".")
    df_webscrap["Precio actual sin PSN"] = df_webscrap["Precio actual sin PSN"].astype(float)

    #Precio actual con Playstation Plus
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.02").replace("Nodisponibleparacomprar","0.01").replace('Anunciado',"0.03")
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].str.replace(",",".")
    df_webscrap["Precio actual con PSN"] = df_webscrap["Precio actual con PSN"].astype(float)

    #Precio Original sin Playstation Plus
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.02").replace("Nodisponibleparacomprar","0.01").replace('Anunciado',"0.03")
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].str.replace(",",".")
    df_webscrap["Precio original sin PSN"] = df_webscrap["Precio original sin PSN"].astype(float)

    #Precio Otiginal con Playstation Plus
    
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].str.replace("No hay información","0.00")
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].str.replace('[^0-9,A-z]','', regex = True).replace('Gratis','0.00').replace("Incluido","0.02").replace("Nodisponibleparacomprar","0.01").replace('Anunciado',"0.03")
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].str.replace(",",".")
    df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].fillna(df_webscrap["Precio original sin PSN"])
    # df_webscrap["Precio original con PSN"] = df_webscrap["Precio original con PSN"].astype(float)

    

    # id de cada juego que es unico
    df_webscrap["id_juego"] = df_webscrap["id_juego"].astype(str)
    df_webscrap["id_juego"] = df_webscrap["id_juego"].astype(int)

    #Fecha de lanzamiento
    df_webscrap["Lanzamiento"] = df_webscrap["Lanzamiento"].str.replace("No hay información", "01/01/2000")
    df_webscrap["Lanzamiento"] = pd.to_datetime(df_webscrap["Lanzamiento"], dayfirst=True)

    #Día y hora del momento
    df_webscrap["Día y hora"] = pd.to_datetime(df_webscrap["Día y hora"])

    #Calificación del juego
    df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].str.replace("No hay información","0.00")
    df_webscrap["Calificación PSN"] = df_webscrap["Calificación PSN"].astype(float)
    
    return df_webscrap

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



    