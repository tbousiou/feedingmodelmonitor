import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import math
import sqlite3



connection = sqlite3.connect("data.db")
df = pd.read_sql("SELECT * FROM user_models",connection)
# print(df)
# exit()
# SCATTERPLOT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"
# df = pd.read_json(SCATTERPLOT_LAYER_DATA)


# Use pandas to calculate additional data
# df["coor"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))

# Define a layer to display on a map
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=5,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=['lon','lat'],
    # get_radius=50,
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
    
)

# Set the viewport location
view_state = pdk.ViewState(latitude=49.7749295, longitude=13.0, zoom=3, bearing=0, pitch=0)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{title}\n{model}"})
st.title("Model Locations Viewer")
st.pydeck_chart(r)