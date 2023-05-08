import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import numpy as np

scieszka = r"F:\PC RESET PACK\Tu zapisuje py\.ipynb_checkpoints\Chyba_git_teraz.csv"


@st.cache_data(persist=True)
def wczytaj_dane(scieszka):
    dane = pd.read_csv(scieszka,index_col=0)
    dane = dane.rename(columns={dane.columns[5]:"lat"})
    dane = dane.rename(columns={dane.columns[6]:"lon"})
    return dane


dane = wczytaj_dane(scieszka)

st.title('Mapa Publicznych Hot Spotów Gdańsk')

st.header("Który hotspot jest najczęściej używany? (Styczeń 2020)")
liczba_uzytkownikow = st.slider("Liczba użytkowników hotspotu w danym miesiącu",3,1229)
dane_suwak= dane.query("Users >=@liczba_uzytkownikow")[["lat","lon","Nazwa lokalizacji","Users"]]
st.map(dane_suwak,)
if st.checkbox("Poka dane w tabelce"):
    st.write(dane_suwak)

                                                                   
zoom_mapy_srodek = (np.average(dane['lon']),np.average(dane['lat']))

layer_podjebane = pdk.Layer(
    "HexagonLayer",
    data=dane[["Users","lat","lon"]],
    get_position=['lon','lat'],
    auto_highlight=True,
    elevation_scale=4,
    pickable=True,
    elevation_range=[0, 500],
    extruded=True,
    coverage=1,
)

layer = pdk.Layer(
    "HexagonLayer",
    data=dane[["Users","lat","lon"]],
    get_position=['lon','lat'],
    radius=180,    #obszar wokół punktu w metrach chyba
    extruded=True, #2d robi jak false
    pickable=True,
    auto_highlight=True,
    coverage=1,
    elevation_scale=4,
    elevation_range=[0,500])

viev_state = initial_view_state={
    "latitude":zoom_mapy_srodek[1],
    "longitude":zoom_mapy_srodek[0],
    "zoom":11,
    "pitch":45,
    }

deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=viev_state,
    layers=[layer])


st.bar_chart(dane,x="Nazwa lokalizacji",y="Users")
st.pydeck_chart(deck)