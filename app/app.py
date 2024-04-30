import streamlit as st
import pandas as pd
import re
prueba_df = pd.read_csv("../csv_s/csv_final_mix_to_db/Insertados/csv_2024-04-25.csv")

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

platform = st.sidebar.selectbox("Plataforma" ,index=None, options=["Sin filtro","PS5", "PS4", "No hay información"], key="platform_selectbox",placeholder="Plataforma",label_visibility='collapsed') 

genre = st.sidebar.selectbox("Género", index=None, options= ['Sin filtro','Deporte','Acción','Aventura','Juegos de rol','Conducción/Carreras','Lucha',
                                                             'Simulación','Juegos de disparos','Terror','Únicos','Casual','Simulador'
                                                              ,'Arcade','Estrategia','Familia','Grupo','Música/Ritmo','Puzzle','Educativos',
                                                              'Fitness','Agilidad mental','Preguntas y respuestas','Adulto','No hay información'], key="genre_selectbox", placeholder="Género",label_visibility='collapsed')

idioma = st.sidebar.selectbox("Disponibilidad de Idioma", index=None, options= ['No hay información','Coreano','Inglés','Español','Polaco','Alemán'
                                                                            ,'Ruso','Turco','Francés (Francia)','Árabe','Japonés','Italiano'
                                                                            ,'Portugués (Brasil)','Español (México)','Portugués (Portugal)'
                                                                            ,'Chino (Tradicional)','Chino (Simplificado)','Neerlandés','Sueco'
                                                                            ,'Griego','Checo','Noruego','Finlandés','Húngaro','Danés','Ucraniano'
                                                                            ,'Francés (Canadá)','Eslovenio','Vietnamita','Tailandés','Croata','Rumano'
                                                                            ,'Eslovaco','Hindi','Búlgaro','Irlandés','Catalán','Francés (Bélgica)'
                                                                            ,'Gallego','Vasco','Malayo','Galés','Tagalo','Afrikaans','Gaélico escocés'],key="idioma_selectbox", placeholder="Idioma disponible",label_visibility='collapsed')

st.sidebar.markdown('<p style="font-family: Arial;color: #FFFFFF;font-size: 20px;">Rango de Precio</p>', unsafe_allow_html=True)
price_range = st.sidebar.slider("Precios",0,100,(0,60),key="price_range_slider",label_visibility='collapsed')

# Datos de ejemplo (podrías reemplazar esto con tus propios datos)
st.dataframe(prueba_df)

# Filtrar datos según la selección del usuario
filtered_data = prueba_df[
    (prueba_df["Plataforma"].str.contains(fr'\b{platform}\b', na=False)) &
    (prueba_df["Genero"] == genre) &
    (prueba_df["Precio original_es"].between(price_range[0], price_range[1])) &
    (prueba_df["Idiomas"].str.contains(fr'\b{idioma}\b', na=False))

]

# Mostrar resultados
st.subheader("Resultados")
if len(filtered_data) > 0:
    for index, game in filtered_data.iterrows():
        st.write(f"**{game['Titulo']}** - {game['Plataforma']} - {game['Genero']} - €{game['Precio original_es']}")
else:
    st.warning("No se encontraron juegos que coincidan con los filtros seleccionados.")
