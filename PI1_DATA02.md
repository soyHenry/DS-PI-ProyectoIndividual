### PI 1 DATA 02 SOY HENRY

![image](https://user-images.githubusercontent.com/108296379/182138583-9011699a-f009-4454-885e-80dca182b6c8.png)


## API BCRA
Enlace de la página: https://estadisticasbcra.com/  
Documentación: https://estadisticasbcra.com/api/documentacion

Informe sobre dólar en Argentina para un grupo financiero. Tener en cuenta que la gerencia le puede llegar a requerir nuevas consultas.

Importar librerías  
Automatizar código  
Token BCRA  
Endpoints: se pueden utilizar los que se consideren necesarios  
Autorización y requests  
Función para convertir Json a Dataframe  
Limpieza de datos  
Preguntas
 * Dólar oficial vs Dólar Blue:   
    * Últimos 365 días:
        * 1) Día con mayor variación en la brecha  
        * 2) Top 5 días con mayor variación  
        * 3) Semana con mayor variación en la brecha  
        * 4) Día de la semana donde hay mayor variación en la brecha   


    * General:
        * 5) Con la info histórica del valor del dólar y del blue, realizar un análisis exploratorio. Cruzar la data con sucesos importantes a nivel político-económico y graficar mes a mes.
        
        * 6) Implementar una regresión lineal (una para cada tipo de dólar) para predecir el valor del dólar en:
            * 3 meses
            * 6 meses
            * 12 meses
        * 7) Bonus opcional: Realizar una calculadora de predicción de aumento del dólar


* Inflación vs Dólar
    * Últimos 4 años:
        * 8) Mejor momento para comprar dolár oficial y venderlo a dolár blue
