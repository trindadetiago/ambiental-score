import pandas as pd
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="AmbientalScore", page_icon=":earth_americas:")

st.title("AmbientalScore")

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if "map_data" not in st.session_state:
    st.session_state.map_data = gpd.read_file('data/BR_UF_2022.shp')

if "emission_data" not in st.session_state:
    st.session_state.emission_data = pd.read_csv('data/SEEG.csv')

if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.read_csv('data/Temp.csv')

if st.session_state.map_data is not None:
    shapefile = st.session_state.map_data

    if st.session_state.emission_data is not None:
        emission_data = st.session_state.emission_data
        for column in st.session_state.emission_data.columns:
            if is_numeric(column):
                emission_data[column] = (emission_data[column]/1000).round(-3)
                emission_data.rename(columns={column: "Emissão em " + column + " em milhares "}, inplace=True)
        shapefile = shapefile.merge(emission_data, left_on="NM_UF", right_on="Categoria", how="left")
    if st.session_state.temperature_data is not None:
        temperature_data = st.session_state.temperature_data
        for column in st.session_state.temperature_data.columns:
            if is_numeric(column):
                temperature_data[column] = temperature_data[column].round(1)
        shapefile = shapefile.merge(temperature_data, left_on="NM_UF", right_on="Estado", how="left")

    columns = ["NM_UF", "geometry"]

    st.write("---")

    option = st.selectbox("Selecione o filtro", ["Temperatura", "Emissão Co2"])
    if option == "Temperatura":
        columns.append("TMedia")
    elif option == "Emissão Co2":
        columns.append("Emissão em 2022 em milhares ")

    st.write("---")

    # Explore method to generate the map
    m = shapefile[columns].explore(
                            style_kwds={'fillOpacity': 0.75, 'lineOpacity': 0.5},
                            tiles="CartoDB positron",
                            cmap="OrRd",
                            column=columns[-1],
                            scheme="quantiles"
                            )

    # Display the map
    st_folium(m, height=600, use_container_width=True, returned_objects=[])
    
