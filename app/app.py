import streamlit as st
import pandas as pd
import re
prueba_df = pd.read_csv("../csv_s/csv_limpio/es/csv_limpio_2024-03-13.csv")

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
st.dataframe(prueba_df)

# Filtrar datos según la selección del usuario
filtered_data = prueba_df[
    (prueba_df["Plataforma"] == platform) |
    (platform == "No hay información")
    & (prueba_df["Genero"] == genre)
    & (prueba_df["Precio actual con PSN"].between(price_range[0], price_range[1]))
]

# Mostrar resultados
st.subheader("Resultados")
if len(filtered_data) > 0:
    for index, game in filtered_data.iterrows():
        st.write(f"**{game['Titulo']}** - {game['Plataforma']} - {game['Genero']} - €{game['Precio actual con PSN']}")
else:
    st.warning("No se encontraron juegos que coincidan con los filtros seleccionados.")
