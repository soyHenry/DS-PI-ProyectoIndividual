import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime as dt
import cufflinks as cf
from IPython.display import display, HTML
from sodapy import Socrata
import plotly.express as px

cf.set_config_file(sharing='public', theme='ggplot', offline=True)


def cargadata():
    #descarga de datos y limpieza
    df = pd.read_csv('DS-PI-ProyectoIndividual\COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv', )
    df = pd.merge(df, nom_est()[['state', 'state_name']], on=['state'], how='left')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['date'])
    df['Year']  = pd.DatetimeIndex(df['date']).year
    df.reset_index(drop=True, inplace=True)
    return df

def nom_est():
    #nombre de los estados
    nam = pd.read_html('https://es.wikipedia.org/wiki/Estado_de_los_Estados_Unidos')[1]
    nam = nam[['Abrev.','Estado']]
    nam.rename(columns={'Abrev.':'state', 'Estado':'state_name'}, inplace=True)
    return nam
    
df = cargadata()
nam = nom_est()
#1 - ¿Cuáles fueron los 5 Estados con mayor ocupación hospitalaria por COVID? Criterio de ocupación por
# cama común. Considere la cantidad de camas ocupadas con pacientes confirmados y tome como referencia los 
# 6 primeros meses del 2020 - recuerde incluir la cifra de infectados en esos meses (acumulativo). ¿Influye el rango etario en este comportamiento?

def df01():
    df01 = cargadata().loc[:,['state', 'date', 'inpatient_beds', 'inpatient_beds_used_covid', ]]

    df01 = df01.loc[(df01['date'] >= '2020-01-01') & (df01['date'] <= '2020-06-30')]
    df01 = df01[df01['inpatient_beds'].notna()] #eliminando filas nan
    df01 = df01.fillna(0) #remplazo nan

    df01['Percentege_bed_used'] = df01['inpatient_beds_used_covid'] / df01['inpatient_beds']

    df01 = df01.groupby('state')['Percentege_bed_used'].mean()
    df01 = df01.reset_index()

    col = ['state', 'Percentege_bed_used']
    top05 = df01.nlargest(5, 'Percentege_bed_used')[col]
    top05 = pd.merge(top05, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05.pop('state_name')   
    top05.insert(0, 'state_name', first_column)

    df01 = df01.sort_values('Percentege_bed_used', ascending=False)
    #df01.set_index('state', inplace=True)
    return df01


#2 - Analice la ocupación de camas (Común) por COVID en el Estado de Nueva York durante la cuarentena establecida e indique:

def df02():
    df02 = df.loc[:,['state', 'date', 'inpatient_beds', 'inpatient_beds_used_covid']]
    df02 = df02.loc[(df02['date'] >= '2020-03-22') & (df02['date'] <= '2020-06-13')]
    df02 = df02[df02['state']== 'NY']
    
    return df02

def picos():
  
    df02 = df.loc[:,['state', 'date', 'inpatient_beds', 'inpatient_beds_used_covid']]
    df02 = df02.loc[(df02['date'] >= '2020-03-22') & (df02['date'] <= '2020-06-13')]
    df02 = df02[df02['state']== 'NY']
    pru = df02.copy()
    from scipy.signal import find_peaks #obtenemos los picos 
    peaks, _ =find_peaks(df02.inpatient_beds_used_covid, prominence=1)
    df02['minima'] = df02['inpatient_beds_used_covid']*-1 #convierto a negativo para obtener los picos minimos
    peaks1, _ =find_peaks(df02.minima, prominence=1)
    df02 = df02.groupby('date')['inpatient_beds_used_covid'].sum()
    pi01 = []
    for i in df02[peaks].index.strftime('%Y-%m-%d'):
        pi01.append(i)
    pi02 = []
    for i in df02[peaks1].index.strftime('%Y-%m-%d'):
        pi02.append(i)
    pi01 = pd.DataFrame(pi01)
    pi01.rename(columns={0:'date'}, inplace=True)
    pi01['Desc'] = 'Pico Maximo'
    pi02 = pd.DataFrame(pi02)
    pi02.rename(columns={0:'date'}, inplace=True)
    pi02['Desc'] = 'Pico Minimo'
    pi01 = pi01.reset_index()
    pi02 = pi02.reset_index()
    picos = pd.concat([pi01, pi02])
    picos = picos.sort_values('index', ascending=True)
    picos['date'] = pd.to_datetime(picos['date'])
    picos = pd.merge(picos, pru[['date', 'inpatient_beds_used_covid']], on=['date'], how='left')
    
    picos = picos.drop(['index'], axis=1)
    first_column = picos.pop('Desc')   
    picos.insert(0, 'Desc', first_column) 
    picos= picos.dropna()
    return picos

    

#3
def df03():
    df03 = df.loc[:,['state', 'state_name', 'date', 'inpatient_beds', 'adult_icu_bed_utilization_numerator', 'staffed_pediatric_icu_bed_occupancy']]
    df03['Year']  = pd.DatetimeIndex(df03['date']).year
    #filtrado por año
    df03 = df03.loc[(df03['Year'] == 2020)]
    df03 = df03.fillna(0)
    df03['total_icu_bed_use'] = df03['adult_icu_bed_utilization_numerator'] + df03['staffed_pediatric_icu_bed_occupancy']
    df03 = df03.groupby('state')['total_icu_bed_use'].sum()
    df03 = df03.reset_index()
    df03['total_camas'] = df03.total_icu_bed_use / 254
    df03 = df03.sort_values('total_camas', ascending=False)
    return df03

#4
def df04():
    df04 = df.loc[:,['state', 'state_name', 'date', 'inpatient_beds', 'all_pediatric_inpatient_bed_occupied']]
    df04['Year']  = pd.DatetimeIndex(df04['date']).year
    #filtrado por año
    df04 = df04.loc[(df04['Year'] == 2020)]
    df04 = df04.fillna(0)
    df04 = df04.groupby('state')['all_pediatric_inpatient_bed_occupied'].sum()
    df04 = df04.reset_index()
    df04['total_camas_pedia'] = df04.all_pediatric_inpatient_bed_occupied / 254
    df04 = df04.sort_values('total_camas_pedia', ascending=False)
    return df04

#5
def df05():
    df05 = df.loc[:,['state', 'date', 'inpatient_beds', 'adult_icu_bed_covid_utilization']]
    df05 = df05[df05['adult_icu_bed_covid_utilization'].notna()] #eliminando filas nan
    df05 = df05.groupby('state')['adult_icu_bed_covid_utilization'].mean()
    df05 = df05.reset_index()
    df05 = df05.sort_values('adult_icu_bed_covid_utilization', ascending=False)
    return df05


#6
def df06():
    df06 = df.loc[:,['state','date', 'Year', 'deaths_covid']]
    df06 = df06.loc[(df06['Year'] == 2021)]
    df06 = df06.groupby('state')['deaths_covid'].sum()
    df06 = df06.reset_index()
    df06 = df06.sort_values('deaths_covid', ascending=False)
    return df06


#7
def df07():
    df07 = df.loc[:,['date', 'Year', 'deaths_covid', 'critical_staffing_shortage_today_yes']]
    df07 = df07.loc[(df07['Year'] == 2021)]
    df07 = df07.groupby('date')['deaths_covid', 'critical_staffing_shortage_today_yes'].sum()
    return df07

#8
def df08():
    df08 = df.loc[:,['date', 'Year', 'deaths_covid', 'critical_staffing_shortage_today_yes']]
    df08 = df08.groupby('date')['deaths_covid', 'critical_staffing_shortage_today_yes'].sum()
    return df08

#9
def df09():
    df09 = df.loc[:,['date', 'deaths_covid', 'on_hand_supply_therapeutic_b_bamlanivimab_courses',
                 'on_hand_supply_therapeutic_a_casirivimab_imdevimab_courses', 'on_hand_supply_therapeutic_c_bamlanivimab_etesevimab_courses']]
    df09 = df09.fillna(0)
    df09= df09.groupby('date')['deaths_covid', 'on_hand_supply_therapeutic_b_bamlanivimab_courses',
                 'on_hand_supply_therapeutic_a_casirivimab_imdevimab_courses', 'on_hand_supply_therapeutic_c_bamlanivimab_etesevimab_courses'].sum()
    return df09