import streamlit as st

# Configuración de página
st.set_page_config(page_title="Precios de Videojuegos", page_icon="🎮")

# Estilos CSS personalizados
css = """
<style>
[data-testid="stSidebar"] {
    background-color: #212B36;
}
/* Cambiar el tipo de letra de la barra lateral */
[data-testid="stSidebar"][class^="st"] {
    font-family: 'Arial', sans-serif !important;
}
</style>
"""

# Encabezado
st.title("🕹️ Precios de Videojuegos 🎮")

# Barra lateral para filtrar
st.sidebar.markdown(css, unsafe_allow_html=True)
# st.sidebar.markdown('<p style="font-family: Arial; color: #FFFFFF;font-size: 20px;">Seleccione los filtros necesarios</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="font-family: Arial; color: #FFFFFF;font-size: 20px;">Filtros</p>', unsafe_allow_html=True)
platform = st.sidebar.selectbox("Plataforma" ,index=None, options=["PS5", "PS4", "No hay información"], key="platform_selectbox",placeholder="Plataforma",label_visibility='collapsed') 
genre = st.sidebar.selectbox("Género", index=None, options= ['Deporte','Acción','Aventura','Juegos de rol','Conducción/Carreras','Lucha',
                                                             'Simulación','Juegos de disparos','Terror','Únicos','Casual','Simulador'
                                                              ,'Arcade','Estrategia','Familia','Grupo','Música/Ritmo','Puzzle','Educativos',
                                                              'Fitness','Agilidad mental','Preguntas y respuestas','Adulto','No hay información'], key="genre_selectbox", placeholder="Género",label_visibility='collapsed')
st.sidebar.markdown('<p style="font-family: Arial;color: #FFFFFF;font-size: 20px;">Rango de Precio</p>', unsafe_allow_html=True)
price_range = st.sidebar.slider("Precios",0,100,(0,60),key="price_range_slider",label_visibility='collapsed')

# Datos de ejemplo (podrías reemplazar esto con tus propios datos)
data = [
    {"Juego": "The Witcher 3", "Plataforma": "PC", "Género": "RPG", "Precio": 20},
    {"Juego": "The Last of Us Part II", "Plataforma": "PlayStation", "Género": "Acción", "Precio": 40},
    {"Juego": "Halo Infinite", "Plataforma": "Xbox", "Género": "Shooter", "Precio": 60},
    {"Juego": "Animal Crossing: New Horizons", "Plataforma": "Nintendo", "Género": "Simulación", "Precio": 50},
]

# Filtrar datos según la selección del usuario
filtered_data = []
for game in data:
    if (platform == "Todas" or game["Plataforma"] == platform) and \
       (genre == "Todos" or game["Género"] == genre) and \
       (price_range[0] <= game["Precio"] <= price_range[1]):
        filtered_data.append(game)

# Mostrar resultados
st.subheader("Resultados")
if len(filtered_data) > 0:
    for game in filtered_data:
        st.write(f"**{game['Juego']}** - {game['Plataforma']} - {game['Género']} - ${game['Precio']}")
else:
    st.warning("No se encontraron juegos que coincidan con los filtros seleccionados.")
