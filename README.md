# Comparativa de precios en diferentes PSN Store a traves de webscrapping.
#### En este proyecto se quiere dar una visión completa de los precios de los videojuegos en diferentes Stores (Española, Inglesa y Japonesa), para ello lo enfocamos de la siguiente manera:  
1. En una primera fase, hemos querido hacer un dashboard de los mejores precios en el tiempo de un juego concreto:  
    * Necesitamos información de primera mano de la página de PSN España, para ello hacemos una primera aproximacion para encontrar los datos de cada juego ofertado con webscrapping diariamente (4 horas aproximadamente).
    * Limpiamos los datos para que tengan sentido, tanto para analizar con Pandas como para inyectarlo en un bases de datos de SQL.
    * Racionalizar la base de datos que la haremos en un servidor gratuito de PostGreSQL (Elephant)  
2. En una segunda fase, queremos tener mas datos de otras tiendas online:
    * Expandimos el webscrapping ya que en otras regiones se puede obtener la misma información intentando que el coste computacional y de tiempo sea el minimo posible


