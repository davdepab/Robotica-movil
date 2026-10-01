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
            if dato < 0.1:
                obstaculo = True
    
    if obstaculo:
        # CAMBIAR SLEEP POR CONTEO DE ITERACIONES (TICKS)
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
