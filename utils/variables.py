# Librerias necesarias
"""
VARIABLES NECESARIAS
"""
link_inicial = "https://store.playstation.com/"
# link_inicial = "https://store.playstation.com/es-es/pages/browse"
contador_juegos_real = 1 # Esta linea está creada para comprobar que el flujo de los cambios de páginas con sus juegos está correcto.
# seleccion de juego

page = 1 # Variable
game = 0 # Establecemos el primer juego que estará en cont = 1, pero lo establecemos en 0 para iniciarlo

# Mostrar un numero de juegos limitado para que no nos salte error de maximo numero de intentos.
limite = 100 # limite de juegos que se van multiplicando por 2 max abajo para poder ir recopilando la info
timeout = 10
list_error = []
intentos = 0