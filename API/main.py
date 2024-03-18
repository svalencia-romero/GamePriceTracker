import sys
sys.path.append("../")
from utils import funciones as f
from utils import clases as c
from utils import variables as v
from fastapi import FastAPI
import bs4 as bs
from fake_useragent import UserAgent
import httpx
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = FastAPI()

@app.get("/")
async def inicio():
    return {"Bienvenida": "Bienvenid@ a la API de juegos"}
 
@app.get("/titulo")
async def titulo(busqueda:str):
    
    # Cargamos página inicial
    driver,service,options = f.carga_driver()
    driver.get(v.link_inicial)
    f.carga_pagina_inicial(driver)
    
    # Cargamos cuadro de busqueda
    search = driver.find_element(By.XPATH,'/html/body/div[2]/header/div/section/span/span/button')
    search.click()
    barra_busqueda = driver.find_element(By.XPATH,'/html/body/div[7]/div/div/div/div[2]/input')
    barra_busqueda.send_keys(busqueda)
    
    try:
        sel_game = EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/ul/li[1]/div/a'))
        WebDriverWait(driver, v.timeout).until(sel_game)
    except TimeoutException:
        print(f"Timed out waiting for game to appear, game number {v.game}, número de intentos {v.intentos}")
    
    response = driver.page_source

    url_game_element = driver.find_element(By.CSS_SELECTOR, f'[data-qa="ems-sdk-grid#productTile0"] a')
    href_store_es = url_game_element.get_attribute('href')
    id_game = href_store_es.replace('https://store.playstation.com/es-es/concept/', '')
    
    # id = "228748" # Añadimos el id necesario para coger el titulo que la obtenemos con el otro webscrap, hacemos prueba con un numero concreto
    
    ua = UserAgent()
    url = f"https://store.playstation.com/es-es/concept/{id_game}" 
    async with httpx.AsyncClient() as client:
        headers = {'User-Agent': ua.random}
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            soup = bs.BeautifulSoup(response.text, features="lxml")
            title = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word").get_text()
            return {"title": title}
        else:
            return {"error": "No se pudo acceder al sitio web"}