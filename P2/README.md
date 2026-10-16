
# PRÁCTICA 2 - F1 SIGUE LÍNEAS

<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/b1a1239f-85b0-4016-a711-a1f36f9db412" />

El objetivo de esta práctica consiste en, mediante un controlador PID en un bucle infinito, conseguir que un Formula 1 logre recorrer de forma autónoma varios circuitos en el menor tiempo posible, únicamente guiándose a través de una cámara sobre el trazo de una línea roja.

## DESARROLLO DE LA PRÁCTICA Y BREVE EXPLICACIÓN DEL CÓDIGO:

En primer lugar he tomado los datos obtenidos de la cámara mediante la abstracción **HAL.getImage()** , la cual me proporciona los datos de la cámara en formato RGB, por lo que en primer lugar lo que he hecho ha sido parsearlos a HSV, para evitar problemas con la detección de color en distintas condiciones de iluminación, sombras...  
Con los nuevos datos en formato HSV, dada la distribución de colores y teniendo en cuenta que la línea que ha de seguir el robot es roja, he creado dos máscaras, una para los tonos rojos de la parte inferior y otra para los mismos de la parte superior:  

<img width="720" height="355" alt="gyuw4" src="https://github.com/user-attachments/assets/83a7ab57-5180-4f63-b65f-6753b29b9669" />  

Mediante bitwise combino las máscaras para obtener una única y utilizando **WebGUI.showImage()** la muestro en pantalla para visualizarla en tiempo real.  

## CONTROLADORES PID:

<img width="1024" height="370" alt="image" src="https://github.com/user-attachments/assets/de0338ad-d785-4882-9c6c-1e7e89494fd4" />  

He utilizado dos controladores PD para calcular en cada iteración del bucle infinito tanto una velocidad lineal como una angular.

### CONTROLADOR PD VELOCIDAD ANGULAR:
La velocidad angular se calcula realizando la resta del centroide de la máscara de la línea roja al centro real de la misma, obteniendose así el error, o variación que existe entre ambas al cual posteriormente multiplicaremos por una Kp obtenida de forma experimental. Por otro lado, obtenemos la derivada del error, que en tiempo discreto no es más que restar al error actual el error anterior, a este valor lo multiplicaremos por Kd, obtenida de la misma forma que Kp. El resultado de la suma de ambos errores multiplicados por sus constantes correspondientes será la velocidad angular que aplicaremos para que el F1 gire de forma controlada y fluida para seguir la línea roja.  

### CONTROLADOR PD VELOCIDAD LINEAL:
Para la velocidad lineal utilizo el valor absoluto del error obtenido anteriormente, el cual multiplico por una nueva constante Kpv, por otro lado obtengo la derivada de la misma forma que el anterior controlador salvo porque esta vez utilizo el error en valor absoluto. Este controlador funciona disminuyendo una velocidad lineal constante a medida que el error es más grande. La velocidad lineal aplicada al robot es igual a la velocidad constante menos el error total obtenido. Así consiguiendo una deceleración proporcional a la intensidad de la curva.

### DEMOSTRACIONES DEL FUNCIONAMIENTO:

En primer lugar muestro el comportamiento del robot al no visualizar la línea, lo único que hará será retroceder a la par que gira hasta que la línea sea visible para así comenzar a recorrer el circuito:  

<img width="400" height="" alt="ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/8154ccd8-b591-48ef-92ad-d05e1ac1ccfb" />  

### VÍDEOS:  

Cabe recalcar que todas las simulaciones realizadas han sido bajo el modelo holonómico, ninguna implementación ha sido implementada bajo el modelo Ackermann

### Modelo Ackermann:  
<img width="638" height="550" alt="image" src="https://github.com/user-attachments/assets/3ff5eb83-c22b-443f-9028-5ce3c1451d86" />  


### Modelo holonómico:  
<img width="438" height="456" alt="image" src="https://github.com/user-attachments/assets/0743a542-511f-474f-8aa3-1836215ddf60" />

### [Circuito simple](https://youtube.com/shorts/LcykYA4Ir8Q?feature=share)    
### [Nurburging](https://youtube.com/shorts/jDJJP8_daNA)
### [Montreal](https://youtu.be/ogd5Wwj7WUw)
### [Montmelo](https://youtube.com/shorts/aIZiAnfneRo)




