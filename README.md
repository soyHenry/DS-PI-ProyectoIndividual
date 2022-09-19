_____
# Proyecto Análisis CDC (centro de control y prevención de enfermedades, en lapandemia COVID-19)

La COVID-19 afecta de distintas maneras en función de cada persona. La mayoría de las personas que se contagian presentan síntomas de intensidad leve o moderada, y se recuperan sin necesidad de hospitalización, sin embargo se tuvo una alta tasa de mortalidad en el país (EEUU).

_____
### 1 - Los 5 Estados con mayor ocupación hospitalaria por COVID-19 con pacientes confirmados durante los 6 primeros meses del 2020, como podemos apreciar NY es el estado más golpeado por la pandemia en Estados Unidos y alberga un tercio de los contagios del país y la mitad de las muertes contabilizada, sin embargo para este año solo se tuvo un 21.35% de sus camas usadas por casos Covid con un promedio de 35,925 internos:

| Estado   | Nombre de Estado       |   Camas usadas (%) |
|:--------|:-----------------|----------------------:|
| NY      | Nueva York   |                 21.35 |
| NJ      | Nueva Jersey​ |                 20.24 |
| MA      | Massachusetts    |                 17.77 |
| CT      | Connecticut      |                 14.55 |
| LA      | Luisiana​     |                 13.78 |

![src\img01.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img01.png)

______
### 2 - Durante la cuarentena establecida en el país, Nueva York superó la barrera de los 10.000 muertos por Covid-19 este 13 de abril, asi mismo el este es el más golpeado por la pandemia en Estados Unidos, aqui podemos apreciar el crecimiento de los contagios que fueron exponencial en los primeros meses del inicio de la pandemia y los picos donde alcanzo su maximos casos que requerian internamiento.

|    | Descripcción       | Fecha                |   Camas usadas pacientes covid |
|---:|:------------|:--------------------|----------------------------:|
|  0 | Pico Maximo | 2020-04-04 00:00:00 |                       13107 |
|  1 | Pico Minimo | 2020-04-05 00:00:00 |                       12363 |
|  2 | Pico Maximo | 2020-04-06 00:00:00 |                       12711 |
|  3 | Pico Minimo | 2020-04-07 00:00:00 |                       12611 |
|  4 | Pico Maximo | 2020-04-10 00:00:00 |                       13369 |
|  5 | Pico Minimo | 2020-04-11 00:00:00 |                       13361 |
|  6 | Pico Maximo | 2020-04-14 00:00:00 |                       14126 |


![src\img02.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img02.png)
_____
### 3 - Los estados que ocuparon mayor camas UCI (Unidades de Cuidados Intensivos) durante el año 2020, el aumento de la cantidad de casos se ha convertido en un motivo de preocupación tal que todas las regiones de California, excepto dos, tuvieron órdenes de quedarse en casa provocadas por la capacidad en las unidades de UCI.

Los estados con ocuparon mas camas UCI, 2020: 
 |    | state_name      | state   |   total_camas |
|---:|:----------------|:--------|--------------:|
|  0 | California      | CA      |          4417 |
|  1 | Texas​       | TX      |          4097 |
|  2 | Florida         | FL      |          3523 |
|  3 | Nueva York | NY      |          2448 |
|  4 | Pensilvania​ | PA      |          2180 |

![src\img03.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img03.png)

_____
### 4 - ¿Qué cantidad de camas se utilizaron, por Estado, para pacientes pediátricos con COVID durante el 2020?

|    | state_name      | state   |   total_camas_pedia |
|---:|:----------------|:--------|--------------------:|
|  0 | California      | CA      |                1902 |
|  1 | Nueva York​  | NY      |                1734 |
|  2 | Pensilvania​ | PA      |                1104 |
|  3 | Illinois        | IL      |                1080 |
|  4 | Míchigan  | MI      |                 918 |

![src\img04.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img04.png)

_______
### 5 - ¿Qué porcentaje de camas UCI corresponden a casos confirmados de COVID-19? Agrupe por Estado.

Los estados que ocuparon (%) mas camas UCI: 
 |    | state_name       | state   |   adult_icu_bed_covid_utilization |
|---:|:-----------------|:--------|----------------------------------:|
|  0 | Texas[27]​        | TX      |                          0.229946 |
|  1 | Misisipi[14]​     | MS      |                          0.221417 |
|  2 | Georgia          | GA      |                          0.21672  |
|  3 | Idaho            | ID      |                          0.214566 |
|  4 | Nuevo México[22]​ | NM      |                          0.211469 |

![src\img05.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img05.png)

### 6 - ¿Cuántas muertes por covid hubo, por Estado, durante el año 2021?

Estados con mayor deceso, 2021: 
 |    | state_name     | state   |   deaths_covid |
|---:|:---------------|:--------|---------------:|
|  0 | California     | CA      |          35108 |
|  1 | Texas[27]​      | TX      |          32889 |
|  2 | Florida        | FL      |          26004 |
|  3 | Nueva York[19]​ | NY      |          17620 |
|  4 | Arizona        | AZ      |          16250 |

![src\img06m.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img06m.png)

### 7 - ¿Qué relación presenta la falta de personal médico, con la cantidad de muertes por covid durante el año 2021? (editado) 

### 8 - Siguiendo las respuestas anteriores, ¿cuál fue el peor mes de la pandemia para USA en su conjunto? Puede utilizar otras medidas que considere necesarias.

### 9 - ¿Qué recomendaciones haría, ex post, con respecto a los recursos hospitalarios y su uso?