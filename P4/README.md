# PRÁCTICA 4 - NAVEGACIÓN GLOBAL (WAVEFRONT)

<img width="647" height="336" alt="image" src="https://github.com/user-attachments/assets/c5f7029f-1054-4a07-be85-afc8b39103cd" />

El objetivo de esta práctica consiste en implementar un sistema de navegación global para un vehículo autónomo en un entorno urbano conocido. Mediante el algoritmo de propagación de onda (**Wavefront**) combinado con un subcampo de penalización por cercanía a obstáculos, el taxi autónomo calcula la trayectoria óptima y segura hacia cualquier destino marcado en el mapa y la ejecuta en tiempo real.

## DESARROLLO DE LA PRÁCTICA Y BREVE EXPLICACIÓN DEL CÓDIGO:

En primer lugar, cargo el mapa binario de la ciudad mediante **WebGUI.getMap()**, obteniendo una matriz 2D donde las celdas negras (`0`) representan edificios y las blancas carretera libre. Antes de entrar en el bucle principal, realizo un preprocesado único del mapa para generar una matriz de penalizaciones sin necesidad de engrosar artificialmente los obstáculos.

Dentro del bucle infinito regulado por **Frequency.tick()**, compruebo si el usuario ha seleccionado un nuevo destino con **WebGUI.getTargetPose()**. Cuando cambia la meta, transformo tanto las coordenadas del destino como la posición actual del vehículo a celdas de la matriz mediante **WebGUI.worldToGrid()**, ejecuto la propagación **wavefront()** y extraigo la trayectoria con **calcular_ruta()**.

<img width="962" height="285" alt="image" src="https://github.com/user-attachments/assets/fccc64ef-1b52-4d8f-bb1b-0db8cb3480b3" />

Finalmente, represento visualmente en tiempo real la expansión de la onda y el mapa de costes resultante normalizado en escala de grises mediante **WebGUI.showNumpy()**, junto con la trayectoria obtenida en **WebGUI.showPath()**, mientras la función **conduccion_ruta()** guía al vehículo en cada iteración.

## PLANIFICACIÓN Y CONTROL:

<img width="962" height="573" alt="image" src="https://github.com/user-attachments/assets/ed9b25bd-77fe-4ffe-b8ed-35a652df9f98" />

El sistema divide la navegación en tres fases diferenciadas: modelado del entorno con márgenes de seguridad, cálculo del camino mínimo y control continuo de velocidades.

### SUBCAMPO DE PENALIZACIÓN POR CERCANÍA A OBSTÁCULOS:
Para evitar que el taxi roce las esquinas debido a su anchura física sin bloquear las calles estrechas mediante engrosamiento, ejecuto una búsqueda en anchura (BFS) en 8 direcciones desde todos los píxeles de obstáculo hasta un radio de **4 celdas**:
- **Penalización cuadrática (`1` a `4` celdas):** Se asigna un coste según la fórmula `((5 - celda_actual) ** 2) * 0.8`, generando valores decrecientes (`12.8`, `7.2`, `3.2` y `0.8`). Esta progresión penaliza fuertemente las celdas pegadas a las fachadas y vértices para que la ruta se abra hacia el centro de la calzada, manteniendo un borde exterior suave (`0.8`) que permite atravesar calles estrechas.

### PROPAGACIÓN WAVEFRONT Y DESCENSO POR GRADIENTE:
La función **wavefront()** inicia una expansión desde la celda destino (coste `0`) en **8 direcciones**, asignando un coste de desplazamiento de `1.0` para movimientos ortogonales y `1.4` para diagonales, e impidiendo pasos en diagonal que atraviesen el vértice de un edificio adyacente. 

Para evitar mínimos locales, la propagación utiliza una cola de prioridad (**heapq**) que integra directamente el subcampo de penalización en el coste acumulado de cada celda (`coste_paso + mapa_obstaculos`). Además, incorpora un criterio de parada temprana (`distancia_corte`) que detiene la expansión `15` unidades de coste después de alcanzar la celda del coche, reduciendo el tiempo de cálculo sin perder margen de maniobra. Posteriormente, **calcular_ruta()** parte de la posición del taxi y desciende iterativamente eligiendo el vecino (en 8 direcciones y sin cortar esquinas) con menor coste hasta alcanzar la meta.

### SEGUIMIENTO DE RUTA Y CONTROL DE VELOCIDADES:
En cada iteración del bucle principal, **conduccion_ruta()** toma el primer punto pendiente de la lista (`ruta[0]`) y lo convierte a metros con **WebGUI.gridToWorld()**. A partir de la pose actual obtenida con **HAL.getPose3d()**, calcula el ángulo objetivo con **math.atan2()** y normaliza el error angular al intervalo $[-\pi, \pi]$ para evitar giros completos innecesarios. 

Se aplica un control proporcional en velocidad angular (`Kw * error_yaw`, con `Kw = 4`) y una **velocidad lineal variable** modulada por el coseno del error angular (`max(2.0, V * math.cos(error_yaw))`, con `V = 10`), permitiendo circular a máxima velocidad en rectas y reducir hasta `2.0` en giros cerrados para no salirse de la trazada. Cada waypoint se descarta mediante `ruta.pop(0)` al entrar en un margen de `1.2` metros hasta detener el vehículo al vaciarse la lista.

### DEMOSTRACIONES DEL FUNCIONAMIENTO:

Se muestran distintos recorridos por la ciudad (trayectos cortos, cruces y rutas de larga distancia rodeando múltiples manzanas), comprobando cómo el gradiente rodea las esquinas gracias al subcampo de penalización cuadrático y el taxi mantiene el centro del carril adaptando su velocidad hasta frenar en el destino:

### [Vídeo de demostración](https://youtu.be/nFW_UkFHBRM)
