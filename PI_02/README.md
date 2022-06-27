![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)



# Trabajo Práctico Individual N°2 - Finanzas 

<p> La empresa tomó la decisión de invertir parte de sus ganancias del año y va a tomar en cuenta el índice del SP500.<br>
Este índice se basa en la capitalización bursátil de 500 grandes empresas que poseen acciones que cotizan en las bolsas NYSE o NASDAQ, y captura aproximadamente el 80% de toda la capitalización de mercado.</p>
Luego del éxito que tuvo el informe ejecutivo y la normalización de datos del proyecto anterior, se solicitó al área de Datos ayuda con el análisis sobre los distintas empresas a lo largo del tiempo para comprender mejor el mercado, y poder tomar decisiones en base a nuestras recomendaciones.

* Se trabajara con los periodos contemplados entre 01/01/2000 y 31/12/2021<br>
Para este trabajo se utilizará la API de yahoo finance, cual posee su librería https://pypi.org/project/yfinance/ y página oficial https://finance.yahoo.com/ <br>


Los indicadores que se tomaron en cuenta fueron los siguientes

- Cual es el mejor día para invertir teniendo en cuenta el retorno de los movimiento gap
- Cual es el mejor día para invertir teniendo en cuenta el retorno de los movimientos intradiarios 
- Cuales son las mejores industrias que pertenecen al SP500 en las cuales se puede invertir
- Cuales fueron los momentos de alta volatilidad que afectaron al SP500
- Cuales son las 9 mejores empresas para invertir



Se pueden utilizar las siguientes librerias para graficar

- matplotlib
- matplotlib finance
- Plotly

Se dejan aqui unos calculos financieros que pueden servir de ayuda:<br>


- retornos_gaps = np.log(aperturas/cierres.shift(1)).fillna(0)<br>

- retornos_intra = np.log(cierres/aperturas).fillna(0)<br>

- variaciones = activo.cierre_ajustado.pct_change()<br>

- volatilidad = activos.variaciones.rolling(250).std()*100*(250)**0.5 (en este caso se puede utilizar el indice VIX)<br>

Se dejan aqui unos ejemplos para la parte grafica:<br>

![img1](https://github.com/soyHenry/DS-PI-ProyectoIndividual/blob/main/PI_02/1655704802024.png)
![img2](https://github.com/soyHenry/DS-PI-ProyectoIndividual/blob/main/PI_02/1655704803889.png)
![img3](https://github.com/soyHenry/DS-PI-ProyectoIndividual/blob/main/PI_02/1655704805872.png)
![img3](https://github.com/soyHenry/DS-PI-ProyectoIndividual/blob/main/PI_02/1655971323111.png)



Es necesario que determinen de manera grafica dichos indicadores.<br>

Por último, recuerden que los reportes que se desarrollarán serán para la toma de decisiones ejecutivas (Directores, vicepresidente y/o presidente de la empresa, etc), por lo tanto es imperativo evitar errores en los mismos. <br>


