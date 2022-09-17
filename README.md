_____
# Proyecto Análisis CDC (centro de control y prevención de enfermedades, en lapandemia COVID-19)

La COVID-19 afecta de distintas maneras en función de cada persona. La mayoría de las personas que se contagian presentan síntomas de intensidad leve o moderada, y se recuperan sin necesidad de hospitalización, sin embargo se tuvo una alta tasa de mortalidad en el país (EEUU).

_____
### 1 - ¿Cuáles fueron los 5 Estados con mayor ocupación hospitalaria por COVID? Criterio de ocupación por cama común. Considere la cantidad de camas ocupadas con pacientes confirmados y tome como referencia los 6 primeros meses del 2020 - recuerde incluir la cifra de infectados en esos meses (acumulativo). ¿Influye el rango etario en este comportamiento?

| state   | state_name       |   Percentege_bed_used |
|:--------|:-----------------|----------------------:|
| NY      | Nueva York   |               21.3473 |
| NJ      | Nueva Jersey |               20.2405 |
| MA      | Massachusetts    |               17.7679 |
| CT      | Connecticut      |               14.5507 |
| LA      | Luisiana     |               13.7848 |

![src\img01.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img01.png)

______
### 2 - Analice la ocupación de camas (Común) por COVID en el Estado de Nueva York durante la cuarentena establecida e indique:
- Intervalos de crecimiento y decrecimiento
- Puntos críticos (mínimos y máximos)

|    | Desc        | date                |   inpatient_beds_used_covid |
|---:|:------------|:--------------------|----------------------------:|
|  0 | Pico Maximo | 2020-04-04 00:00:00 |                       13107 |
|  1 | Pico Minimo | 2020-04-05 00:00:00 |                       12363 |
|  2 | Pico Maximo | 2020-04-06 00:00:00 |                       12711 |
|  3 | Pico Minimo | 2020-04-07 00:00:00 |                       12611 |
|  4 | Pico Maximo | 2020-04-10 00:00:00 |                       13369 |
|  5 | Pico Minimo | 2020-04-11 00:00:00 |                       13361 |
|  6 | Pico Maximo | 2020-04-14 00:00:00 |                       14126 |
|  7 | Pico Minimo | 2020-04-19 00:00:00 |                       12496 |
|  8 | Pico Maximo | 2020-04-20 00:00:00 |                       12507 |
|  9 | Pico Minimo | 2020-04-21 00:00:00 |                       12335 |
| 10 | Pico Maximo | 2020-04-22 00:00:00 |                       13005 |
| 11 | Pico Minimo | 2020-05-10 00:00:00 |                        6674 |
| 12 | Pico Maximo | 2020-05-12 00:00:00 |                        8237 |
| 13 | Pico Minimo | 2020-05-17 00:00:00 |                        5966 |
| 14 | Pico Maximo | 2020-05-18 00:00:00 |                        6110 |
| 15 | Pico Minimo | 2020-05-24 00:00:00 |                        4659 |
| 16 | Pico Minimo | 2020-06-02 00:00:00 |                        3805 |
| 17 | Pico Maximo | 2020-05-26 00:00:00 |                        4708 |
| 18 | Pico Maximo | 2020-06-04 00:00:00 |                        4261 |

![src\img02.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img02.png)
_____
### 3 - ¿Cuáles fueron los cinco Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020? La medición debe realizarse en términos absolutos.


Los estados con ocuparon mas camas UCI, 2020: 
 |    | state_name      | state   |   total_camas |
|---:|:----------------|:--------|--------------:|
|  0 | California      | CA      |          4417 |
|  1 | Texas​       | TX      |          4097 |
|  2 | Florida         | FL      |          3523 |
|  3 | Nueva York | NY      |          2448 |
|  4 | Pensilvania​ | PA      |          2180 |

![src\img01.png](https://github.com/Jhlirion/DS-PI-ProyectoIndividual/blob/main/src/img03.png)