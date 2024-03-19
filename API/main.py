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
        time.sleep(1.5)
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
            
            if response.status_code == 200:

                soup = bs.BeautifulSoup(response.text, features="lxml")
                dict_completo = soup.find('button',attrs={'data-qa':'mfeCtaMain#cta#action'}).get_attribute_list('data-telemetry-meta')[0]
                conv_json = json.loads(dict_completo)
                try:
                    title = conv_json['productDetail'][0]['productName']
                except:
                    title = "No definido"
                try:
                    precio_original_sn_psn = conv_json['productDetail'][0]['productPriceDetail'][0]['originalPriceFormatted']
                except:
                    precio_original_sn_psn = "Precio no disponible"

                try:   
                    precio_actual_sn_psn = conv_json['productDetail'][0]['productPriceDetail'][0]['discountPriceFormatted']
                except:
                    precio_actual_sn_psn = "Precio no disponible"
                try:
                    precio_actual_cn_psn = conv_json['productDetail'][0]['productPriceDetail'][1]['discountPriceFormatted'] # Precio actual con PSN u otro servicio
                except:
                    precio_actual_cn_psn = precio_actual_sn_psn
                
                precios.update({f"{title}_{i}":{f"Precios_juegos_{i}": [precio_original_sn_psn,precio_actual_sn_psn,precio_actual_cn_psn]}})
                
        return precios
 