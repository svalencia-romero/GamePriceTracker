"""
Importamos las librerias necesarias para hacer nuestro webscrapping
"""
import funciones as f
import re # Expresiones regulares 
import time
import requests
import pandas as pd
from datetime import datetime

# import variables as v
# import random

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
"fake_user_agent"

service = Service(executable_path='../../psn_env/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe')
options = webdriver.ChromeOptions()
# options.add_argument('--start-maximized') SOLO EN PC SOBREMESA si fuera necesario.



# MEJORANDO EL SCRAPEO IDENTIFICANDO EL SOURCE Y OBTENIENDO TODOS LOS DATOS DE ELLA

### PRUEBA FUNCIONAL WEBSCRAPING DE X JUEGOS Y TIEMPO UTILIZADO ### Completamente funcional, pocos campos, meter más cosas genero etc... (Prueba con timeouts en vez de random choice de tiempos)
# Reset df



ua = UserAgent()
service = Service(executable_path='../../psn_env/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
timeout = 10

df_juegos = pd.DataFrame(columns=["id_juego","Titulo","Día y hora","Plataforma","Genero","Compañia",
                                "Lanzamiento","Idiomas","Calificación PSN","Número de calificaciones","Calificación 5 estrellas",
                                "Calificación 4 estrellas","Calificación 3 estrellas","Calificación 2 estrellas",
                                "Calificación 1 estrella","Precio original sin PSN","Precio actual sin PSN","Precio original con PSN","Precio actual con PSN"]) #,"Precio con mayor rebaja"

driver = webdriver.Chrome(service=service, options=options)

link_inicial = "https://store.playstation.com/"
driver.get(link_inicial)


lista_tiempo = [3,3.1,3.2]

f.carga_pagina_inicial(driver)

# Mostrar un numero de juegos limitado para que no nos salte error de maximo numero de intentos.
limite = 300 # limite de juegos que se van multiplicando por 2 max abajo para poder ir recopilando la info

'''
Aquí tenemos el código para meter de manera automatica el limite del numero de juegos
Si queremos limitar el numero de juegos comentar las 5 lineas siguiente para comprobar que el flujo está correcto.

'''

# page_source = driver.page_source
# soup_numero_juegos = bs(page_source, 'html.parser')
# numero_juegos = soup_numero_juegos.find('div', class_= "ems-sdk-active-filters psw-m-b-8 psw-m-t-4").get_text()
# numero_juegos = re.findall(r"\d+",numero_juegos)
# numero_juegos = int(numero_juegos[0])
# print(numero_juegos)
numero_juegos = 500


contador_juegos_real = 1 # Esta linea está creada para comprobar que el flujo de los cambios de páginas con sus juegos está correcto.
# seleccion de juego
page = 1
game = 0 # Establecemos el primer juego que estará en cont = 1, pero lo establecemos en 0 para iniciarlo
while numero_juegos != len(df_juegos):
    try:
        try:
            sel_game = EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/ul/li[{game+1}]/div/a'))
            WebDriverWait(driver, timeout).until(sel_game)
        except TimeoutException:
            print(f"Timed out waiting for game to appear, game number {game}")
            
        driver.implicitly_wait(10)
        
        try:
            url = driver.current_url  
            headers = {'User-Agent': ua.random}
            response = requests.get(url, headers=headers)
            soup_pagina_entera = bs(response.text,features="lxml")
            url_game = soup_pagina_entera.select_one(f'[data-qa="ems-sdk-grid#productTile{game}"] a')
            href_valor = url_game.get('href')
            link_juego = link_inicial + href_valor
        # obtenemos info del juego         
            headers = {'User-Agent': ua.random}
            response = requests.get(link_juego, headers=headers)
            soup = bs(response.text,features="lxml")
            
        except Exception as e:
            print(f"Error al obtener la URL: error en el juego{game}, página{page}")
            
        
        # Aquí vamos a coger el soup de cada url de cada juego para obtener la info
        
        driver.implicitly_wait(10)
        #Titulo e id del juego  
      
        try: #Intentamos primero con un tipo de letra
            titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word").get_text()
            id_juego = re.findall(r"\d+",href_valor)
            id_juego = int(id_juego[0])
            
        except: #Intentamos después con otro tipo de letra
            try:
                titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-7 psw-l-line-break-word").get_text()
                id_juego = re.findall(r"\d+",href_valor)
                id_juego = int(id_juego[0])
            except:
                titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-6 psw-l-line-break-word").get_text()
                id_juego = re.findall(r"\d+",href_valor)
                id_juego = int(id_juego[0])
        # Día y hora de webscrappeo
        
        fecha_webs = datetime.now()
        fecha_webs = datetime.isoformat(fecha_webs)
        
            
        # Precio original sin PSN
        try:
            precio_original_sn_psn = soup.find("span",class_="psw-t-title-s psw-c-t-2 psw-t-strike").get_text() 
        except:
            precio_original_sn_psn = soup.find("span",class_="psw-t-title-m").get_text()
            
        # Precio original con PSN
        try:
            precio_original_cn_psn = soup.find("span",attrs={'data-qa':'mfeCtaMain#offer1#originalPrice','class':'psw-t-title-s psw-c-t-2 psw-t-strike'}).get_text()
        except: 
            try:
                precio_original_cn_psn = soup.find("span",attrs={'class':'psw-truncate-text-1 psw-p-t-1 psw-l-exclude@desktop'}).get_text()
            except:
                precio_original_cn_psn = precio_original_sn_psn
                
        # Precio actual sin PSN
        try:
            precio_actual_sn_psn = soup.find("span",class_="psw-t-title-m psw-m-r-4").get_text()
        except:
            precio_actual_sn_psn = precio_original_sn_psn
        
        #Precio Actual con PSN
        try:
            precio_actual_cn_psn = soup.find("span",attrs={'data-qa':'mfeCtaMain#offer1#finalPrice','class':'psw-t-title-m psw-m-r-4'}).get_text()
        except: 
            try:
                precio_actual_cn_psn = soup.find("span",class_="psw-t-title-m psw-m-r-4").get_text()
            except: 
                precio_actual_cn_psn = precio_actual_sn_psn
        
        # Plataforma
        try:
            plataforma = soup.find("dd", attrs={'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max','data-qa':'gameInfo#releaseInformation#platform-value'}).get_text()
        except:
            plataforma = "No hay información"
        
        # Genero
        try:
            genero = soup.find("dd", attrs={'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max','data-qa':'gameInfo#releaseInformation#genre-value'}).get_text()
        except:
            genero = "No hay información"
        
        # Compañia
        try:
            compania = soup.find("dd", attrs={'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max','data-qa':'gameInfo#releaseInformation#publisher-value'}).get_text()
        except:
            compania = "No hay información"
        
        # Lanzamiento
        try:  
            lanzamiento = soup.find("dd", attrs={'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max','data-qa':'gameInfo#releaseInformation#releaseDate-value'}).get_text()
        except:
            lanzamiento = "No hay información"
        
        # Idiomas
        try:
            idiomas = soup.find("dd", attrs={'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max','data-qa':'gameInfo#releaseInformation#subtitles-value'}).get_text()
        except:
            idiomas = "No hay información"
        # Nº Calificaciones
        try:
            num_calificaciones = soup.find("span", attrs={'class':'psw-c-t-2 psw-t-secondary','data-qa':'mfe-star-rating#overall-rating#total-ratings'}).get_text()
        except:
            num_calificaciones = "No hay información"
        # Calificación PSN
        
        try:
            calificacion = soup.find("div", attrs={'class':'psw-t-subtitle psw-t-bold psw-l-line-center','data-qa':'mfe-game-title#average-rating'}).get_text()
        except:
            calificacion = "No hay información"
        try:
            calificacion_1 = soup.find("span", attrs={'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress1#percentage-label'}).get_text()
        except:
            calificacion_1 = "No hay información"
        try:
            calificacion_2 = soup.find("span", attrs={'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress2#percentage-label'}).get_text()
        except:
            calificacion_2 = "No hay información"
        try:
            calificacion_3 = soup.find("span", attrs={'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress3#percentage-label'}).get_text()
        except:
            calificacion_3 = "No hay información"
        try:
            calificacion_4 = soup.find("span", attrs={'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress4#percentage-label'}).get_text()
        except:
            calificacion_4 = "No hay información"
        try:
            calificacion_5 = soup.find("span", attrs={'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress5#percentage-label'}).get_text()
        except:
            calificacion_5 = "No hay información"
        
        # precio_con_mayor_rebaja = "No hay información"
        
        # Inserto valores en cada columna
        df_juegos.loc[len(df_juegos)] = {"id_juego":id_juego,"Titulo":titulo,"Día y hora":fecha_webs,"Plataforma":plataforma,"Genero":genero,"Compañia":compania,"Lanzamiento":lanzamiento,
                                        "Idiomas":idiomas,"Calificación PSN":calificacion,"Número de calificaciones":num_calificaciones,
                                        "Calificación 5 estrellas":calificacion_5,
                                        "Calificación 4 estrellas":calificacion_4,"Calificación 3 estrellas":calificacion_3,
                                        "Calificación 2 estrellas":calificacion_2,"Calificación 1 estrella":calificacion_1,
                                        "Precio original sin PSN":precio_original_sn_psn,"Precio actual sin PSN":precio_actual_sn_psn,"Precio original con PSN":precio_original_cn_psn, "Precio actual con PSN":precio_actual_cn_psn}
                                        # "Precio con mayor rebaja":precio_con_mayor_rebaja 
        
        # time.sleep(random.choice(lista_tiempo))
        # chequeo juegos
        print("contador real",contador_juegos_real,"contador_en_df",game,page)
        contador_juegos_real += 1
        game += 1

        #Comprobar error aquí
        if game == 24:
            next_page = driver.find_element(By.XPATH,'/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/div/nav/button[2]')  
            next_page.click()
            page += 1      
            game = 0
            # time.sleep(random.choice(lista_tiempo))
        elif len(df_juegos) == limite:
            # Volvemos a hacer la carga completa de la pagina
            driver.quit()
            time.sleep(5)
            driver = webdriver.Chrome(service=service, options=options)
            service = Service(executable_path='../../psn_env/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe')
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver.get("https://store.playstation.com/")
            f.carga_pagina_inicial(driver)
            f.pagina_concreta_carga(page,driver)
            limite = limite + 300
            print("Número de juegos completados de webscrapear", str(len(df_juegos)))
            continue
        # elif numero_juegos == len(df_juegos):
        #     break
        else:
            continue
    except:
        # Volvemos a hacer la carga completa de la pagina
        print(f"Error en la carga juego {game}, pagina {page}")
        list_error = []
        list_error.append((game,page))
        driver.quit()
        driver = webdriver.Chrome(service=service, options=options)
        service = Service(executable_path='../../psn_env/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver.get("https://store.playstation.com/")
        f.carga_pagina_inicial(driver)
        f.pagina_concreta_carga(page,driver)
        game += 1
                  
driver.quit()





fecha_acabado = str(datetime.now())
df_juegos_limpio = f.limpieza_df(df_juegos)
df_juegos_limpio.to_csv(f"../csv_s/csv_{fecha_acabado[:10]}.csv",index=False)