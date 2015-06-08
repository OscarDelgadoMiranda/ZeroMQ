# ZeroMQ
Trabajo de ZeroMQ del grupo 3 de SD

Componentes del grupo:

**Óscar Delgado Miranda**    
**Miguel Ángel Pérez García**  
**Ildefonso de la Cruz Romero**  
**David Blanco Fuentes**  
  
---
***Introducción***

En el programa en conjunto, hemos hecho uso de Zmq para las
conexiones entre servidor y distintos clientes, junto con la
implementación del juego 3 en raya. Principalmente la finalidad
del trabajo ha sido trabajar sobre las distintas conexiones y para
probarlo hemos implementado el juego.

El servidor actuara como una sala de espera, al cual se
conectarán distintos clientes(jugadores) en busca de una
partida. Una vez que el servidor tiene a más de un jugador
esperando para jugar les pasa a estos sus IP para que
comiencen una nueva conexión entre ambos clientes, donde
uno actuará como server y otro como cliente.

---
***¿Cómo se ejecuta?***

Debemos de tener en cuenta si vamos usar el juego de manera
local para probar su funcionamiento o en una red para hacer
uso de este programa y jugar por diversión algunas partidas.

En caso de que se quiera hacer una prueba en un mismo PC
hay que tener en cuenta lo siguiente:

Primero ejecutamos el servidor (python Server.py), el cuál nos
imprimirá la IP y los puerto que está usando.

Segundo ejecutamos en un terminal diferente cada
cliente(python cliente.py), este nos pidirá la IP del servidor, que
ya nos había mostrado este, y la IP que usará este cliente para
jugar.

Es necesario que cada cliente tenga una IP distinta, uno de ellos
puede tener la IP que este usando el PC, la misma que usa el
servidor, y el otro cliente debe de usar la IP de
localhost(127.0.0.1)

Si solo se quiere jugar con otro jugador dentro de una
misma red, se decide un PC de dicha red para ejecutar el
servidor. Y en los clientes solo ponemos la IP del servidor y la
del equipo en el que estemos.

Y deberia iniciarse así:
![img](https://cloud.githubusercontent.com/assets/11409249/8037742/efd3811c-0dff-11e5-976f-da04051818c5.jpg)
---
