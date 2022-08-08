![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)

# Proyecto Individual \#2



## Descripción

El CDC (centro de control y prevención de enfermedades) de EE. UU. es la entidad encargada de monitorear la salud pública y desarrollar estrategias para la prevención y control de enfermedades. Por esto ha contratado a nuestra consultora para organizar, en base a los datos recolectados, los recursos hospitalarios para prevenir que lo ocurrido durante la pandemia COVID-19 suceda de vuelta.

## API o .csv

Nos disponibilizan desde el departamento de Data Engineering un archivo .csv (detalle [aquí](https://healthdata.gov/Hospital/COVID-19-Reported-Patient-Impact-and-Hospital-Capa/g62h-syeh)), el cuál podemos usar para realizar nuestro análisis. Nuestro Team Líder, a su vez, nos facilitó información sobre la [API](https://dev.socrata.com/foundry/healthdata.gov/g62h-syeh), aclarando que podemos usarla como alternativa. El análisis solicitado, debe contemplar los datos hasta el 01/08/2022 inclusive.

## Cuestionario

Para guiar nuestro trabajo, nuestro Team Líder nos facilita un cuestionario. Entonces, usando los datos ingestados anteriormente debemos responder:

1 - ¿Cuáles fueron los 5 Estados con mayor ocupación hospitalaria por COVID? Criterio de ocupación por cama común. Considere la cantidad de camas ocupadas con pacientes confirmados y tome como referencia los 6 primeros meses del 2020 - recuerde incluir la cifra de infectados en esos meses (acumulativo). ¿Influye el rango etario en este comportamiento?

2 - Analice la ocupación de camas (Común) por COVID en el Estado de Nueva York durante la cuarentena establecida e indique:
- Intervalos de crecimiento y decrecimiento
- Puntos críticos (mínimos y máximos)

3 - ¿Cuáles fueron los cinco Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020? La medición debe realizarse en términos absolutos. 

4 - ¿Qué cantidad de camas se utilizaron, por Estado, para pacientes pediátricos con COVID durante el 2020?

5 - ¿Qué porcentaje de camas UCI corresponden a casos confirmados de COVID-19? Agrupe por Estado.

6 - ¿Cuántas muertes por covid hubo, por Estado, durante el año 2021? 

7 - ¿Qué relación presenta la falta de camas UCI disponibles con la cantidad de muertes durante el año 2021?

8 - Siguiendo las respuestas anteriores, ¿cuál fue el peor mes de la pandemia para USA en su conjunto? Puede utilizar otras medidas que considere necesarias.

9 - ¿Qué recomendaciones haría, ex post, con respecto a los recursos hospitalarios y su uso?

## Dashboard

 A raíz de nuestro informe, el Congreso de los Estados Unidos de América le pide a nuestra firma que realice una presentación y la ponga a disposición de sus miembros, recordando lo que vivió el país durante la pandemia.

La presentación deberá contener deberá contener, como mínimo:

- Un mapa que muestre la cantidad de hospitalizados debido al COVID-19 por Estado.
- Uso de camas UCI por Estado.
- Ranking de Estados con mayor ocupación hospitalaria por COVID
- Cantidad de camas ocupadas por COVID-19 entre dos fechas elegidas por el usuario.

Nuestro Team Líder nos pide que nos encarguemos de la construcción de este dashboard, usando una herramienta de nuestra preferencia. Sin embargo, nos recomienda usar [streamlit](https://docs.streamlit.io/library/get-started). Streamlit nos permite crear dashboards de manera ágil y rápida con Python, sin tener que saber HTML o CSS.

## Sugerencias
- Analizar muy bien el diccionario de datos, observar qué dato ofrece cada columna del dataset.

### Streamlit
Permite crear dashboards y presentaciones de data sólo con Python.

### Power Bi
El dataset puede ser ingestado directamente desde Power Bi, seleccionando 'Obtener Datos' - 'Fuente OData' y colocando el siguiente link
https://healthdata.gov/api/odata/v4/g62h-syeh

