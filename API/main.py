import sys
sys.path.append("../")
import bs4 as bs
import httpx
import json
import time
from utils import funciones as f
from utils import clases as c
from utils import variables as v
from fastapi import FastAPI
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




tags_metadata = [
    {
        "name": "Inicio",
        "description": "Bienvenida",
    },
    {
        "name": "monedas",
        "description": "Devuelve el cambio a Euros de la moneda concreta que queramos, para luego en streamlit hacer el cambio de precio de cada juego",
    },
    {
        "name": "precios",
        "description": "Devuelve precios de juego id psn España en otras stores en tiempo real",
    
    }, 
    
]
app = FastAPI(title="PSN OFFER WBSCRP",
              summary= 'API con FastAPI que webscrapea en tiempo real precios de una busqueda concreta del usuario, cambio de moneda y criterios concretos de juegos',
                version="0.2",openapi_tags=tags_metadata)



@app.get("/", tags=['Inicio'])
async def inicio():
    return {"Bienvenida": "Bienvenid@ a la API de juegos de PSN"}

@app.get("/cambios_monedas/" ,tags=['monedas']) # Idea de añadir otro input para así elegir que juegos escoger o que numero de juegos que se relacionen con esa busqueda
async def titulo(moneda:str, ): 
    
    driver,service,options = f.carga_driver()
    driver.get(v.link_google)
    datos = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[1]/div')))
    datos.click()
    
    barra_busqueda = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')))
    barra_busqueda.send_keys(moneda)
    barra_busqueda.submit()
    
    dato_ = WebDriverWait(driver, v.timeout).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="DFlfde SwHCTb"]')))
    dato = dato_.text
    return {f"Cambio_moneda_{moneda}": dato}
    
    
    
@app.get("/precios/", tags=['precios']) # Idea de añadir otro input para así elegir que juegos escoger o que numero de juegos que se relacionen con esa busqueda
async def titulo(busqueda:str):
    
    # Cargamos página inicial
    driver,service,options = f.carga_driver()
    driver.get(v.link_inicial)
    f.carga_pagina_inicial(driver)

    # Cargamos cuadro de busqueda
    search_ = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/header/div/section/span/span/button'))
    WebDriverWait(driver, v.timeout).until(search_)
    search = driver.find_element(By.XPATH,'/html/body/div[2]/header/div/section/span/span/button')
    search.click()

    #Cargamos barra
    barra_ = EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div/div[2]/input'))
    WebDriverWait(driver, v.timeout).until(barra_)
    barra_busqueda = driver.find_element(By.XPATH,'/html/body/div[7]/div/div/div/div[2]/input')
    barra_busqueda.send_keys(busqueda)
    click_barra = driver.find_element(By.XPATH,'/html/body/div[7]/div/div/div/button[2]')
    click_barra.click()
    
    
    #######
    # Seleccionamos juego  Todo este codigo esta probado y funciona en ocasiones, hay que ver el flujo y si las variables se reinician         
    # anunciado = True
    # while anunciado: # Chequeamos que no es un anunciado ya que no tenemos datos de ello
            
    #     sel_game = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/main/section/div/ul/li[{v.game+1}]/div/a/div/div/div[1]/span[2]/img[2]')))
    #     sel_game.click()
        
    #     texto_1 = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div/div/label/div/span/span/span')))
    #     texto_1 = texto_1.text
    #     print(texto_1)
    #     try: # Además del anunciado, vemos si el id es correcto
    #         dict_completo = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, "//button[@data-qa='mfeCtaMain#cta#action']")))
    #         data_telemetry_meta = dict_completo.get_attribute('data-telemetry-meta')
    #         id_game = json.loads(data_telemetry_meta)['conceptId']
    #         print(id_game)
    #     except:
    #         id_game = 'No hay id'
        
    #     if texto_1 == 'Anunciado' or id_game == 'No hay id':
    #         print('Entra condicional')
    #         v.game += 1
    #         driver.back()
    #         print("sale if")
    #         continue
    #     else:
    #         print("entra else")
    #         anunciado = False
    #         print("sale else")
    #         break
            
    # print('Pasamos bucle')
    ########

    
    # # Obtenemos la id del juego para poderla comparar con otras store
    sel_game = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/main/section/div/ul/li[{v.game+1}]/div/a/div/div/div[1]/span[2]/img[2]')))
    sel_game.click()
    dict_completo = WebDriverWait(driver, v.timeout).until(EC.presence_of_element_located((By.XPATH, "//button[@data-qa='mfeCtaMain#cta#action']")))
    data_telemetry_meta = dict_completo.get_attribute('data-telemetry-meta')
    id_game = json.loads(data_telemetry_meta)['conceptId']
    driver.quit()
            
    ua = UserAgent()
    region_es = 'es-es'
    region_us = 'en-us'
    region_jp = 'ja-jp'
    list_region = [region_es,region_us,region_jp] 
    
    async with httpx.AsyncClient() as client:
        precios = {}
        for i in list_region:
            
            url = f"https://store.playstation.com/{i}/concept/{id_game}"
            headers = {'User-Agent': ua.random}
            response = await client.get(url, headers=headers)
            soup = bs.BeautifulSoup(response.text, features="lxml")
            
            if response.status_code == 200:
                
                title_info = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productName']])
                title = title_info.precios_y_otras_caracteristicas("Precio no disponible")
                
                po_sn_psn_info = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',0,'originalPriceFormatted']])
                precio_original_sn_psn = po_sn_psn_info.precios_y_otras_caracteristicas("No hay información")
                                
                pa_sn_psn_info = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',0,'discountPriceFormatted']])
                promo_1 = pa_sn_psn_info.precios_y_otras_caracteristicas("No hay información")
                                
                pa_cn_psn_info = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',1,'discountPriceFormatted']])
                promo_2 = pa_cn_psn_info.precios_y_otras_caracteristicas("No hay información")
                
                lbl_psn = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',1,'offerBranding']]) 
                label_promo_2 = lbl_psn.precios_y_otras_caracteristicas("No hay información")
                
                otras_promos = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',2,'discountPriceFormatted']])
                promo_3 = otras_promos.precios_y_otras_caracteristicas("No dispone de promoción extra") 
                lbl_promo = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',2,'offerBranding']]) 
                label_promo_3 = lbl_promo.precios_y_otras_caracteristicas("No hay información") 

                if label_promo_2 == 'PS_PLUS':
                    label2 = 'PS_PLUS'
                    promo_plus = promo_2 
                elif label_promo_3 == 'PS_PLUS':
                    label2 = 'PS_PLUS'
                    promo_plus = promo_3    
                else:
                    label2 = 'PS_PLUS'
                    promo_plus = "No hay promoción"

                if (label_promo_2 == 'EA_ACCESS') or (label_promo_2 == 'UBISOFT_PLUS'):
                    otra_promo = promo_2
                    label3 = label_promo_2
                elif (label_promo_3 == 'EA_ACCESS') or (label_promo_3 == 'UBISOFT_PLUS'):
                    otra_promo = promo_3
                    label3 = label_promo_3
                else:
                    otra_promo = "No hay promoción"
                    label3 = "No hay otra promoción"  
                        
                
                precios.update({f"{title}_{i}":{f"Precios_juegos_{i}": [{'Precio_original':precio_original_sn_psn},{"Precio actual":promo_1},{f"Precio actual con {label2}":promo_plus},{f"Precio con promo {label3}":otra_promo}]}})
                
        return precios



