import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Load your GeoJSON data
with open("brazil_geo.json", "r") as geojson_file:
    brazil_geojson = json.load(geojson_file)

# Enhanced fictional data for all states
data_dict = {
    "AC": 15, "AL": 7, "AP": 14, "AM": 13, "BA": 8, 
    "CE": 22, "DF": 19, "ES": 16, "GO": 20, "MA": 11,
    "MT": 17, "MS": 18, "MG": 23, "PA": 9, "PB": 21, 
    "PR": 24, "PE": 25, "PI": 10, "RJ": 26, "RN": 12,
    "RS": 27, "RO": 6, "RR": 5, "SC": 28, "SP": 29, 
    "SE": 4, "TO": 3
}

# Update GeoJSON properties with the data
for feature in brazil_geojson['features']:
    state_id = feature['id']
    feature['properties']['value'] = data_dict.get(state_id, 0)

# Calculate max value for normalization in color scale
max_value = max(data_dict.values())

# Set up a pydeck layer with enhanced visual styling
layer = pdk.Layer(
    'GeoJsonLayer',
    brazil_geojson,
    opacity=0.7,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=f"[255, 255 - 255 * (properties.value / {max_value}), 0 + 255 * (properties.value / {max_value})]",
    get_line_color="[50, 50, 50]",
    get_line_width=20,
    pickable=True
)

# Set up the pydeck view
view_state = pdk.ViewState(latitude=-14.2350, longitude=-51.9253, zoom=4)

# Render the deck.gl map in Streamlit with a simple tooltip
st.title("Brazil State Data Visualization")
st.write("This map shows some fictional data for each state. Click on a state for more information.")
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9',
    tooltip={"text": "Click on a state"}
))

# Adding a caption or subtitle for data explanation
st.caption("Data values are fictional and for illustrative purposes only.")
