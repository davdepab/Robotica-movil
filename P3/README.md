# PRÁCTICA 3 - NAVEGACIÓN LOCAL VFF

<img width="640" height="410" alt="image" src="https://github.com/user-attachments/assets/99a84daf-5c51-4701-af03-1d7b60050ecd" />

El objetivo de esta práctica consiste en, mediante el algoritmo reactivo de Campos Potenciales Virtuales (VFF) iterando en un bucle infinito, conseguir que un vehículo autónomo logre recorrer una pista esquivando obstáculos dinámicamente en tiempo real, guiándose únicamente mediante una navegación global dada en forma de waypoints y las lecturas de un sensor LiDAR de 180 grados.

## DESARROLLO DE LA PRÁCTICA Y BREVE EXPLICACIÓN DEL CÓDIGO:

En primer lugar he tomado los datos del sensor láser mediante la abstracción **HAL.getLaserData()**, la cual me proporciona 180 distancias. Lo que he hecho ha sido parsearlas obteniendo tanto sus coordenadas polares (distancia y ángulo) como cartesianas (x e y) referenciadas al frente del robot. 
Por otro lado, con **WebGUI.getNextTarget()** y **HAL.getPose3d()** extraigo la ubicación global de la meta y del coche. Utilizando trigonometría, convierto la coordenada absoluta del objetivo a una coordenada relativa centrada en el eje del vehículo, lo cual facilita mucho el cálculo de los vectores.

<img width="423" height="395" alt="image" src="https://github.com/user-attachments/assets/7d45f82e-0fb0-4b4b-b9dd-db28276f899d" />


Mediante la suma vectorial de las componentes resultantes combino las fuerzas calculadas y utilizando **WebGUI.showForces()** las muestro en pantalla para visualizar los tres vectores (Atracción, Repulsión y Resultante) en tiempo real.

## ALGORITMO VFF (VIRTUAL FORCE FIELD):

<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/c4e60873-9499-4413-ac83-ff2b0dc16b0d" />  


He utilizado dos componentes vectoriales para calcular en cada iteración del bucle infinito tanto la trayectoria deseada como las acciones evasivas, calculando a partir de ellas tanto una velocidad lineal como una angular.

### 🟢 VECTOR ATRACTIVO (TARGET):
Esta fuerza empuja el vehículo hacia la meta a través de una serie de waypoints establecidos como navegación global. Se calcula utilizando la posición relativa del objetivo. Para evitar que la fuerza disminuya drásticamente al acercarse al punto (lo cual provocaría sobrepasos por inercia o desvíos bruscos frente a obstáculos), se normaliza el vector. De esta forma adquiere una magnitud constante de 1, a la cual posteriormente multiplicaremos por una **K_TAR** obtenida de forma experimental. Además, si el coche entra en el radio de tolerancia del waypoint, se establece como alcanzado utilizando **target.setReached(True)** para forzar el paso al siguiente punto.

### 🔴 VECTOR REPULSIVO (OBSTÁCULOS):
Esta fuerza aleja el vehículo de las paredes. Para calcularla, sumo los 180 rayos del láser. A cada rayo se le aplica la ley de la inversa del cuadrado para que los objetos cercanos generen un rechazo exponencial frente a los lejanos. Adicionalmente, he implementado un sistema de zonificación de pesos: los rayos frontales aplican el 100% de su repulsión, mientras que los laterales solo aplican un 30%. Esto permite que el robot circule paralelo a las paredes de los pasillos sin sufrir oscilaciones laterales. Al total se le multiplica por una constante **K_OBS** pequeña para calibrar la fuerza. Este vector no se normaliza, preservando así la física exponencial de los impactos cercanos.

### 🔵 VECTOR RESULTANTE Y VELOCIDADES:
La suma de las componentes del vector de atracción y repulsión conforma el vector resultante. Para la velocidad angular, extraigo el ángulo exacto de esta fuerza resultante mediante la función **math.atan2()**. Esto fuerza al coche a dar volantazos agresivos de evasión si hay un choque frontal inminente. Por otro lado, la velocidad lineal disminuye proporcionalmente al riesgo: el algoritmo registra la "distancia efectiva" más pequeña obtenida por el láser y frena el vehículo si se acerca demasiado a un muro frontal, manteniendo siempre una velocidad mínima constante para evitar que el coche se quede completamente detenido.

### DEMOSTRACIONES DEL FUNCIONAMIENTO:

En primer lugar muestro el comportamiento del robot al acercarse frontalmente a un obstáculo y desenvolverse en pasillos. Se observa cómo el vehículo adapta su velocidad y gira de forma reactiva sin quedarse atascado. Al inicio de cada iteración, se reinician todas las variables de cálculo para asegurar un comportamiento puramente reactivo:  


<img width="420" height="450" alt="giphy" src="https://github.com/user-attachments/assets/d86c7829-45c0-4e8d-93ea-fb2d8fe38639" />  


Cabe recalcar que todas las simulaciones realizadas han sido ejecutadas garantizando un comportamiento fluido sin oscilaciones bruscas, logrado gracias a la mitigación del peso de las lecturas laterales del LiDAR.

### [Vídeo de demostración]((https://youtube.com/shorts/gHH--5v6LXI))
