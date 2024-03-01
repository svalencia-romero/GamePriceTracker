"""
Importamos las librerias necesarias para hacer nuestro webscrapping
"""
import clases as c
import variables as v
import funciones as f
import re # Expresiones regulares 
import time
import requests
import pandas as pd
from datetime import datetime
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# MEJORANDO EL SCRAPEO CON CLASES Y FUNCIONES INTEGRADAS

### PRUEBA FUNCIONAL WEBSCRAPING DE X JUEGOS Y TIEMPO UTILIZADO ###

ua = UserAgent()
driver,service,options = f.carga_driver()


df_juegos = pd.DataFrame(columns=["id_juego","Titulo","Día y hora","Plataforma","Genero","Compañia",
                                "Lanzamiento","Idiomas","Calificación PSN","Número de calificaciones","Calificación 5 estrellas",
                                "Calificación 4 estrellas","Calificación 3 estrellas","Calificación 2 estrellas",
                                "Calificación 1 estrella","Precio original sin PSN","Precio actual sin PSN","Precio original con PSN","Precio actual con PSN"]) #,"Precio con mayor rebaja"


driver.get(v.link_inicial)
f.carga_pagina_inicial(driver)
numero_juegos = f.numero_de_juegos(driver,400) # Llamamos a los números de juegos que necesitamos de manera concreta, en caso de no poner juegos saltamos a poner todos los juegos.

while numero_juegos != len(df_juegos):
    try:
        try:
            sel_game = EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/ul/li[{v.game+1}]/div/a'))
            WebDriverWait(driver, v.timeout).until(sel_game)
        except TimeoutException:
            print(f"Timed out waiting for game to appear, game number {v.game}")
            
        driver.implicitly_wait(10)
        
        try:
            url = driver.current_url  
            headers = {'User-Agent': ua.random}
            response = requests.get(url, headers=headers)
            soup_pagina_entera = bs(response.text,features="lxml")
            url_game = soup_pagina_entera.select_one(f'[data-qa="ems-sdk-grid#productTile{v.game}"] a')
            href_valor = url_game.get('href')
            link_juego = v.link_inicial + href_valor
        # obtenemos info del juego         
            headers = {'User-Agent': ua.random}
            response = requests.get(link_juego, headers=headers)
            soup = bs(response.text,features="lxml")
            
        except Exception as e:
            print(f"Error al obtener la URL: error en el juego{v.game}, página{v.page}")
            
        
        # Aquí vamos a coger el soup de cada url de cada juego para obtener la info
        
        driver.implicitly_wait(10)
        #Titulo e id del juego  
      
        #Titulo e id del juego 
        title_info = c.info_game(soup,"h1",[{"class":"psw-m-b-5 psw-t-title-l psw-t-size-6 psw-l-line-break-word"},
                                    {"class":"psw-m-b-5 psw-t-title-l psw-t-size-7 psw-l-line-break-word"},
                                    {"class":"psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word"}])

        id_juego = re.findall(r"\d+",href_valor)
        id_juego = int(id_juego[0])
        titulo = title_info.caracteristica_tipo("Error al recoger el título")
        # Día y hora de webscrappeo
        
        fecha_webs = datetime.now()
        fecha_webs = datetime.isoformat(fecha_webs)
        
        # Precio original sin PSN
        
        org_price_without_psn = c.info_game(soup,"span",[{"class":"psw-t-title-s psw-c-t-2 psw-t-strike"},
                                                    {"class":"psw-t-title-m"}])
        precio_original_sn_psn = org_price_without_psn.caracteristica_tipo("Error al recoger precio original sin psn")

        # Precio original con PSN
        
        org_price_with_psn = c.info_game(soup,"span",[{'data-qa':'mfeCtaMain#offer1#originalPrice','class':'psw-t-title-s psw-c-t-2 psw-t-strike'},
                                                    {"class":"psw-t-title-s psw-c-t-2 psw-t-strike"},{"class":"psw-t-title-m"}])
        precio_original_cn_psn = org_price_with_psn.caracteristica_tipo("Error al recoger precio original con psn")

        # Precio actual sin PSN
        
        act_price_without_psn = c.info_game(soup,"span",[{'class':"psw-t-title-m psw-m-r-4"},{"class":"psw-t-title-m"}])
        precio_actual_sn_psn = act_price_without_psn.caracteristica_tipo("Error al recoger precio actual sin psn")

        # Precio actual con PSN
        
        act_price_with_psn = c.info_game(soup,"span",[{'data-qa':'mfeCtaMain#offer1#finalPrice','class':'psw-t-title-m psw-m-r-4'},
                                                    {'class':"psw-t-title-m psw-m-r-4"},{"class":"psw-t-title-m"}])
        precio_actual_cn_psn = act_price_with_psn.caracteristica_tipo("Error al recoger precio original con psn")

        #Plataforma
        
        pltform = c.info_game(soup,"dd",[{'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max',
                                    'data-qa':'gameInfo#releaseInformation#platform-value'}])
        plataforma = pltform.caracteristica_tipo("Error al recoger plataforma")

        # Genero
        
        gnr = c.info_game(soup,"dd",[{'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max',
                                    'data-qa':'gameInfo#releaseInformation#genre-value'}])
        genero = gnr.caracteristica_tipo("Error al recoger género")

        # Compañia
        
        company = c.info_game(soup,"dd",[{'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max',
                                        'data-qa':'gameInfo#releaseInformation#publisher-value'}])
        compania = company.caracteristica_tipo("Error al recoger la compañia")

        # Lanzamiento
        
        lanz = c.info_game(soup,"dd",[{'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max',
                                    'data-qa':'gameInfo#releaseInformation#releaseDate-value'}])
        lanzamiento = lanz.caracteristica_tipo("Error al recoger Lanzamiento")
        
        # Idiomas
        
        lng = c.info_game(soup,"dd",[{'class':'psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max',
                                    'data-qa':'gameInfo#releaseInformation#subtitles-value'}])
        idiomas = lng.caracteristica_tipo("Error al recoger Idiomas")

        # Nº de calificaciones

        num_cal = c.info_game(soup,"span",[{'class':'psw-c-t-2 psw-t-secondary',
                                        'data-qa':'mfe-star-rating#overall-rating#total-ratings'}])
        num_calificaciones = num_cal.caracteristica_tipo("Error al recoger num calificaciones")
        
        # Calificación PSN
        
        cal_psn = c.info_game(soup,"div",[{'class':'psw-t-subtitle psw-t-bold psw-l-line-center','data-qa':'mfe-game-title#average-rating'}])
        calificacion = cal_psn.caracteristica_tipo("Error al recoger Calificación PSN")
        
        # Calificaciones por estrellas

        cal_stars = c.info_game(soup,"span",[{'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress1#percentage-label'},
                                    {'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress2#percentage-label'},
                                    {'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress3#percentage-label'},
                                    {'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress4#percentage-label'},
                                    {'class':'psw-t-body','data-qa':'mfe-star-rating#overall-rating#rating-progress5#percentage-label'}])

        list_stars = cal_stars.caracteristica_tipo("Error al obtener calificaciones por estrella",cal=True)
        calificacion_1 = list_stars[0]
        calificacion_2 = list_stars[1]
        calificacion_3 = list_stars[2]
        calificacion_4 = list_stars[3]
        calificacion_5 = list_stars[4]    
        
        
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
        print("contador real",v.contador_juegos_real,"contador_en_df",v.game,v.page)
        v.contador_juegos_real += 1
        v.game += 1

        #Comprobar error aquí
        if v.game == 24:
            next_page = driver.find_element(By.XPATH,'/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/div/nav/button[2]')  
            next_page.click()
            v.page += 1      
            v.game = 0
        elif len(df_juegos) == v.limite:
            # Volvemos a hacer la carga completa de la pagina
            driver.quit()
            time.sleep(5)
            driver,service,options = f.carga_driver()
            f.carga_pagina_inicial(driver)
            f.pagina_concreta_carga(v.page,driver)
            limite = limite + 300
            print("Número de juegos completados de webscrapear", str(len(df_juegos)))
            continue
        # elif numero_juegos == len(df_juegos):
        #     break
        else:
            continue
    except:
        # Volvemos a hacer la carga completa de la página
        print(f"Error en la carga juego {v.game}, página {v.page}")
        # Guardamos los errores en una lista
        list_error = []
        list_error.append((v.game,v.page))
        driver.quit()
        
        driver,service,options = f.carga_driver()
        time.sleep(5)
        f.carga_pagina_inicial(driver)
        f.pagina_concreta_carga(v.page,driver)
        v.game += 1
                  
driver.quit()

fecha_acabado = str(datetime.now())
df_juegos_limpio = f.limpieza_df(df_juegos)
# df_juegos_limpio.to_csv(f"../csv_s/csv_{fecha_acabado[:10]}.csv",index=False)
df_juegos_limpio.to_csv("../csv_s/csv_prueba_new_code.csv",index=False) # Convertir a csv para pruebas