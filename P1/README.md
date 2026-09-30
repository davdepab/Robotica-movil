# PRÁCTICA 1 - ROBOT ASPIRADOR

El objetivo de esta práctica es cubrir el área mas grande posible a limpiar por el robot aspirador autónomo, para ello implementaré diversas formas de algoritmos de
cobertura. Para ello emplearemos algoritmos de cobertura online que implican datos del entorno y control del mismo en tiempo real. En primer lugar utilizaremos un
movimiento básico reactivo, el robot irá de frente hasta que detecte un objeto/pared en un rango de "visión" determinado, tras el "impacto" retrocederá ligeramente, 
girará a una velocidad constante durante un tiempo aleatorio (entre 2 y 3 segundos, para conseguir "aleatoriedad") y luego continuará avanzando de frente.

El código elaborado para realizar esta taréa es el siguiente:
``` python
import WebGUI
import HAL
import Frequency
import time
import random

while True:

    laser_data = HAL.getLaserData()

    obstaculo = False

    if len(laser_data.values) > 0:  # Aseguramos que haya datos que leer
        print(laser_data)
        # Recorremos la lista únicamente en ese rango (que cubre la parte frontal del robot)
        for dato in laser_data.values[50:130]:  # Aumentado el rango de visión  
            if dato < 0.2:
                obstaculo = True
    
    if obstaculo:
        HAL.setV(0.0)
        time.sleep(0.1) # Parada breve para evitar cambios bruscos
        HAL.setV(-0.5)
        time.sleep(0.5) # Breve retroceso para evitar colisiones laterales
        HAL.setV(0.0)
        HAL.setW(1.0)   # Giro durante tiempo aleatorio a velocidad cte
        tiempo_giro = random.uniform(2, 3)
        time.sleep(tiempo_giro)
    else:
        HAL.setV(0.5)
        HAL.setW(0.0)
```
En primer lugar obtenemos los datos del sensor de distancia laser mediante la capa de abstracción de hardware(HAL) y establecemos un flag que indicará si existe un
obstáculo/pared, luego comprobaremos los datos del sensor en un rango de 50º-130º para únicamente tener en cuenta obstáculos que estén directamente enfrente, por otro lado establecemos la distancia de "impacto" a 0.2 metros, si este límite se rebasa consideraremos que tenemos un obstáculo delante y activaremos el flag.

Cuando detectamos un objeto se ejecutará la secuencia de pasos explicados al principio: retroceso breve, giro aleatorio y continuación.
