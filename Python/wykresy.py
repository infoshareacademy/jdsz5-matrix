import pandas as pd
import numpy as np
import datetime

#importy dla wykresow

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import seaborn as sns
import ipywidgets as widgets
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import bokeh
from bokeh.palettes import Spectral3
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer


def kolizje_miesiac(df_prognozy):
    sns.set_style('white')
    fig, ax = plt.subplots(figsize=(15,6))

    df_prognozy.set_index('data').resample('M').size().plot(label='Ilość kolizji na miesiąc', color='grey', ax=ax)
    df_prognozy.set_index('data').resample('M').size().rolling(window=12).mean().plot(color='rgb(58, 155, 150)', linewidth=5, label='Średnia roczna ilość kolizji', ax=ax)

    ax.set_title('Ilość kolizji na miesiąc', fontsize=14, fontweight='bold')
    ax.set(ylabel='Ilość kolizji\n', xlabel='')
    ax.legend(bbox_to_anchor=(1.1, 1.1), frameon=False)
    sns.despine(ax=ax, top=True, right=True, left=True, bottom=False)

def kolizje_rok_dzien(df_prognozy):
    nazwa_dzien = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
    dzien_tyg = df_prognozy['data'].dt.weekday_name
    rok = df_prognozy['data'].dt.year

    tabela_kolizje = df_prognozy.groupby([rok, dzien_tyg]).size()
    tabela_kolizje = tabela_kolizje.rename_axis(['rok', 'dzien_tyg']).unstack('dzien_tyg').reindex(columns=nazwa_dzien)
    
    plt.figure(figsize=(10,7))
    sns.heatmap(tabela_kolizje, cmap='Blues')
    plt.title('\nKolizje w danym roku i dniu tygodnia\n', fontsize=14, fontweight='bold')
    plt.xlabel('')
    plt.ylabel('')

def kolizje_doba(df_prognozy):
    sns.set_style('white')
    fig, ax = plt.subplots(figsize=(10,6))

    df_prognozy.GODZINA.hist(range=(1,25), bins=24, ax=ax, color='lightblue')
    ax.set_title('\n Rokład kolizji w ciągu doby\n', fontsize=14, fontweight='bold')
    ax.set(xlabel='Godzina', ylabel='Ilość kolizji')
    sns.despine(top=True, right=True, left=True, bottom=True)

def ranni_na_miesiac (df):
      
    ranni = df.groupby('MIESIAC').sum().reset_index()

    trace2 = go.Area(
        r=list(ranni.PRZECHODZIEN),
        t=list(ranni.MIESIAC*30),
        name='Liczba poszkodowanych pieszych',
        marker=dict(
            color='rgb(58, 155, 150)'
        )
    )

    trace3 = go.Area(
        r=list(ranni.PROWERZYSTA),
        t=list(ranni.MIESIAC*30),
        name='Liczba poszkodowanych rowerzystów',
        marker=dict(
            opacity=0.8,
            color='rgb(22,78,76)'
        )
    )

    trace4 = go.Area(
        r=list(ranni.POWAZNIE_RANNI),
        t=list(ranni.MIESIAC*30),
        name='Liczba ofiar śmiertelnych',
        marker=dict(
            color='rgb(140, 28, 108)'
        )
    )

    data = [trace2, trace3, trace4]

    layout = go.Layout(
        title='Liczba wypadków na miesiąć (w analizowanych latach, czytaj według wskazówek zegara)',
        width = 1000,
        height = 500,
        orientation=-90
    )
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

def wypadki_na_dzien (df):
   
    ranni = df[df.GODZINA != 0].groupby('GODZINA').sum().reset_index()

    trace1 = go.Area(
        r=list(ranni.PRZECHODZIEN),
        t=list(ranni.GODZINA*15),
        name='Liczba poszkodowanych pieszych',
        marker=dict(
            color='rgb(58, 155, 150)'
        )
    )
    
    trace2 = go.Area(
        r=list(ranni.PROWERZYSTA),
        t=list(ranni.GODZINA*15),
        name='Liczba poszkodowanych rowerzystów',
        marker=dict(
            opacity=0.8,
            color='rgb(22,78,76)'
        )
    )

    trace3 = go.Area(
        r=list(ranni.POWAZNIE_RANNI),
        t=list(ranni.GODZINA*15),
        name='Liczba ofiar śmiertelnych',
        marker=dict(
            opacity=0.8,
            color='rgb(140, 28, 108)'
        )
    )

    data = [trace1, trace2, trace3]

    layout = go.Layout(
        title='Liczba poszkodowanych o określonych godzinach (w wybranych analizowanych latach)',
        width = 1000,
        height = 500,
        orientation=-90
    )
  
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

def ranni_uczestnik_ruchu (df):
    
    ranni = df.groupby('MIESIAC').sum().reset_index()
    x=list(ranni.MIESIAC)
    fig = go.Figure(go.Bar(x=x, y=ranni['RANNI']-ranni['PROWERZYSTA']-ranni['PRZECHODZIEN'], name='Liczba rannych kierowców', marker_color='rgb(58, 155, 150)'))
    fig.add_trace(go.Bar(x=x, y=ranni['PROWERZYSTA'], name='Liczba rannych rowerzystów', marker_color='rgb(22,78,76)'))
    fig.add_trace(go.Bar(x=x, y=ranni['PRZECHODZIEN'], name='Liczba rannych pieszych', marker_color='rgb(140, 28, 108)'))

    fig.update_layout(title_text='Liczba rannych (wg grupy) w miesiącach', barmode='stack', xaxis={'categoryorder':'category ascending'})
    fig.show()

def co_wplywa_na_kolizje (df):

    group = df.groupby('MIESIAC').sum().reset_index()
    group1 = df.drop(df[df.POD_WYPLYWEM == 0].index)
    group1 = group1.groupby('MIESIAC').sum()
    group2 = df.drop(df[df.PRZEKORCZENIE_PREDKOSCI == 0].index)
    group2 = group2.groupby('MIESIAC').sum()

    source = ColumnDataSource(group)
    source1 = ColumnDataSource(group1)
    source2 = ColumnDataSource(group2)

    p = figure(x_axis_type="datetime")

    p.line(x='MIESIAC', y='RANNI', line_width=2, source=source1, color='rgb(58, 155, 150)', legend='Liczba rannych w wypadkach, gdy kierowca był "podwpływem"')
    p.line(x='MIESIAC', y='RANNI', line_width=2, source=source2, color='rgb(140, 28, 108)', legend='Liczba rannych w wypadkach, gdy kierowca przekroczył prędkość')

    p.title.text = 'Które czynniki powodują większą kolizyjność'

    p.yaxis.axis_label = 'Liczba rannych'
    p.xaxis.axis_label = 'miesiące'

    show(p)

def warunki_pogodowe (df):

    #array(['Dry', 'Wet', 0, 'Unknown', 'Ice', 'Snow/Slush', 'Oil', 'Sand/Mud/Dirt', 'Other', 'Standing Water'], dtype=object)

    group1 = df.drop(df[df.POGODA == 'Clear'].index)
    group1 = group1.groupby('MIESIAC').sum().reset_index()
    group2 = df.drop(df[df.POGODA == 'Overcast'].index)
    group2 = group2.groupby('MIESIAC').sum().reset_index()
    group3 = df.drop(df[df.POGODA == 'Raining'].index)
    group3 = group3.groupby('MIESIAC').sum().reset_index()
    group4 = df.drop(df[df.POGODA == 'Fog/Smog/Smoke'].index)
    group4 = group4.groupby('MIESIAC').sum().reset_index()
    group5 = df.drop(df[df.POGODA == 'Snowing'].index)
    group5 = group5.groupby('MIESIAC').sum().reset_index()
    group6 = df.drop(df[df.POGODA == 'Blowing Sand/Dirt'].index)
    group6 = group6.groupby('MIESIAC').sum().reset_index()
    group7 = df.drop(df[df.POGODA == 'Sleet/Hail/Freezing Rain'].index)
    group7 = group7.groupby('MIESIAC').sum().reset_index()
    group8 = df.drop(df[df.POGODA == 'Severe Crosswind'].index)
    group8 = group8.groupby('MIESIAC').sum().reset_index()

    # Stwórz nowy wykres

    p= figure(
        title='Warunki pogodowe i ich wpływ na liczbę rannych w wypadkach',
        plot_height=500, plot_width=900,
        x_axis_label= 'Miesiące',
        y_axis_label= 'Liczba poszkodowanych w wypadkach'
    )

    # Dodaj linie do wykresu
    p.line(group1['MIESIAC'],group1['RANNI'], legend='ładna pogoda', line_width = 4, color ='#8c1c6c')
    p.line(group2['MIESIAC'],group2['RANNI'], legend='pochmurnie', line_width = 4, color = '#164e4c')
    p.line(group3['MIESIAC'],group3['RANNI'], legend='deszczowo', line_width = 4, color = '#3a9b96')
    p.line(group4['MIESIAC'],group4['RANNI'], legend='mgliście', line_width = 4, color = '#57e8e0')
    p.line(group5['MIESIAC'],group5['RANNI'], legend='śnieżnie', line_width = 4, color = '#7db9b6')
    p.line(group6['MIESIAC'],group6['RANNI'], legend='marznący deszcz', line_width = 4, color = '#a87460')
    p.line(group7['MIESIAC'],group7['RANNI'], legend='wiatr boczny', line_width = 4, color = '#e8df85')
    
    # Wyplotuj wykres 
    show(p)
  
def warunki_drogowe (df):
    
    group1 = df.drop(df[df.WARUNKI_DROGOWE == 'Dry'].index)
    group1 = group1.groupby('MIESIAC').sum().reset_index()
    group2 = df.drop(df[df.WARUNKI_DROGOWE == 'Wet'].index)
    group2 = group2.groupby('MIESIAC').sum().reset_index()
    group3 = df.drop(df[df.WARUNKI_DROGOWE == 'Ice'].index)
    group3 = group3.groupby('MIESIAC').sum().reset_index()
    group4 = df.drop(df[df.WARUNKI_DROGOWE == 'Snow/Slush'].index)
    group4 = group4.groupby('MIESIAC').sum().reset_index()
    group5 = df.drop(df[df.WARUNKI_DROGOWE == 'Oil'].index)
    group5 = group5.groupby('MIESIAC').sum().reset_index()
    group6 = df.drop(df[df.WARUNKI_DROGOWE == 'Sand/Mud/Dirt'].index)
    group5 = group6.groupby('MIESIAC').sum().reset_index()
    group7 = df.drop(df[df.WARUNKI_DROGOWE == 'Standing Water'].index)
    group7 = group7.groupby('MIESIAC').sum().reset_index()


    # Stwórz nowy wykres
    p= figure(
        title='Warunki panujące na drodze i ich wpływ na liczbę rannych w wypadkach',
        plot_height=500, plot_width=900,
        x_axis_label= 'X Axis',
        y_axis_label= 'Y Axis'
    )

    # Dodaj linie do wykresu
    p.line(group1['MIESIAC'],group1['RANNI'], legend='sucha nawierzchnia', line_width = 4, color ='#8c1c6c')
    p.line(group2['MIESIAC'],group2['RANNI'], legend='mokra nawierzchnia', line_width = 4, color = '#164e4c')
    p.line(group3['MIESIAC'],group3['RANNI'], legend='oblodzenie', line_width = 4, color = '#3a9b96')
    p.line(group4['MIESIAC'],group4['RANNI'], legend='zaśnieżona', line_width = 4, color = '#57e8e0')
    p.line(group5['MIESIAC'],group5['RANNI'], legend='olej na drodze', line_width = 4, color = '#7db9b6')
    p.line(group6['MIESIAC'],group6['RANNI'], legend='błoto, piasek', line_width = 4, color = '#a87460')
    p.line(group7['MIESIAC'],group7['RANNI'], legend='woda stojąca', line_width = 4, color = '#e8df85')

    # Pokaż wykres
    show(p)
