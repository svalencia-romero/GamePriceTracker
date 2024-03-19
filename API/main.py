import sys
sys.path.append("../")
import time
import bs4 as bs
import httpx
import json

from utils import funciones as f
from utils import clases as c
from utils import variables as v
from fastapi import FastAPI
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


app = FastAPI()

@app.get("/")
async def inicio():
    return {"Bienvenida": "Bienvenid@ a la API de juegos de PSN"}

@app.get("/cambios_monedas") # Idea de añadir otro input para así elegir que juegos escoger o que numero de juegos que se relacionen con esa busqueda
async def titulo(moneda:str): 
    
    driver,service,options = f.carga_driver()
    driver.get(v.link_google)
    barra_ = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'))
    WebDriverWait(driver, v.timeout).until(barra_)
    barra_busqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
    barra_busqueda.send_keys(moneda)
    next_page_number = EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[6]/div/div[12]/div[1]/div[2]/div[2]/div/div/div[1]/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/span[1]'))
    dato = next_page_number.get_attribute()
    return {f"Cambio_moneda_{moneda}": dato}
    
    
    
@app.get("/precios") # Idea de añadir otro input para así elegir que juegos escoger o que numero de juegos que se relacionen con esa busqueda
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

    # Seleccionamos juego
    try:
        # time.sleep(1.5)
        sel_game = EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/section/div/ul/li[1]/div/a/div/div/div[1]/span[2]/img[2]'))
        WebDriverWait(driver, v.timeout).until(sel_game)
        enl_game = driver.find_element(By.XPATH, '/html/body/div[3]/main/section/div/ul/li[1]/div/a/div/div/div[1]/span[2]/img[2]')
        enl_game.click()
    except TimeoutException:
        print(f"Timed out waiting for game to appear, game number {v.game}, número de intentos {v.intentos}")

    # Obtenemos la id del juego para poderla comparar con otras store
    
    dict_completo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-qa='mfeCtaMain#cta#action']")))
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
                precio_original_sn_psn = po_sn_psn_info.precios_y_otras_caracteristicas("Precio no disponible",)
                
                pa_sn_psn_info = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',0,'discountPriceFormatted']])
                precio_actual_sn_psn = pa_sn_psn_info.precios_y_otras_caracteristicas("Precio no disponible")
                
                pa_cn_psn_info = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',1,'discountPriceFormatted']])
                precio_actual_cn_psn = pa_cn_psn_info.precios_y_otras_caracteristicas("Precio no disponible")
                
                if precio_actual_cn_psn == "Precio no disponible":
                    precio_actual_cn_psn = precio_actual_sn_psn 
                
                #Precios para otras promos
                
                otras_promos = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',2,'discountPriceFormatted']])
                otra_promo = otras_promos.precios_y_otras_caracteristicas("No dispone de promoción extra")
                lbl_promo = c.info_game(soup,'button',[{'data-qa':'mfeCtaMain#cta#action'},'data-telemetry-meta',['productDetail',0,'productPriceDetail',2,'offerBranding']])
                label_promo = lbl_promo.precios_y_otras_caracteristicas("No dispone de promoción extra")
                
                
                precios.update({f"{title}_{i}":{f"Precios_juegos_{i}": [{'Precio_original':precio_original_sn_psn},{"Precio actual sin PSPlus":precio_actual_sn_psn},{f"Precio actual con PSPlus":precio_actual_cn_psn},{f"Precio con promo {label_promo}":otra_promo}]}})
                
        return precios



