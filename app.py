import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def sin_outliers(tabla, columnas, K, columns_to_ignore = []):
    df = tabla[columnas].copy()
    df.dropna(inplace = True)
    for columna in columnas:
        if columna in columns_to_ignore:
            continue
        mean = df[columna].mean()
        std = df[columna].std()
        df = df[(df[columna] > mean - K*std) & (df[columna] < mean + K*std)]
    return df

def add_criticos(table, columna):
    casos = np.array([])
    critico = np.array([])
    if table.loc[1,columna] - table.loc[0,columna] > 0:
        case = 'Creciente'
    else:
        case = 'Decreciente'
    for index in table.index:
        if index == 0 or index == table.index[-1]:
            casos = np.append(casos,case)
            if index == 0: critico = np.append(critico,'Limite')
            else: critico = np.append(critico,'Limite')
            continue
        actual_value = table.loc[index, columna]
        last_value = table.loc[index-1, columna]
        next_value = table.loc[index+1, columna]
        last_dif = actual_value - last_value
        next_dif = next_value - actual_value
        if last_dif*next_dif < 0 and last_dif < 0:
            critico = np.append(critico, 'Mínimo')
            casos = np.append(casos,'--')
            case = 'Creciente'
            continue
        elif last_dif*next_dif < 0:
            critico = np.append(critico, 'Máximo')
            casos = np.append(casos,'--')
            case = 'Decreciente'
            continue
        casos = np.append(casos,case)
        critico = np.append(critico, '--')
    table['Comportamiento'] = casos
    table['Criticos'] = critico
    pass


table = pd.read_csv('my_table.csv')
table['date'] = table['date'].map(lambda x: dt.datetime.strptime(x.split('T')[0], '%Y-%m-%d'))
table.sort_values(['date','state'], inplace = True)
table.reset_index(drop=True, inplace=True)

def page_0(): 
    # Tabla
    st.markdown('# ¡Empezando con el DataSet!')
    st.write("Se realiza un **reconocimiento de los datos**")
    st.dataframe(table)
    st.info('Número de registros: {}'.format(len(table)))

    # Columnas
    st.write('----')
    col1, col2 = st.columns(2)
    col1.write('Las columnas del **dataset**:')
    col1.dataframe(pd.DataFrame(pd.Series(table.columns, name='Columnas')), height=350)
    col1.info('Número de columnas: {}'.format(len(table.columns)))
    col2.write('Las columnas que **usaron en este análisis**:')
    cols = ['date', 'state', 'deaths_covid', 'inpatient_beds_used_covid',
            'staffed_adult_icu_bed_occupancy', 'all_pediatric_inpatient_bed_occupied', 
            'adult_icu_bed_covid_utilization', 'critical_staffing_shortage_today_yes']
    short = ['date', 'state', 'deaths', 'beds_covid','icu_beds',
             'pediatric_beds', 'icu_bed_covid', 'staffing_shortage']
    expl = ['Fecha', 'Estado', 'Muertes por COVID-19', 'Camas usadas por pacientes con covid',
            'Camas usadas por adultos en UCI', 'Camas usadas por pacientes pediátricos', 
            'Camas usadas por adultos en UCI con COVID-19', 'Hospitales que reportan falta de personal crítico']
    cols = pd.Series(cols, name='Columnas')
    short = pd.Series(short, name='Nombre_corto')
    expl = pd.Series(expl, name='Explicación')
    col2.dataframe(pd.concat([cols, expl, short], axis = 1), height=350)
    col2.info('Número de columnas: {}'.format(len(cols)))

    # Exploración de datos
    st.write('----')
    st.markdown('## Exploración de datos')
    tabs = st.tabs(list(short.values))
    with tabs[0]:
        st.write('Columna a analizar: **{}**'.format(cols.values[0]))
        col3, col4 = st.columns(2)
        col3.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['date']))))
        col3.write('* Cantidad de valores faltantes: {}'.format(len(table[table['date'].isna()])))
        col4.write('* Valor mínimo: {}'.format(table['date'].min()))
        col4.write('* Valor máximo: {}'.format(table['date'].max()))
        table_0_1 = table['date'].value_counts().reset_index()
        table_0_1 = table_0_1.rename(columns={'index':'Fecha', 'date':'Conteo'})
        table_0_1.sort_values('Fecha', inplace = True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_1['Fecha'], y = table_0_1['Conteo']))
        fig.update_layout(
            title='Conteo de registros para las fechas',
            xaxis_title = 'Fecha',
            yaxis_title = 'Conteo')
        st.plotly_chart(fig)

    with tabs[1]:
        st.write('Columna a analizar: **{}**'.format(cols.values[1]))
        col3, col4 = st.columns(2)
        col3.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['state']))))
        col4.write('* Cantidad de valores faltantes: {}'.format(len(table[table['state'].isna()])))
        table_0_1 = table['state'].value_counts()
        fig = go.Figure()
        fig.add_trace(go.Bar(x = table_0_1.index, y = table_0_1.values))
        fig.update_layout(
            title='Conteo de registros para estados')
        st.plotly_chart(fig)
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_1.index,
                            locationmode='USA-states',
                            z = table_0_1.values,
                            colorscale = 'Rainbow',
                            colorbar_title = 'Registros',
                            marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Cantidad de registros por estado',
                          geo_scope='usa', paper_bgcolor='rgba(175,175,175,0)', geo_bgcolor = 'rgba(175,175,175,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)

    with tabs[2]:
        st.write('Columna a analizar: **{}**'.format(cols.values[2]))
        table_0_2 = table[['date', 'state','deaths_covid']].copy()
        table_0_2.dropna(inplace = True)
        col1, col2 = st.columns(2)
        col1.write('* Cantidad de datos: {}'.format(len(table['deaths_covid'].dropna())))
        col1.write('* Cantidad de datos faltantes: {}'.format(len(table[table['deaths_covid'].isna()])))
        col1.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['deaths_covid']))))
        col2.write('* Rango de valores: ({:.0f} , {:.0f})'.format(table['deaths_covid'].min(), table['deaths_covid'].max()))
        col2.write('* Promedio: {:.3f}'.format(table['deaths_covid'].mean()))
        col2.write('* Desviación estándar: {:.3f}'.format(table['deaths_covid'].std()))
        table_0_2_1 = table_0_2[['date','deaths_covid']].groupby('date').sum()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = table_0_2_1['deaths_covid']))
        fig.update_layout(
            title='Distribución',
            xaxis_title = 'Valores',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('----')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_2_1.index, y = table_0_2_1['deaths_covid']))
        fig.update_layout(
            title='Cantidad de muertes diarias',
            xaxis_title = 'Fecha',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_2_1.sort_values('deaths_covid', ascending=False).head())
        st.write('----')
        table_0_2_2 = table_0_2[['state','deaths_covid']].groupby('state').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_2_2['state'],
                                    locationmode='USA-states',
                                    z = table_0_2_2['deaths_covid'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Pacientes en cama',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Cantidad de muertes diarias',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_2_2.sort_values('deaths_covid', ascending=False).head())

    with tabs[3]:
        st.write('Columna a analizar: **{}**'.format(cols.values[3]))
        table_0_3 = table[['date', 'state','inpatient_beds_used_covid']].copy()
        table_0_3.dropna(inplace = True)
        # table_0_2 = sin_outliers(table_0_2, ['date', 'deaths_covid'], 3, ['date'])
        col3, col4 = st.columns(2)
        col3.write('* Cantidad de datos: {}'.format(len(table['inpatient_beds_used_covid'].dropna())))
        col3.write('* Cantidad de datos faltantes: {}'.format(len(table[table['inpatient_beds_used_covid'].isna()])))
        col3.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['inpatient_beds_used_covid']))))
        col4.write('* Rango de valores: ({:.0f} , {:.0f})'.format(table['inpatient_beds_used_covid'].min(), table['inpatient_beds_used_covid'].max()))
        col4.write('* Promedio: {:.3f}'.format(table['inpatient_beds_used_covid'].mean()))
        col4.write('* Desviación estándar: {:.3f}'.format(table['inpatient_beds_used_covid'].std()))
        table_0_3_1 = table_0_3[['date','inpatient_beds_used_covid']].groupby('date').sum()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = table_0_3_1['inpatient_beds_used_covid']))
        fig.update_layout(
            title='Distribución',
            xaxis_title = 'Valores',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('----')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_3_1.index, y = table_0_3_1['inpatient_beds_used_covid']))
        fig.update_layout(
            title='Total pacientes con COVID-19 en cama',
            xaxis_title = 'Fecha',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_3_1.sort_values('inpatient_beds_used_covid', ascending=False).head())
        st.write('----')
        table_0_3_2 = table_0_3[['state','inpatient_beds_used_covid']].groupby('state').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_3_2['state'],
                                    locationmode='USA-states',
                                    z = table_0_3_2['inpatient_beds_used_covid'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Pacientes en cama',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Total de pacientes en cama',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_3_2.sort_values('inpatient_beds_used_covid', ascending=False).head())
    with tabs[4]:
        st.write('Columna a analizar: **{}**'.format(cols.values[4]))
        table_0_4 = table[['date', 'state','staffed_adult_icu_bed_occupancy']].copy()
        table_0_4.dropna(inplace = True)
        col3, col4 = st.columns(2)
        col3.write('* Cantidad de datos: {}'.format(len(table['staffed_adult_icu_bed_occupancy'].dropna())))
        col3.write('* Cantidad de datos faltantes: {}'.format(len(table[table['staffed_adult_icu_bed_occupancy'].isna()])))
        col3.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['staffed_adult_icu_bed_occupancy']))))
        col4.write('* Rango de valores: ({:.0f} , {:.0f})'.format(table['staffed_adult_icu_bed_occupancy'].min(), table['staffed_adult_icu_bed_occupancy'].max()))
        col4.write('* Promedio: {:.3f}'.format(table['staffed_adult_icu_bed_occupancy'].mean()))
        col4.write('* Desviación estándar: {:.3f}'.format(table['staffed_adult_icu_bed_occupancy'].std()))
        table_0_4_1 = table_0_4[['date','staffed_adult_icu_bed_occupancy']].groupby('date').sum()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = table_0_4_1['staffed_adult_icu_bed_occupancy']))
        fig.update_layout(
            title='Distribución',
            xaxis_title = 'Valores',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('----')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_4_1.index, y = table_0_4_1['staffed_adult_icu_bed_occupancy']))
        fig.update_layout(
            title='Total pacientes en camas de UCI',
            xaxis_title = 'Fecha',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_4_1.sort_values('staffed_adult_icu_bed_occupancy', ascending=False).head())
        st.write('----')
        table_0_4_2 = table_0_4[['state','staffed_adult_icu_bed_occupancy']].groupby('state').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_4_2['state'],
                                    locationmode='USA-states',
                                    z = table_0_4_2['staffed_adult_icu_bed_occupancy'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Pacientes en cama',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Total pacientes en camas de UCI',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_4_2.sort_values('staffed_adult_icu_bed_occupancy', ascending=False).head())
    with tabs[5]:
        st.write('Columna a analizar: **{}**'.format(cols.values[5]))
        table_0_5 = table[['date', 'state','all_pediatric_inpatient_bed_occupied']].copy()
        table_0_5.dropna(inplace = True)
        col1, col2 = st.columns(2)
        col1.write('* Cantidad de datos: {}'.format(len(table['all_pediatric_inpatient_bed_occupied'].dropna())))
        col1.write('* Cantidad de datos faltantes: {}'.format(len(table[table['all_pediatric_inpatient_bed_occupied'].isna()])))
        col1.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['all_pediatric_inpatient_bed_occupied']))))
        col2.write('* Rango de valores: ({:.0f} , {:.0f})'.format(table['all_pediatric_inpatient_bed_occupied'].min(), table['all_pediatric_inpatient_bed_occupied'].max()))
        col2.write('* Promedio: {:.3f}'.format(table['all_pediatric_inpatient_bed_occupied'].mean()))
        col2.write('* Desviación estándar: {:.3f}'.format(table['all_pediatric_inpatient_bed_occupied'].std()))
        table_0_5_1 = table_0_5[['date','all_pediatric_inpatient_bed_occupied']].groupby('date').sum()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = table_0_5_1['all_pediatric_inpatient_bed_occupied']))
        fig.update_layout(
            title='Distribución',
            xaxis_title = 'Valores',
            yaxis_title = 'Cantidad')
        st.write('----')
        st.plotly_chart(fig)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_5_1.index, y = table_0_5_1['all_pediatric_inpatient_bed_occupied']))
        fig.update_layout(
            title='Total pacientes pediátricos en cama',
            xaxis_title = 'Fecha',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_5_1.sort_values('all_pediatric_inpatient_bed_occupied', ascending=False).head())
        st.write('----')
        table_0_5_2 = table_0_5[['state','all_pediatric_inpatient_bed_occupied']].groupby('state').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_5_2['state'],
                                    locationmode='USA-states',
                                    z = table_0_5_2['all_pediatric_inpatient_bed_occupied'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Pacientes en cama',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Total pacientes pediátricos en cama',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_5_2.sort_values('all_pediatric_inpatient_bed_occupied', ascending=False).head())
    with tabs[6]:
        st.write('Columna a analizar: **{}**'.format(cols.values[6]))
        table_0_6 = table[['date', 'state','adult_icu_bed_covid_utilization']].copy()
        table_0_6.dropna(inplace = True)
        col1, col2 = st.columns(2)
        col1.write('* Cantidad de datos: {}'.format(len(table['adult_icu_bed_covid_utilization'].dropna())))
        col1.write('* Cantidad de datos faltantes: {}'.format(len(table[table['adult_icu_bed_covid_utilization'].isna()])))
        col1.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['adult_icu_bed_covid_utilization']))))
        col2.write('* Rango de valores: ({:.0f} , {:.0f})'.format(table['adult_icu_bed_covid_utilization'].min(), table['adult_icu_bed_covid_utilization'].max()))
        col2.write('* Promedio: {:.3f}'.format(table['adult_icu_bed_covid_utilization'].mean()))
        col2.write('* Desviación estándar: {:.3f}'.format(table['adult_icu_bed_covid_utilization'].std()))
        table_0_6_1 = table_0_6[['date','adult_icu_bed_covid_utilization']].groupby('date').sum()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = table_0_6_1['adult_icu_bed_covid_utilization']))
        fig.update_layout(
            title='Distribución',
            xaxis_title = 'Valores',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('----')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_6_1.index, y = table_0_6_1['adult_icu_bed_covid_utilization']))
        fig.update_layout(
            title='Porcentaje de camas de UCI para COVID-19',
            xaxis_title = 'Fecha',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_6_1.sort_values('adult_icu_bed_covid_utilization', ascending=False).head())
        st.write('----')
        table_0_6_2 = table_0_6[['state','adult_icu_bed_covid_utilization']].groupby('state').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_6_2['state'],
                                    locationmode='USA-states',
                                    z = table_0_6_2['adult_icu_bed_covid_utilization'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Pacientes en cama',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Porcentaje de camas de UCI para COVID-19',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_6_2.sort_values('adult_icu_bed_covid_utilization', ascending=False).head())
    with tabs[7]:
        st.write('Columna a analizar: **{}**'.format(cols.values[7]))
        table_0_7 = table[['date', 'state','critical_staffing_shortage_today_yes']].copy()
        table_0_7.dropna(inplace = True)
        col1, col2 = st.columns(2)
        col1.write('* Cantidad de datos: {}'.format(len(table['critical_staffing_shortage_today_yes'].dropna())))
        col1.write('* Cantidad de datos faltantes: {}'.format(len(table[table['critical_staffing_shortage_today_yes'].isna()])))
        col1.write('* Cantidad de valores únicos: {}'.format(len(np.unique(table['critical_staffing_shortage_today_yes']))))
        col2.write('* Rango de valores: ({:.0f} , {:.0f})'.format(table['critical_staffing_shortage_today_yes'].min(), table['critical_staffing_shortage_today_yes'].max()))
        col2.write('* Promedio: {:.3f}'.format(table['critical_staffing_shortage_today_yes'].mean()))
        col2.write('* Desviación estándar: {:.3f}'.format(table['critical_staffing_shortage_today_yes'].std()))
        table_0_7_1 = table_0_7[['date','critical_staffing_shortage_today_yes']].groupby('date').sum()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = table_0_7_1['critical_staffing_shortage_today_yes']))
        fig.update_layout(
            title='Distribución',
            xaxis_title = 'Valores',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('----')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = table_0_7_1.index, y = table_0_7_1['critical_staffing_shortage_today_yes']))
        fig.update_layout(
            title='Hospitales que han reportado falta de personal',
            xaxis_title = 'Fecha',
            yaxis_title = 'Cantidad')
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_7_1.sort_values('critical_staffing_shortage_today_yes', ascending=False).head())
        st.write('----')
        table_0_7_2 = table_0_7[['state','critical_staffing_shortage_today_yes']].groupby('state').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table_0_7_2['state'],
                                    locationmode='USA-states',
                                    z = table_0_7_2['critical_staffing_shortage_today_yes'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Pacientes en cama',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Hospitales que han reportado falta de personal',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))
        st.plotly_chart(fig)
        st.write('**Top 5:**')
        st.table(table_0_7_2.sort_values('critical_staffing_shortage_today_yes', ascending=False).head())
# ------------------------------------------------------------------------------------------------------------
def page_1():
    st.title('Exploración basada en preguntas')
    tabs = st.tabs(['1- Ocupación','2 - Intervalos','3 - UCI','4 - Pediatría','5 - UCI y COVID-19','6 - Muertes','7 - Personal','8 - Peor Mes'])
    
    
    # 1 Ocupación Hospitalaria
    with tabs[0]:
        st.write('## Pacientes en cama con COVID-19')
        st.write('Ocupación hospitalaria de camas con pacientes con covid')
        st.write('**Argumentos para analizar:**')
        cols = st.columns(2)
        fecha_inicial = dt.datetime.strptime(cols[0].date_input('Fecha inicial:', dt.datetime(2020,1,1), key='01_1').strftime("%Y-%m-%d"), "%Y-%m-%d")
        fecha_final = dt.datetime.strptime(cols[0].date_input('Fecha final:', dt.datetime(2020,6,30), key='01_2').strftime("%Y-%m-%d"), "%Y-%m-%d")
        top_n = cols[0].slider('Número top a mostrar:', 1, 54, 5)
        if fecha_inicial > fecha_final: st.error('Error, la fecha inicial es mayor que la final')
        table01 = table[(table['date'] >= fecha_inicial) & (table['date'] <= fecha_final)].copy()
        table01 = table01[['date', 'state', 'inpatient_beds_used_covid']]
        table01.dropna(inplace=True)
        table01.reset_index(drop=True, inplace=True)
        top_oc_hosp = table01[['state','inpatient_beds_used_covid']].groupby('state').sum().sort_values('inpatient_beds_used_covid', ascending=False)
        top_oc_hosp.rename(columns={'inpatient_beds_used_covid':'Camas usadas por covid'}, inplace=True)
        top_oc_hosp.reset_index(inplace=True)
        top_oc_hosp.rename(columns={'state':'Estado'}, inplace=True)
        cols[1].dataframe(top_oc_hosp.head(top_n), height=260)
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=top_oc_hosp['Estado'],
                                    locationmode='USA-states',
                                    z = top_oc_hosp['Camas usadas por covid'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Camas por covid',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Total de pacientes en cama por covid',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))       
        st.plotly_chart(fig)


    # 2 Intervalos
    with tabs[1]:
        st.write('## Intervalos de comportamiento y puntos críticos')
        st.write('Analizaremos la misma columna (**inpatient_beds_used_covid**) para ver ahora su comportamiento')
        st.write('**Argumentos para analizar:**')
        cols2 = st.columns(2)
        fecha_inicial = dt.datetime.strptime(cols2[0].date_input('Fecha inicial:', dt.datetime(2020,3,22), key='02_1').strftime("%Y-%m-%d"), "%Y-%m-%d")
        fecha_final = dt.datetime.strptime(cols2[0].date_input('Fecha final:', dt.datetime(2020,6,13), key='02_2').strftime("%Y-%m-%d"), "%Y-%m-%d")
        if fecha_inicial > fecha_final: st.error('Error, la fecha inicial es mayor que la final')
        state = cols2[0].selectbox('Introduzca estado:', list(np.unique(table01['state'].values)))
        table02 = table[(table['date'] >= fecha_inicial) & (table['date'] <= fecha_final) & (table['state'] == state)].copy()
        table02 = table02[['date', 'inpatient_beds_used_covid']]
        table02.reset_index(drop=True, inplace=True)
        table02.rename(columns={'date':'Fecha', 'state':'Estado', 'inpatient_beds_used_covid':'Ocupación de camas por Covid'}, inplace = True)
        add_criticos(table02, 'Ocupación de camas por Covid')
        cols2[1].dataframe(table02, height=260)
        fig = go.Figure()
        x0 = table02.loc[0,'Fecha']
        comp = table02.loc[0,'Comportamiento']
        for index in table02.index:
            if index == 0:
                continue
            elif table02.loc[index,'Comportamiento'] == '--':
                x1 = table02.loc[index,'Fecha']
                if comp == 'Creciente': color = 'red'
                else: color = 'green'
                fig.add_vrect(x0,x1, fillcolor=color, line_width=0, opacity=0.2, annotation_text=comp[0], annotation_position="bottom left")
                x0 = table02.loc[index,'Fecha']
                if comp == 'Creciente': comp = 'Decreciente'
                else: comp = 'Creciente'
                continue
            elif index == table02.index[-1]:
                x1 = table02.loc[index,'Fecha']
                if comp == 'Creciente': color = 'red'
                else: color = 'green'
                fig.add_vrect(x0,x1, fillcolor=color, line_width=0, opacity=0.2, annotation_text=comp[0], annotation_position="bottom left",)
                continue
        fig.add_trace(go.Scatter(x = table02['Fecha'], y = table02['Ocupación de camas por Covid'], mode='lines', name='Número de camas'))
        table02_ = table02[table02['Criticos'] == 'Máximo']
        fig.add_trace(go.Scatter(x = table02_['Fecha'], y = table02_['Ocupación de camas por Covid'], mode='markers', name='Máximos'))
        table02_ = table02[table02['Criticos'] == 'Mínimo']
        fig.add_trace(go.Scatter(x = table02_['Fecha'], y = table02_['Ocupación de camas por Covid'], mode='markers', name='Mínimos'))
        fig.update_layout(
            title='Ocupación de camas por Covid en ' + state,
            xaxis_title = 'Fecha',
            yaxis_title = 'Número de camas')
        st.plotly_chart(fig)
        if state == 'NY':
            fuente = 'https://en.m.wikipedia.org/wiki/COVID-19_lockdowns'
            link = 'https://pix11.com/news/coronavirus/latest-coronavirus-updates-in-new-york-tuesday-april-14-2020/'
            st.info('Las fechas sugeridas corresponden al inicio y fin de la pandemia. Fuente:'+fuente)
            st.write('El punto máximo de camas para pacientes con COVID fue el **14 de abril del 2020.**')
            st.write('En ese día el gobernador de NY anunció que según métricas habían llegado al tope:')
            st.image('capture01.PNG', 'Fuente'+link)
        

    # 3 - UCI
    with tabs[2]:
        st.write('## Pacientes en camas de UCI (unidad de cuidado intensivo)')
        st.write('¿Cuáles fueron los estados que ocuparon mayor cantidad de camas dado cierto periodo de tiempo?')
        st.write('**Argumentos para analizar:**')    
        cols3 = st.columns(2)
        fecha_inicial = dt.datetime.strptime(cols3[0].date_input('Fecha inicial:', dt.datetime(2020,1,1), key='03_1').strftime("%Y-%m-%d"), "%Y-%m-%d")
        fecha_final = dt.datetime.strptime(cols3[0].date_input('Fecha final:', dt.datetime(2020,12,31), key='03_2').strftime("%Y-%m-%d"), "%Y-%m-%d")
        top_n = cols3[0].slider('Número top a mostrar:', 5, 54, 5, key='03_1')
        if fecha_inicial > fecha_final: st.error('Error, la fecha inicial es mayor que la final')
        table03 = table[(table['date'] >= fecha_inicial) & (table['date'] <= fecha_final)].copy()
        table03 = table03[['date', 'state', 'staffed_adult_icu_bed_occupancy']]
        table03.dropna(inplace=True)
        table03.reset_index(drop=True, inplace=True)
        table03.rename(columns={'date':'Fecha', 'state':'Estado', 'staffed_adult_icu_bed_occupancy':'Ocupación de camas por adultos en UCI'}, inplace = True)
        table03 = table03[['Estado', 'Ocupación de camas por adultos en UCI']].groupby('Estado').sum().sort_values('Ocupación de camas por adultos en UCI', ascending=False).reset_index()
        cols3[1].dataframe(table03.head(top_n), height=260)
        colors03 = ['rgb(179,179,179)']*top_n
        colors03[:5] = ['rgb(228,26,28)']*5
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table03['Estado'],
                                    locationmode='USA-states',
                                    z = table03['Ocupación de camas por adultos en UCI'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Camas por covid',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Ocupación de camas por adultos en UCI',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))       
        st.plotly_chart(fig)
        fig = go.Figure()
        trace03 = go.Bar(x = table03.head(top_n)['Estado'], 
                        y = table03.head(top_n)['Ocupación de camas por adultos en UCI'],
                        marker_color = colors03, text=table03.head(top_n)['Ocupación de camas por adultos en UCI'])
        fig.add_trace(trace03)
        fig.update_layout(title='Ocupación de camas por adultos en UCI', xaxis_title='Estados')
        fig.update_traces(texttemplate='%{text:.3s}', textposition='auto')
        st.plotly_chart(fig)


    # 4 - Pediatría
    with tabs[3]:
        st.write('## Camas com pacientes pediátricos')
        st.write('Por estado, ¿cuál fue la cantidad de camas para pacientes pediátricos utilizadas?')
        st.write('**Argumentos para analizar:**')          
        cols4 = st.columns(2)
        fecha_inicial = dt.datetime.strptime(cols4[0].date_input('Fecha inicial:', dt.datetime(2020,1,1), key='04_1').strftime("%Y-%m-%d"), "%Y-%m-%d")
        fecha_final = dt.datetime.strptime(cols4[1].date_input('Fecha final:', dt.datetime(2020,12,31), key='04_2').strftime("%Y-%m-%d"), "%Y-%m-%d")
        if fecha_inicial > fecha_final: st.error('Error, la fecha inicial es mayor que la final')
        table04 = table[(table['date'] >= fecha_inicial) & (table['date'] <= fecha_final)].copy()
        table04 = table04[['state', 'all_pediatric_inpatient_bed_occupied']]
        table04.dropna(inplace=True)
        table04.reset_index(drop=True, inplace=True)
        table04.rename(columns={'state':'Estado', 'all_pediatric_inpatient_bed_occupied':'Camas ocupadas para pacientes pediátricos con COVID-19'}, inplace = True)
        table04 = table04[['Estado', 'Camas ocupadas para pacientes pediátricos con COVID-19']].groupby('Estado').sum().sort_values('Camas ocupadas para pacientes pediátricos con COVID-19', ascending=False).reset_index()
        colors04 = ['rgb(179,179,179)']*54
        colors04[:5] = ['rgb(228,26,28)']*5
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table04['Estado'],
                                    locationmode='USA-states',
                                    z = table04['Camas ocupadas para pacientes pediátricos con COVID-19'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Camas para pacientes pediátricos',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Ocupación de camas para pacientes pediátricos',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))       
        st.plotly_chart(fig)
        fig = go.Figure()
        trace04 = go.Bar(x = table04['Estado'], 
                        y = table04['Camas ocupadas para pacientes pediátricos con COVID-19'],
                        marker_color = colors04, text=table04['Camas ocupadas para pacientes pediátricos con COVID-19'])
        fig.add_trace(trace04)
        fig.update_layout(title='Camas ocupadas para pacientes pediátricos con COVID-19')
        fig.update_traces(texttemplate='%{text:.0s}', textposition='auto')
        st.plotly_chart(fig)


    # 5 - UCI y COVID-19
    with tabs[4]:
        st.write('## Porcentaje de camas de UCI con pacientes con COVID-19')
        st.write('Por estado, ¿cuál es el porcentaje de camas de UCI que corresponden a pacientes con COVID-19?')
        st.write('**Argumentos para analizar:**')
        cols5 = st.columns(2)
        fecha_inicial = dt.datetime.strptime(cols5[0].date_input('Fecha inicial:', dt.datetime(2020,1,1), key='05_1').strftime("%Y-%m-%d"), "%Y-%m-%d")
        fecha_final = dt.datetime.strptime(cols5[1].date_input('Fecha final:', dt.datetime(2022,8,8), key='05_2').strftime("%Y-%m-%d"), "%Y-%m-%d")
        if fecha_inicial > fecha_final: st.error('Error, la fecha inicial es mayor que la final')
        table05 = table[(table['date'] >= fecha_inicial) & (table['date'] <= fecha_final)].copy()
        table05 = table05[['state', 'adult_icu_bed_covid_utilization']]
        table05.dropna(inplace=True)
        table05.reset_index(drop=True, inplace=True)
        table05.rename(columns={'state':'Estado', 'adult_icu_bed_covid_utilization':'Porcentaje de camas UCI para covid'}, inplace = True)
        table05 = table05[['Estado', 'Porcentaje de camas UCI para covid']].groupby('Estado').mean().sort_values('Porcentaje de camas UCI para covid', ascending=False).reset_index()
        colors05 = ['rgb(179,179,179)']*54
        colors05[:5] = ['rgb(228,26,28)']*5
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table05['Estado'],
                                    locationmode='USA-states',
                                    z = table05['Porcentaje de camas UCI para covid'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Camas para pacientes pedriáticos',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Porcentaje de camas UCI para covid por estado',
                          geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                          autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))       
        st.plotly_chart(fig)
        fig = go.Figure()
        trace05 = go.Bar(x = table05['Estado'], 
                        y = table05['Porcentaje de camas UCI para covid'],
                        text=table05['Porcentaje de camas UCI para covid'],
                        marker_color = colors05)
        fig.add_trace(trace05)
        fig.update_layout(title='Porcentaje promedio histórico de camas UCI usadas para casos de COVID-19')
        fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
        st.plotly_chart(fig)
        st.write('**Top estados** con mayor porcentaje de camas de UCI para COVID-19')
        top_n = st.slider('Número top a mostrar:', 5, 54, 5, key='05_1')
        st.table(table05.head(top_n))


    # Muertes por covid-19
    with tabs[5]:
        st.write('## Muertes por COVID-19 por estado')
        st.write('Por estado, ¿cuál es el total de fallecimientos a causa del COVID-19?')
        st.write('**Argumentos para analizar:**')
        cols = st.columns(2)
        fecha_inicial = dt.datetime.strptime(cols[0].date_input('Fecha inicial:', dt.datetime(2021,1,1), key='06_1').strftime("%Y-%m-%d"), "%Y-%m-%d")
        fecha_final = dt.datetime.strptime(cols[1].date_input('Fecha final:', dt.datetime(2021,12,31), key='06_2').strftime("%Y-%m-%d"), "%Y-%m-%d")
        if fecha_inicial > fecha_final: st.error('Error, la fecha inicial es mayor que la final')
        table06 = table[(table['date'] >= fecha_inicial) & (table['date'] <= fecha_final)].copy()
        table06 = table06[['state', 'deaths_covid']]
        table06.dropna(inplace=True)
        table06.rename(columns={'state':'Estado', 'deaths_covid':'Muertes por covid'}, inplace = True)
        table06 = table06[['Estado', 'Muertes por covid']].groupby('Estado').sum().sort_values('Muertes por covid', ascending=False).reset_index()
        colors06 = ['rgb(179,179,179)']*54
        colors06[:5] = ['rgb(228,26,28)']*5
        fig = go.Figure()
        fig.add_trace(go.Choropleth(locations=table06['Estado'],
                                    locationmode='USA-states',
                                    z = table06['Muertes por covid'],
                                    colorscale = 'Inferno_r',
                                    colorbar_title = 'Cantidad',
                                    marker_line_color='rgba(0,0,0,0)'))
        fig.update_layout(title='Muertes causadas por COVID-19',
                        geo_scope='usa', paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor = 'rgba(0,0,0,0)',
                        autosize=False, margin = dict(l=0, r=0, b=0, t=25, pad=4, autoexpand=True))       
        st.plotly_chart(fig)
        with st.expander('Gráfico de barras'):
            fig = go.Figure()
            trace06 = go.Bar(x = table06['Estado'], 
                            y = table06['Muertes por covid'],
                            marker_color = colors06, text=table06['Muertes por covid'])
            fig.add_trace(trace06)
            fig.update_layout(title='Total de muertes por COVID-19 por estado en el año 2021')
            fig.update_traces(texttemplate='%{text:.0s}', textposition='auto')
            st.plotly_chart(fig)
        with st.expander('Tabla top estados'):
            st.write('**Top estados** con mayor cantidad de fallecimientos por COVID-19')
            top_n = st.slider('Número top a mostrar:', 5, 54, 5, key='06_1')
            st.table(table06.head(top_n))


    # 7 - Falta de personal
    with tabs[6]:
        st.write('## Relación de la falta de personal con los facllecimientos por COVID-19')
        st.write('¿Qué relación hay entre estas variables?')
        table07 = table[['date', 'deaths_covid', 'critical_staffing_shortage_today_yes']].copy()
        table07.dropna(inplace=True)
        table07 = table07.groupby('date').sum().reset_index(drop = True)
        st.write('Gráficos a ver:')
        tabs_7_1 = st.tabs(['Dispersión', 'Histograma muertes', 'Histograma falta de personal'])
        with tabs_7_1[0]:
            fig = go.Figure()
            trace07 = go.Scatter(y = table07['deaths_covid'],
                                x = table07['critical_staffing_shortage_today_yes'], mode = 'markers')
            fig.add_trace(trace07)
            fig.update_layout(
                title='Relación muertes por covid con falta de personal',
                yaxis_title = 'Muertes por Covid',
                xaxis_title = 'Número de hospitales con falta de personal')
            st.plotly_chart(fig)
        with tabs_7_1[1]:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x = table07['deaths_covid']))
            fig.update_layout(title='Distribución de muertes por covid-19') 
            st.plotly_chart(fig)
        with tabs_7_1[2]:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x = table07['critical_staffing_shortage_today_yes']))
            fig.update_layout(title='Distribución de falta de personal') 
            st.plotly_chart(fig)
        min = st.slider('Valor mínimo de hospitales con falta de personal', 0, 400, 0)
        tabs_7_2 = st.tabs(['Regresión lineal con x, y', 'Regresión cuadrático con x^2, y'])
        table_r = table07[table07['critical_staffing_shortage_today_yes'] >= min].copy()
        with tabs_7_2[0]:
            X = table_r['critical_staffing_shortage_today_yes'].values.reshape(-1,1)
            y = table_r['deaths_covid'].values
            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)
            lr = LinearRegression(fit_intercept=True)
            lr.fit(X_tr, y_tr)
            y_pr_tr = lr.predict(X_tr)
            y_pr_te = lr.predict(X_te)
            fig = go.Figure()
            fig.add_trace(go.Scatter(y = table_r['deaths_covid'], x = table_r['critical_staffing_shortage_today_yes'], mode = 'markers', name='Datos'))
            fig.add_trace(go.Scatter(x = X_tr.reshape(-1), y = y_pr_tr, mode='markers', name='Train Data'))
            fig.add_trace(go.Scatter(x = X_te.reshape(-1), y = y_pr_te, mode='markers', name='Test Data'))
            fig.update_layout(
                title='Predicciones',
                xaxis_title = 'Falta de personal médico',
                yaxis_title = 'Muertes por COVID-19')
            st.plotly_chart(fig)
            st.write('**Error en predicciones (MSE):** {}'.format(mean_squared_error(y_te,y_pr_te)))
            pass
        with tabs_7_2[1]:
            X = table_r['critical_staffing_shortage_today_yes'].values
            X = (X)**2
            X = X.reshape(-1,1)
            y = table_r['deaths_covid'].values
            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)
            lr = LinearRegression(fit_intercept=True)
            lr.fit(X_tr, y_tr)
            y_pr_tr = lr.predict(X_tr)
            y_pr_te = lr.predict(X_te)
            fig = go.Figure()
            X_tr = X_tr.reshape(-1)
            X_tr = X_tr**0.5
            X_te = X_te.reshape(-1)
            X_te = X_te**0.5
            fig.add_trace(go.Scatter(y = table_r['deaths_covid'], x = table_r['critical_staffing_shortage_today_yes'], mode = 'markers', name='Datos'))
            fig.add_trace(go.Scatter(x = X_tr, y = y_pr_tr, mode='markers', name='Train Data'))
            fig.add_trace(go.Scatter(x = X_te, y = y_pr_te, mode='markers', name='Test Data'))
            fig.update_layout(
                title='Predicciones',
                xaxis_title = 'Falta de personal médico',
                yaxis_title = 'Muertes por COVID-19')
            st.plotly_chart(fig)
            st.write('**Error en predicciones (MSE):** {}'.format(mean_squared_error(y_te,y_pr_te)))
            pass
    

    # 8 - Peor mes
    with tabs[7]:
        st.write('## El peor mes de la pandemia en estados unidos')
        st.write('Dependiendo de las métricas, podemos concluir que X mes fue el peor:')
        metrics = st.selectbox('Seleccione métrica:', ['Muertes Covid', 'Pacientes en cama por covid', 'Falta de personal', 'Promedio de las 3'])
        table08 = table[['date', 'deaths_covid', 'inpatient_beds_used_covid', 'critical_staffing_shortage_today_yes']].copy()
        table08['date'] = table08['date'].map(lambda x: dt.datetime.strptime(x.strftime('%Y-%m'), '%Y-%m'))
        table08 = table08.groupby(['date']).sum().reset_index()
        if metrics == 'Muertes Covid':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['deaths_covid'], 
                          name='Muertes por covid',
                          line=dict(color='rgba(228,26,28, 1)', width=2)))
            fig.update_layout(title='Muertes por covid', xaxis_title = 'Mes')
            st.plotly_chart(fig)
            st.write('Escalando al valor máximo:')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['deaths_covid']/ (table08['deaths_covid'].max()), 
                          name='Muertes por covid',
                          line=dict(color='rgba(228,26,28, 1)', width=2, dash='dash')))
            fig.update_layout(title='Muertes por covid', xaxis_title = 'Mes', yaxis_title='Porcentaje del valor máximo')
            st.plotly_chart(fig)
            st.write('**Peor mes según esta métrica: Enero 2021**')
        elif metrics == 'Pacientes en cama por covid':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['inpatient_beds_used_covid'], 
                          name='Personas con COVID en cama',
                          line=dict(color='rgba(55, 126, 184, 1)', width=2)))
            fig.update_layout(title='Personas con COVID en cama', xaxis_title = 'Mes')
            st.plotly_chart(fig)
            st.write('Escalando al valor máximo:')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['inpatient_beds_used_covid']/ (table08['inpatient_beds_used_covid'].max()), 
                          name='Personas con COVID en cama',
                          line=dict(color='rgba(55, 126, 184, 1)', width=2, dash='dash')))
            fig.update_layout(title='Personas con COVID en cama', xaxis_title = 'Mes', yaxis_title='Porcentaje del valor máximo')
            st.plotly_chart(fig)
            st.write('**Peor mes según esta métrica: Enero 2022**')
        elif metrics == 'Falta de personal':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['critical_staffing_shortage_today_yes'], 
                          name='Falta de personal médico',
                          line=dict(color='rgba(77, 175, 74, 1)', width=2)))
            fig.update_layout(title='Falta de personal médico', xaxis_title = 'Mes')
            st.plotly_chart(fig)
            st.write('Escalando al valor máximo:')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['critical_staffing_shortage_today_yes']/ (table08['critical_staffing_shortage_today_yes'].max()), 
                          name='Falta de personal médico',
                          line=dict(color='rgba(77, 175, 74, 1)', width=2, dash='dash')))
            fig.update_layout(title='Falta de personal médico', xaxis_title = 'Mes', yaxis_title='Porcentaje del valor máximo')
            st.plotly_chart(fig)
            st.write('**Peor mes según esta métrica: Diciembre 2020**')
        else:
            st.write('Esta métrica consiste en promediar las escaladas anteriores')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['deaths_covid']/ (table08['deaths_covid'].max()), 
                          name='Muertes por covid',
                          line=dict(color='rgba(228,26,28, 1)', width=2, dash='dash')))
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['inpatient_beds_used_covid']/ (table08['inpatient_beds_used_covid'].max()), 
                          name='Personas con COVID en cama',
                          line=dict(color='rgba(55, 126, 184, 1)', width=2, dash='dash')))
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['critical_staffing_shortage_today_yes']/ (table08['critical_staffing_shortage_today_yes'].max()), 
                          name='Falta de personal médico',
                          line=dict(color='rgba(77, 175, 74, 1)', width=2, dash='dash')))
            fig.update_layout(title='Falta de personal médico', xaxis_title = 'Mes', yaxis_title='Porcentaje del valor máximo')
            table08['prom_indicators'] = (table08['deaths_covid']/ (table08['deaths_covid'].max()) + table08['inpatient_beds_used_covid']/(table08['inpatient_beds_used_covid'].max()) + table08['critical_staffing_shortage_today_yes']/(table08['critical_staffing_shortage_today_yes'].max())) / 3
            fig.add_trace(go.Scatter(x = table08['date'], 
                          y = table08['prom_indicators'], 
                          name='Promedio de los 3 indicadores',
                          line=dict(color='rgba(0, 0, 0, 1)', width=3)))
            st.plotly_chart(fig)
            st.write('**Peor mes según esta métrica: Enero 2021**')
            st.info('El mes de Enero del 2021 se consideró el peor de la pandemia según varios medios:')
            st.image('Capture02.PNG')
# ------------------------------------------------------------------------------------------------------------
def page_2():
    st.title('Conclusiones')
    st.write('### * A lo largo de las exploraciones de los datos se puede concluir que los estados más',
             'afecatos fueron Nueva York, California y Texas.')
    st.write('### * El peor momento en la pandemia ha sido el enero del 2021.')
    st.write('### * En enero de todos los años hay un repunte debido a la falta de personal en el',
             'mes pasado y a las temperaturas frías.')
    st.write('### * Los gráficos coinciden en que los meses cálidos (sobre todo Junio y Julio) son los',
             'mejores meses del año.')
    st.write('### * Se recomendaría preparar personal antes de las temperaturas frías para poder',
             'abordar de mejor manera la pandemia. Esto debido a que la falta de personal médico',
             'crea tendencia a mayor número de muertes.')
    st.write('### * Aprovechar los climas cálidos para escatimar en gastos y poder usarlos en invierno.')
    


page_names_to_funcs = {
    "1 - Página Principal": page_0,
    "2 - Exploración basada en preguntas": page_1,
    "3 - Conclusiones": page_2,
}

selected_page = st.sidebar.selectbox("Seleccione página", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()