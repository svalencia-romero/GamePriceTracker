![portada](/misc/readme.jpg)
## Game Price Tracker
### Comparativa de precios en diferentes tiendas de PSN a lo largo del tiempo, y actualmente a través de webscraping.
#### Descripción del Proyecto
Este proyecto consiste en una aplicación web desarrollada en Streamlit. Su objetivo es proporcionar precios en tiempo real de juegos disponibles en tres tiendas diferentes (ESP-USA-JAP).  
Además, la aplicación mostrará la evolución del precio de cada juego a lo largo del tiempo.  

El desarrollo se llevará a cabo en varias fases:  

### --  1ª Fase --  Fase de desarrollo principal  (En desarrollo)
- Crear una API con FastAPI que realice webscraping en tiempo real de precios de una búsqueda específica del usuario, cambio de moneda y criterios específicos de juegos alojados en un servidor PostGreSQL (Elephant).
- Realizar webscraping diario de las 3 tiendas en línea, comparando los precios de la tienda española con la estadounidense y la japonesa para ver la relación de precios en el tiempo de un juego o varios (alrededor de 8500 juegos aproximadamente).
- Desarrollar una primera WebAPP hecha en Streamlit para mostrar estadísticas de esta primera etapa.  

### -- 2ª Fase -- Optimización de recursos y código
- Optimizar los tiempos de webscraping, tanto los de la propia API como las obtenciones diarias de cada juego.
- Optimizar las busquedas de los juegos en tiempo real.  

### -- Fases posteriores -- 

- Implementar nuevas funcionalidades
- Implementar otras plataformas


#### Estructura del Repositorio
* API: Desarrollada con FastApi, tendremos los nombres del juego que queramos comprobar y sus precios en tiempo real, además de otras funcionalidades.
* app: Desarrollo de web APP (Streamlit).
* csv_s: Contiene archivos CSV que se han obtenido mediante webscraping.
* notebooks: Jupyter Notebooks con información principal de las caracteristicas del proyecto.
* pruebas: Directorio de pruebas donde se van almacenando los archivos que son descartados.
* scripts: Scripts de utilidad para hacer webscraping en las páginas deseadas.
* utils:  Archivos .py, clases, funciones y variables necesarias para que nuestro código funcione correctamente.

#### Notas Adicionales
Por favor, ten en cuenta que este proyecto está en desarrollo y algunas características pueden no estar completamente implementadas o funcionales.

Este proyecto ha sido desarrollado por [Santiago Valencia Romero](https://www.linkedin.com/in/santiago-valencia-romero/)

---

### Price comparison across different PSN stores over time, and currently through webscraping.
#### Project Description
This project consists of a web application developed in Streamlit. Its goal is to provide real-time prices of games available in three different stores (ESP-USA-JAP).  
Additionally, the application will display the price evolution of each game over time.

The development will take place in several phases: 

### -- Phase 1 -- Main Development Phase (In Progress)
- Create an API with FastAPI that performs real-time webscraping of prices for a specific user search, currency conversion, and game-specific criteria hosted on a PostGreSQL server (Elephant).
- Perform daily webscraping of the 3 online stores, comparing prices from the Spanish store with the American and Japanese ones to observe the price relationship over time for one or more games (approximately 8500 games).
- Develop a first WebAPP made in Streamlit to display statistics from this initial stage.  

### -- Phase 2 -- Resource and Code Optimization
- Optimize webscraping times, both for the API itself and daily data retrievals for each game.
- Improve real-time game searches.  

### -- Subsequent Phases --

- Implement new functionalities.
- Implement other platforms.


#### Repository Structure
* API: Developed with FastAPI, it will have the names of the games we want to check and their real-time prices.
* app:  Development of the web APP (Streamlit).
* csv_s: Contains CSV files obtained through webscraping.
* notebooks: Jupyter Notebooks with primary information about the project's characteristics.
* pruebas: Test directory where discarded files are stored.
* scripts: Utility scripts for webscraping desired pages.
* utils:  .py files, classes, functions, and necessary variables for our code to work correctly.

#### Additional Notes
Please note that this project is in development and some features may not be fully implemented or functional.

This project has been developed by [Santiago Valencia Romero](https://www.linkedin.com/in/santiago-valencia-romero/)

