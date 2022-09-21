import streamlit as st
from streamlit_option_menu import option_menu
#import streamlit.components.v1 as html
import pandas as pd
import plotly.express as px

def nom_est():
        #nombre de los estados
    nam = pd.read_html('https://es.wikipedia.org/wiki/Estado_de_los_Estados_Unidos')[1]
    nam = nam[['Abrev.','Estado']]
    nam.rename(columns={'Abrev.':'state', 'Estado':'state_name'}, inplace=True)
    return nam

def cargadata():
    #descarga de datos y limpieza
    df = pd.read_csv('D:\Proyectos\DS-PI-ProyectoIndividual\data\COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv')
    df = pd.merge(df, nom_est()[['state', 'state_name']], on=['state'], how='left')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['date'])
    df['Year']  = pd.DatetimeIndex(df['date']).year
    df.reset_index(drop=True, inplace=True)
    
    return df
    
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


#menu
with st.sidebar:
    choose = option_menu("Henry PI02", [ 'Inicio','Pagina 01', 'Pagina 02', 'Pagina 03', 'Pagina 04', 'Pagina 05', 'Pagina 06', 'Pagina 07',
                                        'Pagina 08'],
                         icons=['house', 'book', 'book', 'book','book', 'book', 'book', 'book','book', 'book', 'person lines fill' ],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fafa39"},
    }
    )
#logo = Image.open('https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/logoHn.png') #importando logo
#pagina de inicio
if choose == "Inicio":
    col1, col2,  = st.columns([1, 0.2])
           
    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">COVID-19 Impacto en los pacientes y capacidad hospitalaria</p>', unsafe_allow_html=True)      
        st.write("Se realizo un analisis de lo datos agregados por estado de NorteAmeria, obteniendo así metricas para el conocimiento del impacto que tuvo el COVID-19, en el país.")  
       
          
    mapa = df[["date", "state", "deaths_covid"]]
    mapa = mapa.groupby("state", as_index=False).sum().sort_values("deaths_covid", ascending=False)
    fig = px.choropleth(data_frame=mapa, 
                        locations=mapa["state"], 
                        locationmode="USA-states", scope="usa", 
                        color=mapa["deaths_covid"], 
                        labels={"location":"Estado", "color":"Muertes"},
                        color_continuous_scale='ylorrd')
    st.plotly_chart(fig)
   
    st.markdown('**Dataset empleado para el analisis:**')
    st.markdown('De la siguiente dataframe se tomo distintos datos de casos reales, que fueron reportados día a día, en EEUU, desde el 01/01/2020 a la actualidad.\n\nDatos obtenidos de la pagina: https://dev.socrata.com/foundry/healthdata.gov/g62h-syeh')   
    st.dataframe(df)

#img01 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico01.png')    
if choose == "Pagina 01":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Los 5 Estados con mayor ocupación hospitalaria por COVID </p>', unsafe_allow_html=True)
        
    #with col2: 
    #    st.image(logo, width=130 )
          
    st.write('Pacientes informados que estuvieron hospitalizados en una cama para pacientes hospitalizados que tienen sospecha o confirmación de COVID-19, por estados en los 6 primeros meses del 2020')
    
    df01 = df01()
    nam = nom_est()
    col = ['state', 'Percentege_bed_used']
    top05 = df01.nlargest(5, 'Percentege_bed_used')[col]
    top05 = pd.merge(top05, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05.pop('state_name')   
    top05.insert(0, 'state_name', first_column)   
    st.markdown('**Los 05 estados con mayor ocupacion de camas:**')
    st.markdown('Estos estados fueron los que tuvieron una mayor ocupacion de camas por casos de Covid-19, representado en valor porcentual (decimal)')  
    st.dataframe(top05)
    
    fig = px.bar(df01.head(10), x='state', y='Percentege_bed_used', color='Percentege_bed_used', title='Porcentaje de camas usadas por estado ')
    st.plotly_chart(fig)
    
    mapa = df01.sort_values("Percentege_bed_used", ascending=False)
    fig = px.choropleth(data_frame=mapa, 
                        locations=mapa["state"], 
                        locationmode="USA-states", scope="usa", 
                        color=mapa["Percentege_bed_used"], 
                        labels={"location":"Estado", "color":"Percentege_bed_used"},
                        color_continuous_scale='ylorrd')
    st.plotly_chart(fig)

    
#img02 = Image.open(r'D:\Proyectos\DS-PI-ProyectoIndividual\src\img02.png') #importando logo    
if choose == "Pagina 02":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Ocupación de camas (Común) por COVID en el Estado de Nueva York</p>', unsafe_allow_html=True)
        
    #with col2: 
    #    st.image(logo, width=130 )
          
    st.write('Pacientes informados que estuvieron hospitalizados en una cama para pacientes hospitalizados y/o tuvieron sospecha o confirmación de COVID-19, durante la cuarentena establecida en el pais desde el 2020-03-22 al 2020-06-13, en el cual se encontro picos maximos Intervalos de crecimiento y decrecimiento Puntos críticos (mínimos y máximos)')
    
    st.image(img02, width=900)
    st.markdown('**Picos Maximos y minimos reportados:**')  
    picos = picos()
    st.dataframe(picos)
    st.markdown('**Data set empleado para el analisis:**')  
    df02 = df02()
    st.dataframe(df02)
       
if choose == "Pagina 03":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">los 05 Estados que más camas UCI utilizaron durante el año 2020</p>', unsafe_allow_html=True)
        
    #with col2: 
    #    st.image(logo, width=130 )
          
    st.write('Aqui realizamosanlisis del total de camas reportadas ocupadas por pediatria y de adultos, este analisis se realizo por estados, obteniendo así camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020, los cuales se muestran en terminos absolutos')
    
    df03 = df03()
    nam = nom_est()
    col = ['state', 'total_camas']
    top05_3 = df03.nlargest(5, 'total_camas')[col]
    top05_3 = pd.merge(top05_3, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05_3.pop('state_name')   
    top05_3.insert(0, 'state_name', first_column)
    top05_3 = top05_3.round()
    fig = px.bar(df03.head(10), x='state', y='total_camas', color='total_camas', title='Top 05 estados Los estados con ocuparon mas camas UCI, 2020 ')
    st.plotly_chart(fig)   
    st.markdown('**Estados con mayor ocupacion de camas UCI:**')
    st.dataframe(top05_3)      

