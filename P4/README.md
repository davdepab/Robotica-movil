
# PRÁCTICA 4 - NAVEGACIÓN GLOBAL (WAVEFRONT)

<img width="647" height="336" alt="image" src="https://github.com/user-attachments/assets/c5f7029f-1054-4a07-be85-afc8b39103cd" />

El objetivo de esta práctica consiste en implementar un sistema de navegación global para un vehículo autónomo en un entorno urbano conocido. Mediante el algoritmo de propagación de onda (**Wavefront**) combinado con un subcampo de penalización por cercanía a obstáculos, el taxi autónomo calcula la trayectoria óptima y segura hacia cualquier destino marcado en el mapa y la ejecuta en tiempo real.

## DESARROLLO DE LA PRÁCTICA Y BREVE EXPLICACIÓN DEL CÓDIGO:

En primer lugar, cargo el mapa binario de la ciudad mediante **WebGUI.getMap()**, obteniendo una matriz 2D donde las celdas negras (`0`) representan edificios y las blancas carretera libre. Antes de entrar en el bucle principal, realizo un preprocesado único del mapa para engrosar los obstáculos y generar una matriz de penalizaciones.

Dentro del bucle infinito regulado por **Frequency.tick()**, compruebo si el usuario ha seleccionado un nuevo destino con **WebGUI.getTargetPose()**. Cuando cambia la meta, transformo las coordenadas del mundo (metros) a celdas de la matriz mediante **WebGUI.worldToGrid()**, ejecuto la propagación **wavefront()** y extraigo la trayectoria con **calcular_ruta()**.

<img width="962" height="285" alt="image" src="https://github.com/user-attachments/assets/fccc64ef-1b52-4d8f-bb1b-0db8cb3480b3" />

Finalmente, represento visualmente tanto el mapa de distancias normalizado en escala de grises mediante **WebGUI.showNumpy()** como la trayectoria resultante con **WebGUI.showPath()**, mientras la función **conduccion_ruta()** guía al vehículo en cada iteración.

## PLANIFICACIÓN Y CONTROL:

<img width="962" height="573" alt="image" src="https://github.com/user-attachments/assets/ed9b25bd-77fe-4ffe-b8ed-35a652df9f98" />

El sistema divide la navegación en tres fases diferenciadas: modelado del entorno con márgenes de seguridad, cálculo del camino mínimo y control continuo de velocidades.

### SUBCAMPO DE PENALIZACIÓN Y ENGROSAMIENTO DE OBSTÁCULOS:
Para evitar que el taxi roce las esquinas debido a su anchura física, ejecuto una búsqueda en anchura (BFS) desde todos los píxeles de obstáculo hasta una distancia de 6 celdas:
* **Engrosamiento (`1` a `3` celdas):** Se marcan como intransitables (`inf` en el mapa de costes y `0` en el mapa binario) para impedir que el planificador trace rutas pegadas a las fachadas.
* **Halo de repulsión (`4` a `6` celdas):** Se asignan penalizaciones decrecientes (`2.4`, `1.6` y `0.8`). Al mantener saltos de `0.8` (menores que el avance de `1` unidad por celda hacia la meta), el coche tiende a circular por el centro de la calzada sin quedar atrapado en mínimos locales en calles estrechas.

### PROPAGACIÓN WAVEFRONT Y DESCENSO POR GRADIENTE:
La función **wavefront()** inicia una expansión BFS en 4 direcciones desde la celda destino (coste `0`), incrementando en `+1` cada celda libre alcanzada. Al sumar esta matriz con el subcampo de penalización (`campo_total`), se obtiene un potencial combinado sin mínimos locales. Posteriormente, **calcular_ruta()** parte de la posición del taxi y desciende iterativamente eligiendo el vecino (en 8 direcciones) con menor coste hasta alcanzar la meta.

### SEGUIMIENTO DE RUTA Y CONTROL DE VELOCIDADES:
En cada iteración del bucle principal, **conduccion_ruta()** toma el primer punto pendiente de la lista (`ruta[0]`) y lo convierte a metros con **WebGUI.gridToWorld()**. A partir de la pose actual obtenida con **HAL.getPose3d()**, calcula el ángulo objetivo con **math.atan2()** y normaliza el error angular al intervalo $[-\pi, \pi]$ para evitar giros completos innecesarios. Se aplica una velocidad lineal constante (`V = 10`) y un giro proporcional (`Kw * error_yaw`, con `Kw = 4`), eliminando cada waypoint mediante `ruta.pop(0)` al entrar en un margen de `2.5` metros hasta detener el vehículo al vaciarse la lista.

### DEMOSTRACIONES DEL FUNCIONAMIENTO:

Se muestran distintos recorridos por la ciudad (trayectos cortos, cruces y rutas de larga distancia rodeando múltiples manzanas), comprobando cómo el gradiente rodea los edificios engrosados y el taxi mantiene el centro del carril hasta frenar en el destino:

### [Vídeo de demostración](https://youtu.be/nFW_UkFHBRM)
