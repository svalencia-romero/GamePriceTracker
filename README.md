## Comparativa de precios en diferentes tiendas de PSN en el tiempo, y en la actualidad a traves de webscraping.
#### Descripción del Proyecto
Este proyecto consiste en una aplicación web desarrollada con Streamlit. Su objetivo es proporcionar precios en tiempo real de juegos disponibles en tres tiendas diferentes. Además, la aplicación mostrará la evolución del precio de cada juego a lo largo del tiempo.  
1. En una primera fase, hemos querido hacer un dashboard de los mejores precios en el tiempo de un juego concreto:  
    * Necesitamos información de primera mano de la página de PSN España, para ello hacemos una primera aproximacion para encontrar los datos de cada juego ofertado con webscrapping diariamente (4 horas aproximadamente).
    * Limpiamos los datos para que tengan sentido, tanto para analizar con Pandas como para inyectarlo en un bases de datos de SQL.
    * Racionalizar la base de datos que la insertaremos en un servidor de PostGreSQL (Elephant)  
2. En una segunda fase, queremos tener mas datos de otras tiendas online:
    * Expandimos el webscrapping ya que en otras regiones se puede obtener la misma información intentando que el coste computacional y de tiempo sea el minimo posible
#### Estructura del Repositorio
* API: Cambios en funcionalidades principales de la API. Las selecciones no funcionan actualmente. (Última actualización hace 9 horas).
* app: Funcionan los filtros de búsqueda. Se está considerando una nueva forma de mostrar los precios. (Última actualización ayer).
* csv_s: Contiene archivos CSV que se han ido web scrapeando.
* notebooks: Jupyter Notebooks con información principal de las caracteristicas del proyecto.
* pruebas: Directorio de pruebas donde se van almacenando los archivos que son descartados.
* scripts: Scripts de utilidad para web scrapear las páginas que queremos
* utils: Archivos .py , clases funciones y variables necesarias para que nuestro codigo funcione correctamente
#### Notas Adicionales
Por favor, ten en cuenta que este proyecto está en desarrollo y algunas características pueden no estar completamente implementadas o funcionales.



