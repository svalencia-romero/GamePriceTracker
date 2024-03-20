![portada](/psn_offer/img/readme.jpeg)
## Comparativa de precios en diferentes tiendas de PSN en el tiempo, y en la actualidad a traves de webscraping.
#### Descripción del Proyecto
Este proyecto consiste en una aplicación web desarrollada en Streamlit. Su objetivo es proporcionar precios en tiempo real de juegos disponibles en tres tiendas diferentes (ESP-USA-JAP).  
Además, la aplicación mostrará la evolución del precio de cada juego a lo largo del tiempo.  

Todo el desarrollo se desarrollara en varias fases:  

### --  1ª Fase --  Fase de desarrollo principal
- Realizar una API con FastAPI que webscrapea en tiempo real precios de una busqueda concreta del usuario, cambio de moneda y criterios concretos de juegos alojada en un servidor PostGreSQL(Elephant).
- Realizar webscrapeo diario de las 3 tiendas online, comparando los precios de la store Española con la Americana y la Japonesa para ver la relación de precio en el tiempo de un juego o de varios (Alrededor de 8500 juegos aproximadamente).
- Realizar una primera WebAPP hecha en Streamlit para mostrar estadisticos de esta primera etapa.  

### -- 2ª Fase -- Optimización de recursos y código
- Optimizar los tiempos de webscraping, tanto los de la propia API como las obtenciones diarias de cada juego.
- Optimizar las busquedas de los juegos en tiempo real.  

### -- Fases posteriores -- 

- Implementar nuevas funcionalidades
- Implementar otras plataformas


#### Estructura del Repositorio
* API: Desarrollada con FastApi, tendremos los nombres del juego que queramos comprobar y sus precios en tiempo real.
* app: Funcionan los filtros de búsqueda. Se está considerando una nueva forma de mostrar los precios. (Última actualización ayer).
* csv_s: Contiene archivos CSV que se han ido web scrapeando.
* notebooks: Jupyter Notebooks con información principal de las caracteristicas del proyecto.
* pruebas: Directorio de pruebas donde se van almacenando los archivos que son descartados.
* scripts: Scripts de utilidad para web scrapear las páginas que queremos
* utils: Archivos .py , clases funciones y variables necesarias para que nuestro codigo funcione correctamente

#### Notas Adicionales
Por favor, ten en cuenta que este proyecto está en desarrollo y algunas características pueden no estar completamente implementadas o funcionales.

Este proyecto ha sido desarrollado por [Santiago Valencia Romero](https://www.linkedin.com/in/santiago-valencia-romero/)



