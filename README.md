![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)



# Trabajo Práctico Individual N°1 - Normalización de Datos

## Una empresa de ventas de productos al público tomo la decision de empezar a ser una empresa Data-driven. 
## ¿Que significa esto? Data-Driven es un concepto en el cual los datos son el centro a la hora de tomar decisiones
## Sin embargo se dieron cuenta que los datos que tiene en sus sistemas pueden no ser de tan buena calidad como ellos creian tener. 

En base a esto, se tomo la decision gerencial de primeramente crear una base de datos, teniendo en cuenta las principales entidades que son las ventas, compras y gastos.
Teniendo dicha base de datos, con sus respectivas tablas, va a ser necesario tener un documento donde se detalle la estructura de la tabla y un diccionario de datos para poder comprender mejor el panorama
Una vez esto se deberia analizar la calidad de la misma, con los datos originales; pudiendo asi encontrar valores faltantes, datos incorrectos y outliers
Antes de proceder con la limpieza, nuestro gerente nos solicito un informe ejecutivo con todo lo que podamos reportar como incorrecto o de mala calidad; luego si podemos proceder a corregirlos o desestimarlos.

Bueno, hasta ahora venimos haciendo una limpieza de datos, mejor conocida como Data Cleansing (OJO tambien venimos construyendo un mini DW y haciendo el trabajo de un Data Engineer)

Pasemos a la parte mas "Data driven" y vamos a poder empezar a darle informacion valiosa al negocio, empecemos por la evolucion de las ventas, compras y gastos.
Que informacion valiosa podemos darle al negocio? Pensemos que KPIs podrian darle un gran valor al negocio para poder tomar decisiones

Ademas de todo esto, el area que se encarga de abrir nuevas sucursales se entero de nuestro trabajo y quiere que los ayudemos a encontrar donde podria abrir la siguiente.
Para ello, vamos a contar con una tabla de localidades (analicemos la calidada tambien, por las dudas) pero no todo viene tan sencillo, tenemos que normalizar la informacion de dicha tabla. Un compañero del equipo nos dijo que hay un algoritmo para hacer una comparacion de palabras que podria ayudarnos con esta tarea, asi que tambien tenemos una tarea de research


Para llevar adelante todo este proceso tenemos los siguientes datasets

Clientes.csv
Compra.csv
Gasto.csv
Localidades.csv
Proveedores.csv
Sucursales.csv
Venta.csv

y a ultimo momento, nos avisaron que hay otro dataset de clientes (Clientes_2.csv) y no nos descartan que puedan aparecer otros, asi que por las dudas deberiamos contemplar que nuestro proceso pueda incluir mas dataset de clientes y que no haya problemas de duplicados.
Esto deberia ser automatico, asi que pensemos algo robusto para no tener problemas a futuro.

Tengan en cuenta que estamos construyendo algo para tomar decisiones ejecutivas ( Directores, algun vicepresidente y/o presidente de la empresa) asi que no podemos tener errores en nuestros reportes! 

Exitooss