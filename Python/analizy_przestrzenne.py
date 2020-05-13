#importy bibliotek
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import ipywidgets as widgets

#importy dla map:
import folium # bokeh wywoluje konflikt z ta biblioteka
import geopandas as gpd #uwaga ta biblioteka musi byc zainstalowana na nowym srodowisku i to jako pierwsza, potem kolejne instaluja sie juz spoko

import plotly.express as px
from folium import plugins


# In[ ]:


def mapa_klastry (df):

    map = folium.Map(location=[47.607612, -122.333515], zoom_start=13)

    wypadki = df[df.GODZINA !=0].sample(n=2000)

    # Tworzę podstawową mapę dla seattle
    seattle_map= folium.Map(location=[47.607612, -122.333515], zoom_start=12)

    # Na podstawie współrzędnych każe mu stworzyć punkty na mapie
    for lat, lng, label in zip(wypadki.SZEROKOSC, wypadki.DLUGOSC, wypadki.RANNI.astype(str)):
        if label!='0':
            folium.CircleMarker(
                [lat, lng],
                radius=3,
                color='rgb(58, 155, 150)',
                fill=True,
                popup=label,
                fill_color='rgb(140, 28, 108)',
                fill_opacity=1
            ).add_to(seattle_map)

    # Tworzę clustry dla punktów
    accidents = plugins.MarkerCluster().add_to(seattle_map)

    # Dodaję do clasterków punkty
    for lat, lng, label in zip(wypadki.SZEROKOSC, wypadki.DLUGOSC, wypadki.RANNI.astype(str)):
        if label!='0':
            folium.Marker(
                location=[lat, lng],
                icon=None,
                popup=label,
            ).add_to(accidents)
   
    # Wyplotuj mapę
    return seattle_map


# In[ ]:


def gdzie_powazne_wypadki (df):
    
    mapa = folium.Map(location=[47.607612, -122.333515], zoom_start=12)

    #px.set_mapbox_access_token(open(".mapbox_token").read())
    col = df[df.ROK == 2019].sample(n=200)
    fig = px.scatter_mapbox(col, lat="SZEROKOSC", lon="DLUGOSC",     color="RANNI", size="RANNI",
                      color_continuous_scale=px.colors.sequential.matter, size_max=30, zoom=12)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    print('Wybrana grupa zawiera lokalizację wypadków ze skutkiem śmietlenym, wielkość koła oznacza liczbę poszkodowanych')
    fig.show()


# In[ ]:


def rozklad_wypadkow (df): #(heatmapa)

    #importuję z biblioteki dodatek do tworzenia map skupień
    from folium.plugins import HeatMapWithTime

    # Tworzę podstawową mapę seattle
    seattle_map= folium.Map(location=[47.607612, -122.333515], zoom_start=10)

    wypadki = df[df.GODZINA !=0].sample(n=2000)

    # Wskazuję dla każdego punktu godzinę wydarzenia 
    hour_list = [[] for _ in range(24)]
    for lat,log,hour in zip(wypadki.SZEROKOSC,wypadki.DLUGOSC,wypadki.GODZINA):
        hour_list[hour].append([lat,log]) 

    # Tworzę etykietę dla godzin
    index = [str(i)+'GODZINA' for i in range(24)]

    # Tworzę mapę zagęszczenia dla wypadków 
    HeatMapWithTime(hour_list, index).add_to(seattle_map)

    return seattle_map


# In[ ]:


def mapa_dzielnic (df):
    
    #wczytuje tabelę z dzielnicami i przyłączam ją do naszej pierwotnej bazy danych
    dzielnice = pd.read_csv('dzielnice.csv', dtype={'OBJECTID':int, 'DZIELNICA': str, 'OSIEDLE': str, 'POWIERZCHN': float, 'ID_OSIEDLA':int}, encoding="utf-8")
    df = df.join(dzielnice, lsuffix='OBJECTID', rsuffix='OBJECTID')
    df.dropna(inplace=True)
    df.ID_OSIEDLA = df.ID_OSIEDLA.astype(int)

    #wczytanie pliku shp - to taki który ma geometrię i posiada georeferencje (zrodlo: opendata seattle)
    districts_seattle = gpd.read_file('districts_seattle.shp', dtype={'ID_OSIEDLA':int}, encoding="utf-8")

    #agreguje informacje o liczbie wypadków dla kazdej dzielnicy
    colissions = df.groupby(['ID_OSIEDLA', 'DZIELNICA']).sum().reset_index()

    # Dolaczam naszego shp do stworzonej tabeli zsumowanymi kolizjami
    colissions_districts = districts_seattle.merge(colissions, left_on = 'ID_OSIEDLA', right_on = 'ID_OSIEDLA')

    # Aby rysowal geometrie musze nasza tabele z sumowananymi wypadkami przerobic do GeoJSON
    geosource = GeoJSONDataSource(geojson = colissions_districts.to_json())

    # Definiuje palete kolorow i inne graficzne elementy po ktorych bedzie mi cieniowal dzielnice
    palette = palette = brewer['PuBuGn'][6]
    palette = palette[::-1] # odwracam kolejnosc cieniowania, aby ciemniejsze byly te dzielnice, gdzie wiecej wypadkow
    
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 1700)
    # Define custom tick labels for color bar.
    tick_labels = {'0': '0', '10': '10',
     '100':'100', '250':'250',
     '500':'500', '750':'750',
     '1000':'1000', '1250':'1250',
     '1500':'1500', '2000':'2000',
     '3000':'3000+'}
    # Create color bar.
    color_bar = ColorBar(color_mapper = color_mapper, 
                         label_standoff = 8,
                         width = 500, height = 20,
                         border_line_color = None,
                         location = (0,0), 
                         orientation = 'horizontal',
                         major_label_overrides = tick_labels)
    
    # Create figure object.
    mapa = figure(title = 'Liczba rannych w wypadkach', 
               plot_height = 950, plot_width = 600, 
               toolbar_location = 'below',
               tools = 'pan, wheel_zoom, box_zoom, reset')
    mapa.xgrid.grid_line_color = None
    mapa.ygrid.grid_line_color = None
    # Add patch renderer to figure.
    districs = mapa.patches('xs','ys', source = geosource,
                       fill_color = {'field' :'RANNI',
                                     'transform' : color_mapper},
                       line_color = 'black', 
                       line_width = 0.25, 
                       fill_alpha = 1)
    # Create hover tool
    mapa.add_tools(HoverTool(renderers = [districs],
                          tooltips = [('DZIELNICA','@DZIELNICA'),
                                   ('Liczba rannych', '@RANNI'),
                                   ('Liczba śmiertelnych wypadków', '@SMIERTELNIE_RANNI'),
                                   ('Ilu pieszych zostało poszkodowanych', '@PRZECHODZIEN'),
                                   ('Ilu rowerzystów zostało poszkodowanych', '@PROWERZYSTA'),
                                     ]))
    # Specify layout
    mapa.add_layout(color_bar, 'below')    

    #wyplotowuje mape
    show(mapa)

