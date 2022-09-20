from turtle import color
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 
import analisis
import matplotlib.pyplot as plt
import plotly.offline as py


#menu
with st.sidebar:
    choose = option_menu("Henry PI02", [ 'Inicio','Pagina 01', 'Pagina 02', 'Pagina 03', 'Pagina 04', 'Pagina 05', 'Pagina 06', 'Pagina 07',
                                        'Pagina 08', 'Pagina 09'],
                         icons=['house', 'book', 'book', 'book','book', 'book', 'book', 'book','book', 'book', 'person lines fill' ],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fafa39"},
    }
    )
logo = Image.open(r'D:\Proyectos\ProyectoH02\src\logoHn.png') #importando logo
#pagina de inicio
if choose == "Inicio":
    col1, col2,  = st.columns([1, 0.2])
           
    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">COVID-19 Impacto en los pacientes y capacidad hospitalaria</p>', unsafe_allow_html=True)      
        
    with col2: 
        st.image(logo, width=130 )
    
    st.write("Se realizo un analisis de lo datos agregados por estado de NorteAmeria, obteniendo así metricas para el conocimiento del impacto que tuvo el COVID-19, en el país.")    
    mapa = analisis.df[["date", "state", "deaths_covid"]]
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
    st.dataframe(analisis.df)

img01 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico01.png') #importando logo    
if choose == "Pagina 01":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Los 5 Estados con mayor ocupación hospitalaria por COVID </p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Pacientes informados que estuvieron hospitalizados en una cama para pacientes hospitalizados que tienen sospecha o confirmación de COVID-19, por estados en los 6 primeros meses del 2020')
    
    st.image(img01, width=1000)
    df01 = analisis.df01()
    nam = analisis.nom_est()
    col = ['state', 'Percentege_bed_used']
    top05 = df01.nlargest(5, 'Percentege_bed_used')[col]
    top05 = pd.merge(top05, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05.pop('state_name')   
    top05.insert(0, 'state_name', first_column)   
    st.markdown('**Los 05 estados con mayor ocupacion de camas:**')
    st.markdown('Estos estados fueron los que tuvieron una mayor ocupacion de camas por casos de Covid-19, representado en valor porcentual (decimal)')  
    st.dataframe(top05)
    
    mapa = df01.sort_values("Percentege_bed_used", ascending=False)
    fig = px.choropleth(data_frame=mapa, 
                        locations=mapa["state"], 
                        locationmode="USA-states", scope="usa", 
                        color=mapa["Percentege_bed_used"], 
                        labels={"location":"Estado", "color":"Percentege_bed_used"},
                        color_continuous_scale='ylorrd')
    st.plotly_chart(fig)

    
img02 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico02.png') #importando logo    
if choose == "Pagina 02":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Ocupación de camas (Común) por COVID en el Estado de Nueva York</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Pacientes informados que estuvieron hospitalizados en una cama para pacientes hospitalizados y/o tuvieron sospecha o confirmación de COVID-19, durante la cuarentena establecida en el pais desde el 2020-03-22 al 2020-06-13, en el cual se encontro picos maximos Intervalos de crecimiento y decrecimiento Puntos críticos (mínimos y máximos)')
    
    st.image(img02, width=900)
    st.markdown('**Picos Maximos y minimos reportados:**')  
    picos = analisis.picos()
    st.dataframe(picos)
    st.markdown('**Data set empleado para el analisis:**')  
    df02 = analisis.df02()
    st.dataframe(df02)
    
img03 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico03.png') #importando logo    
if choose == "Pagina 03":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">los 05 Estados que más camas UCI utilizaron durante el año 2020</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Aqui realizamosanlisis del total de camas reportadas ocupadas por pediatria y de adultos, este analisis se realizo por estados, obteniendo así camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020, los cuales se muestran en terminos absolutos')
    
    st.image(img03, width=1000)
    df03 = analisis.df03()
    nam = analisis.nom_est()
    col = ['state', 'total_camas']
    top05_3 = df03.nlargest(5, 'total_camas')[col]
    top05_3 = pd.merge(top05_3, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05_3.pop('state_name')   
    top05_3.insert(0, 'state_name', first_column)
    top05_3 = top05_3.round()   
    st.markdown('**Estados con mayor ocupacion de camas UCI:**')
    st.dataframe(top05_3)      
    
img04 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico04.png') #importando logo    
if choose == "Pagina 04":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Total de camas usada, por Estado, para pacientes pediátricos con COVID durante el 2020</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('se analiso el total de camas pediatricas para pacientes hospitalizados preparadas y con personal que estaban ocupadas por un paciente, Incluye camas de UCIP y de cirugía médica, en los reporte se excluye la NICU, la sala de recién nacidos y las camas de cirugía ambulatoria.')
    
    st.image(img04, width=900)
    df04 = analisis.df04()
    nam = analisis.nom_est()
    col = ['state', 'total_camas_pedia']
    top05_4 = df04.nlargest(5, 'total_camas_pedia')[col]
    top05_4 = pd.merge(top05_4, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05_4.pop('state_name')   
    top05_4.insert(0, 'state_name', first_column)
    top05_4 = top05_4.round()   
    st.markdown('**Estados con mayor ocupacion de camas UCI, pediatricos:**')
    st.dataframe(top05_4)
    
img05 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico05.png') #importando logo    
if choose == "Pagina 05":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Porcentaje de camas UCI usadas corresponden a casos confirmados de COVID-19</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Porcentaje del total de camas de UCI para adultos con personal que fueron ocupadas pacientes con sospecha o confirmación de COVID-19, en este número solo tiene en cuenta los hospitales en el estado que informan los campos.')
    
    st.image(img05, width=900)
    df05 = analisis.df05()
    nam = analisis.nom_est()
    col = ['state', 'adult_icu_bed_covid_utilization']
    top05_5 = df05.nlargest(5, 'adult_icu_bed_covid_utilization')[col]
    top05_5 = pd.merge(top05_5, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05_5.pop('state_name')   
    top05_5.insert(0, 'state_name', first_column)   
    st.markdown('**Los estados que ocuparon (%) mas camas UCI:**')
    st.dataframe(top05_5)
 
img06 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico06.png') #importando logo    
if choose == "Pagina 06":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Muertes por covid, por Estado, durante el año 2021</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Número de pacientes con COVID-19 presunto o confirmado que fallecieron el día calendario anterior en el hospital, el servicio de urgencias o el lugar de desbordamiento.')
    
    st.image(img06, width=900)
    df06 = analisis.df06()
    nam = analisis.nom_est()
    col = ['state', 'deaths_covid']
    top05_6 = df06.nlargest(5, 'deaths_covid')[col]
    top05_6 = pd.merge(top05_6, nam[['state', 'state_name']], on=['state'], how='left')
    first_column = top05_6.pop('state_name')   
    top05_6.insert(0, 'state_name', first_column)   
    
    st.dataframe(top05_6)
    inicio = st.selectbox('Fecha de Inicio', options=analisis.df['date'].iloc[0::].unique())
    final = st.selectbox('Fecha de Final', options=analisis.df['date'].iloc[::-1].unique())
    mapa = analisis.df[["date", "state", "deaths_covid"]]
    mapa = mapa[mapa["date"].between(inicio, final)]
    mapa = mapa.groupby("state", as_index=False).sum().sort_values("deaths_covid", ascending=False)
    fig = px.choropleth(data_frame=mapa, 
                        locations=mapa["state"], 
                        locationmode="USA-states", scope="usa", 
                        color=mapa["deaths_covid"], 
                        labels={"location":"Estado", "color":"Muertes"},
                        color_continuous_scale='ylorrd')
    st.plotly_chart(fig)
    
img07 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico07.png') #importando logo    
if choose == "Pagina 07":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Relación entre la falta de personal médico, con la cantidad de muertes por covid durante el año 2021</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Los datos tomados y previamente analisados fueron del año 2021, a pesar de las vacunas se tuvieron picos en decesos de personas por falta de personal medico')
    
    #st.image(img07, width=900)    
    df07 = analisis.df07()
    nam = analisis.nom_est()
    st.line_chart(df07)
    
img08 = Image.open(r'D:\Proyectos\ProyectoH02\src\grafico08.png') #importando logo    
if choose == "Pagina 08":
    col1, col2,  = st.columns([1, 0.2])

    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Peor mes de la pandemia para USA</p>', unsafe_allow_html=True)
        
    with col2: 
        st.image(logo, width=130 )
          
    st.write('Mayo, los 50 estados de EE.UU. habían comenzado a reabrir al menos parcialmente, entre las advertencias de la comunidad científica por el riesgo de "nuevos picos" y un número clavado en la mente de muchos: 100.000 muertos, según el recuento de Johns Hopkins ')
    
    #st.image(img08, width=900)    
    df08 = analisis.df08()
    nam = analisis.nom_est()
    st.line_chart(df08)   

