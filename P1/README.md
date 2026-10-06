# PRÁCTICA 1 - ROBOT ASPIRADOR

El objetivo de esta práctica es cubrir el área mas grande posible a limpiar por un robot aspirador autónomo, para ello implementaré diversas formas de algoritmos de
cobertura online que implican datos del entorno y control del mismo en tiempo real. En primer lugar utilizaremos un movimiento básico reactivo, el robot irá de frente hasta que detecte un objeto/pared en un rango de "visión" determinado, tras el "impacto" retrocederá ligeramente,  girará a una velocidad constante durante un tiempo aleatorio (entre 3 y 5 segundos, para conseguir "aleatoriedad") y luego continuará avanzando de frente.

## Breve explicación del código:  
En primer lugar obtenemos los datos del sensor de distancia laser mediante la capa de abstracción de hardware(HAL) y establecemos un flag que indicará si existe un
obstáculo/pared, luego comprobaremos los datos del sensor en un rango de 50º-130º para únicamente tener en cuenta obstáculos que estén directamente enfrente, por otro lado establecemos la distancia de "impacto" a 0.2 metros, si este límite se rebasa consideraremos que tenemos un obstáculo delante y activaremos el flag, el cual provocará un salto de estado (de AVANZAR a FRENAR), una vez el robot haya frenado, tras un breve periodo de tiempo comenzará a retroceder para posteriormente girar y continuar su camino. Al implementar la lógica mediante una FSM (autómata de estados finito) tenemos el control del robot en todo momento lo que nos permite poder reaccionar en cualquier momento a cualquier imprevisto a diferencia de si hubiesemos implementado el código utilizando sleeps.

## Simulación:
En la siguiente imagen podemos observar que este método obtiene bastante buenos resultados, obteniendo cerca de un 80% en un tiempo aproximado de 20 minutos, teniendo en cuenta la simplicidad del comportamiento choca-gira:  


<img width="1312" height="581" alt="image" src="https://github.com/user-attachments/assets/91a3d173-dd1b-4612-a89a-aa69872ab415" />  


## [Vídeo de demostración](https://youtu.be/6Sh3VZ2ctaU)  

Como podemos ver en el vídeo, en una ejecución distinta a la de la captura anterior, de unos 15 minutos, el robot cubre alrededor de un 60% de la casa, lo que cuadra con el resultado del 80% en aproximadamente 20 minutos. 


## Movimiento en espiral:  

Al sustituir el estado de choca-gira por choca-espiral observo un mejor rendimiento en espacios abiertos ya que cubre el área más uniformemente, sin embargo, al adentrarse el robot en espacios cerrados se complica el que salga de ahí ya que con este estado los movimientos son circulares a diferencia del choca.gira que una vez gira vuelve a ir recto. Por lo tanto, he llegado a la conclusión de que lo ideal sería combinar el movimiento lineal con la espiral de forma aleatoria para que así haya alternativas en cada caso.  

<img width="1324" height="860" alt="image" src="https://github.com/user-attachments/assets/8e5b90ae-0dcc-4239-8e14-f42bdfe42f4b" />  


## [Vídeo de demostración](https://youtu.be/ogJFFNhsy9A)    


## Movimiento en espiral y lineal combinados:  

Tras la conclusión del apartado "Movimiento en espiral" implementando el código que combina aleatoriamente movimiento lineal y en espiral he consegudio resultados mejores que el del comportamiento básico choca-gira, cubre una parte similar de la casa pero de forma más uniforme, sin dejar calvas por así decirlo.  

<img width="1329" height="853" alt="image" src="https://github.com/user-attachments/assets/b1c9fef0-e30b-4778-8b60-9814f5b63b96" />  


## [Vídeo de demostración](https://youtu.be/aFhWxrW4_5E)  

