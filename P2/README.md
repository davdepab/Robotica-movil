
# PRÁCTICA 2 - FORMULA SIGUE LÍNEAS

El objetivo de esta práctica consiste en, mediante un controlador PD en un bucle infinito, conseguir que un Formula 1 logre recorrer de forma autónoma varios circuitos en el menor tiempo posible, únicamente guiándose a través de una cámara en el trazo de una línea roja.

## DESARROLLO DE LA PRÁCTICA Y BREVE EXPLICACIÓN DEL CÓDIGO:

En primer lugar he tomado los datos obtenidos de la cámara mediante la abstracción 
´´´python
HAL.getImage()
´´´

