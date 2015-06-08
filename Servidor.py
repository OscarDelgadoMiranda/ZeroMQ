#!usr/bin/env python


import zmq
import time
import commands

#Se obtiene la IP privada del ordenador
status, ip = commands.getstatusoutput("hostname -I | cut -d' ' -f1")
print "Ip usada para servidor: ", ip
ip_server = ip

#ip_server = raw_input("IP actual del servidor(introduzca la ip + intro): ")

#El servidor funciona como una sala de espera a la que se conectan los clientes
#que quieran entablar un juego
def Esperar_jugadores():
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	#Asignamos un puerto a la espera de las IPs de clientes
	socket.bind("tcp://"+ip_server+":5000")
	print "Esperando jugadores en el puerto 5000"
	pub = context.socket(zmq.PUB)
	#Asignamos un puerto para enviar las IPs de los jugadores que vallan a jugar
	pub.bind("tcp://"+ip_server+":6000")
	print "Se enviaran las partidas por el puerto 6000"
	#lista de jugadores en espera
	jugadores=[]

	while True: #bucle de prueba al finalizar este bucle seria infinito
		#recibimos las IPs de los jugadores y los colocamos en la lista mediante REP/REQ
		mensaje = socket.recv()
		#La lista actua como una cola FIFO:
		jugadores.append(mensaje)
		#En caso de que halla esperando mas de un jugador se puede empezar una partida
		if len(jugadores) > 1:
			estado = "Emparejando..."
			socket.send(estado)
			time.sleep(2)
			#Se construye el mensaje con la ip_serverr que sera a lo que estan suscritos los
			#clientes y los jugadores que pueden empezar a jugar
			contrincante = ip_server+" "+jugadores[0]+" "+jugadores[1]
			print "Emparejando", contrincante
			#Eliminamos a los jugadores de la cola de espera
			del jugadores[0]
			del jugadores[0]
			#Enviamos el mensaje por el puerto 5000 mediante PUB/SUB
			pub.send(contrincante)
		else:
			estado = "Esperando a mas jugadores...."
			socket.send(estado)



Esperar_jugadores()