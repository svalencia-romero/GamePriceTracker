# Librerias necesarias
"""
VARIABLES NECESARIAS
"""
link_inicial = "https://store.playstation.com/"
link_inicial_esp = "https://store.playstation.com/es-es/"
link_inicial_usa = "https://store.playstation.com/en-us/"
link_inicial_jp = "https://store.playstation.com/ja-jp/"


link_google = "https://www.google.es/"
contador_juegos_real = 1 # Esta linea está creada para comprobar que el flujo de los cambios de páginas con sus juegos está correcto.
# seleccion de juego

page = 1 # Variable
game = 0 # Establecemos el primer juego que estará en cont = 1, pero lo establecemos en 0 para iniciarlo
timeout = 10

# Mostrar un numero de juegos limitado para que no nos salte error de maximo numero de intentos.
list_error = []
lista_recheck = []
lista_no_info = []
intentos = 0
