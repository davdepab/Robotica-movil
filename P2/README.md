
# PRÁCTICA 2 - F1 SIGUE LÍNEAS

El objetivo de esta práctica consiste en, mediante un controlador PD en un bucle infinito, conseguir que un Formula 1 logre recorrer de forma autónoma varios circuitos en el menor tiempo posible, únicamente guiándose a través de una cámara sobre el trazo de una línea roja.

## DESARROLLO DE LA PRÁCTICA Y BREVE EXPLICACIÓN DEL CÓDIGO:

En primer lugar he tomado los datos obtenidos de la cámara mediante la abstracción **HAL.getImage()** , la cual me proporciona los datos de la cámara en formato RGB, por lo que en primer lugar lo que he hecho ha sido parsearlos a HSV, para evitar problemas con la detección de color en distintas condiciones de iluminación, sombras...  
Con los nuevos datos en formato HSV, dada la distribución de colores y teniendo en cuenta que la línea que ha de seguir el robot es roja, he creado dos máscaras, una para los tonos rojos de la parte inferior y otra para los mismos de la parte superior:  

<img width="720" height="355" alt="gyuw4" src="https://github.com/user-attachments/assets/83a7ab57-5180-4f63-b65f-6753b29b9669" />  

Mediante bitwise combino las máscaras para obtener una única y utilizando **WebGUI.showImage()** la muestro en pantalla para visualizarla en tiempo real.



