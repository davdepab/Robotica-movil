# PRÁCTICA 1 - ROBOT ASPIRADOR

El objetivo de esta práctica es cubrir el área mas grande posible a limpiar por un robot aspirador autónomo, para ello implementaré diversas formas de algoritmos de
cobertura online que implican datos del entorno y control del mismo en tiempo real. En primer lugar utilizaremos un movimiento básico reactivo, el robot irá de frente hasta que detecte un objeto/pared en un rango de "visión" determinado, tras el "impacto" retrocederá ligeramente,  girará a una velocidad constante durante un tiempo aleatorio (entre 2 y 3 segundos, para conseguir "aleatoriedad") y luego continuará avanzando de frente.

## Breve explicación del código:  
En primer lugar obtenemos los datos del sensor de distancia laser mediante la capa de abstracción de hardware(HAL) y establecemos un flag que indicará si existe un
obstáculo/pared, luego comprobaremos los datos del sensor en un rango de 50º-130º para únicamente tener en cuenta obstáculos que estén directamente enfrente, por otro lado establecemos la distancia de "impacto" a 0.2 metros, si este límite se rebasa consideraremos que tenemos un obstáculo delante y activaremos el flag.

Cuando detectamos un objeto se ejecutará la secuencia de pasos explicados al principio: retroceso breve, giro aleatorio y continuación.
