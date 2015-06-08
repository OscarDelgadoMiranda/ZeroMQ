#!usr/bin/env python

import zmq
import time
import sys


#Para probar  en un mismo PC de manera local se solicita todas las IPs
ip_server = raw_input("IP actual del servidor(introduzca la ip + intro): ")
ip_client = raw_input("IP actual de su EQUIPO(introduzca la ip + intro): ")

#numero de rondas en la partida
Ronda = 0

def Conectar_server():
	context = zmq.Context()
	#Se establece una conexion para enviar las IPs con REP/REQ
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://"+ip_server+":5000")
	#Se establece otra conexion para recibir las partidas por PUB/SUB
	sub = context.socket(zmq.SUB)
	sub.connect("tcp://"+ip_server+":6000")
	#En la conexion PUB/SUB nos suscribimos a la IP del servidor para recibir sus mensajes
	sub.setsockopt(zmq.SUBSCRIBE, ip_server)
	#enviamos la ip del cliente
	socket.send(ip_client)
	mensaje = socket.recv()
	print mensaje
	Salir = True
	#Escuchamos en el puerto hasta que podamos empezar una partida
	while Salir == True:
		time.sleep(1)
		mensaje = sub.recv()
		#dividimos el mensajes en las tres IPs de las que esta compuesto
		if len(mensaje.split()) == 3:
			IP = mensaje.split()
			#Comprobamos si nuestra IP esta en el mensaje
			if ip_client in IP:
				#Si es asi, miramos la IP que tendra nuestro contrincante
				if ip_client == IP[1]:
					#La variable servidor ayudara a elegir quien de los jugadores actuara
					#como servidor
					servidor = True
					contrincante = IP[2]
				else:
					contrincante = IP[1]
					servidor = False
				print "\nConectando con ", contrincante
				Salir = False
	#Cerramos las conexiones con el servidor
	socket.close()
	sub.close()
	#DDependiento de si hemos sido elegido servidor o no empezamos una nueva conexion
	#con el adversario y empezamos el juego
	if servidor == True:
		Jugar_server()
	else:
		Jugar_cliente(contrincante)



#Se realiza la conexion haciendo al jugador servidor de la partida
def Jugar_server():
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	#Nueva conexion en el puerto 7000, la partida se hara por turnos mediante REP/REQ
	socket.bind("tcp://"+ip_client+":7000")

	#Iniciamos la matriz/tablero de juego
	matriz = []
	for i in range(3):
		matriz.append([])
		for j in range(3):
			matriz[i].append(" ")

	#Al server le correspondera ser el jugador X
	jugador = "X"
	Salir = True
	InicioPartida = False
	rival = "O"
	opciones = ["yes","y","s", "si", "Y", "Yes", "YES"] #Opciones validas para volver a conectarse al servidor
	#Funcion para dibujar la matriz
	Dibujar(matriz)
	print "\nEsperando movimiento rival..."
	#La conexion se llevara acabo mientras ninguno de los jugadores gane o empate
	while Salir == True:
		time.sleep(1)
		#se recibe las coordenadas del otro jugador
		mensaje = socket.recv()
		#El mensaje tiene tres campos separados por espacos, las coordenadas y el numero de ronda
		coor = mensaje.split()
		x = int(coor[0])
		y = int(coor[1])
		Ronda = int(coor[2])	
		sys.stdin.flush()

		#Se llama a la funcion juego para jugar
		estado, coor[0],coor[1],coor[2] = juego(matriz, jugador, Ronda, x, y, InicioPartida, rival)
		#Si estado es false significa que se ha acabado la partida
		Salir = estado
		#construimos el mensaje con las coordendas de este jugador y la ronda
		mensaje = str(coor[0])+" "+str(coor[1])+" "+str(coor[2]) 
		Ronda = coor[2]
		socket.send(mensaje)

	#Despues de acabar se da la opcion para conectarse al servidor en busca de otro jugador
	op = raw_input("\nDesea volver a jugar??(yes,no): ")
	if op in opciones:
		Conectar_server()
	else:
		print "\nEspero que te lo pasaras bien, hasta pronto."
		socket.close()
		
		



def Jugar_cliente(ip_cont):
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	#Nueva conexion en el puerto 7000, la partida se hara por turnos mediante REP/REQ
	socket.connect("tcp://"+ip_cont+":7000")

	#Iniciamos la matriz
	matriz = []
	for i in range(3):
		matriz.append([])
		for j in range(3):
			matriz[i].append(" ")

	#Al server le correspondera ser el jugador O
	jugador = "O"
	
	Salir = True
	InicioPartida = True
	rival = "X"
	opciones = ["yes","y","s", "si", "Y", "Yes", "YES"]
	#El cliente empieza el juego en primer lugar
	#Es necesario pasar unas coordendas aunque estas no se tendran encuenta
	coor = [0,0,0]
	#llamamos a la funcoin para jugar
	estado, coor[0],coor[1], coor[2] = juego(matriz, jugador, 0, 0, 0, InicioPartida, rival)
	#Se construye el mensaje y se envia al servidor
	mensaje = str(coor[0])+" "+str(coor[1])+" "+str(coor[2]) 
	socket.send(mensaje)
	#Variable encargada de decir quien juega el primero, pasado el primer turno del primer jugador
	#Se vueleve a poner a False para realizar correctamente la alternancia de los turnos
	InicioPartida = False
	#La conexion se llevara acabo mientras ninguno de los jugadores gane o empate
	while Salir == True:	
		time.sleep(1)
		#Se realiza la recepcion de las coordenadas del adversario
		mensaje = socket.recv()
		#Se divide el mensaje para su recpecion
		coor = mensaje.split()
		x = int(coor[0])
		y = int(coor[1])
		Ronda = int(coor[2])
		sys.stdin.flush()
		#Llamamos a jugar
		estado, coor[0],coor[1],coor[2] = juego(matriz, jugador, Ronda, x, y, InicioPartida, rival)
		#Como en el server se asignan los valores que devuleve la funcion para saber si se ha acabado
		#el juego y las nuevas coordenadas
		Salir = estado
		#Se construye el mensaje y se envia
		mensaje = str(coor[0])+" "+str(coor[1])+" "+str(coor[2]) 
		Ronda = coor[2]
		socket.send(mensaje)

	#Despues de acabar se da la opcion para conectarse al servidor en busca de otro jugador	
	op = raw_input("\nDesea volver a jugar??(yes,no): ")
	if op in opciones:
		print "\nConectando con el servidor"
		Conectar_server()
	else:
		print "\nEspero que te lo pasaras bien, hasta pronto."
		socket.close()



#Funcion para jugar al tres en raya, se encarga de saber si se ha perdido o ganado y si se termina
#la conexion
def juego(matriz, jugador, Ronda, x, y, InicioPartida, rival):
	Ronda += 1
	if Ronda >= 10:
		if matriz[x][y] !=jugador:
			matriz[x][y] = rival

		Dibujar(matriz)
		if Ganar(matriz,rival)==True:
			print "\nHAS PERDIDO"
		else:
			print "\nEMPATE"
		estado = False
		#Fin de la ejecucion aqui
	else:
		if InicioPartida==False: #El primer jugador que empieza a jugar, no tiene que esperar las coordenadas del otro
								  #Tendria derrota==False directamente
			#Recibo las 2 coordenadas (informacion que viene del otro cliente)
			matriz[x][y]=rival 
			Dibujar(matriz)
			derrota=Ganar(matriz,rival) #Funcion para ver si el jugador (el enemigo) ha ganado
		else:
			Dibujar(matriz)
			derrota=False
		
		if derrota==True: #Mensaje y fin del juego
			print "\nHAS PERDIDO"
			estado = False #En caso de que estado sea false se finaliza la conexion
		else: #Me toca jugar, porque el rival no ha ganado
			while True: 
				print "\nIntroduzca la coordenada X de donde deseas colocar tu ficha"
				x = input()
				print "Introduzca la coordenada Y de donde deseas colocar tu ficha"
				y = input()
				
				#Adaptamos lo visual para el jugador a la codificacion de las posicion de las matrices restando 1 a las posiciones
				x = x - 1 
				y = y - 1
				 
				if x>=0 and x<3 and y>=0 and y<3 and matriz[x][y]==" ":
					break
				else:
					print "\nCoordenadas no validas, introduzcalas de nuevo: "
					continue
			
			matriz[x][y]=jugador #inserto en esa posicion de la matriz 
			Dibujar(matriz)
			victoria=Ganar(matriz,jugador) #Lo mismo que arriba con derrota, compruebo si he ganado despues de poner de nuevo
			
			if victoria==True:
				print "\nHAS GANADO"
				estado = False
				#Enviar las coordenadas x e y
				#Fin de la ejecucion (no se como se hace esto o si depende de tu codigo)
			else:
				print "\nEsperando movimiento rival..."
				estado = True
				#Enviar las coordenadas x e y
				#Quedarse en espera
	return estado, x, y, Ronda



#Comprueba si un jugador ha ganado la partida
def Ganar(matriz,jugador):
	#Compruebo que el jugador recibido ha ganado de las 8 maneras posibles, 3 horizontales, 3 verticales y las 2 diagonales
	if ((matriz[0][0]==jugador and matriz[0][1]==jugador and matriz[0][2]==jugador) or
		(matriz[1][0]==jugador and matriz[1][1]==jugador and matriz[1][2]==jugador) or
		(matriz[2][0]==jugador and matriz[2][1]==jugador and matriz[2][2]==jugador) or
		(matriz[0][0]==jugador and matriz[1][0]==jugador and matriz[2][0]==jugador) or
		(matriz[0][1]==jugador and matriz[1][1]==jugador and matriz[2][1]==jugador) or
		(matriz[0][2]==jugador and matriz[1][2]==jugador and matriz[2][2]==jugador) or
		(matriz[0][0]==jugador and matriz[1][1]==jugador and matriz[2][2]==jugador) or
		(matriz[0][2]==jugador and matriz[1][1]==jugador and matriz[2][0]==jugador)):
		return True #Ha ganado
	else:
		return False #No ha ganado



#Dibuja la matriz/tablero
def Dibujar(matriz):
	print "\n     1    2    3"
	print "  ||=============||"
	for i in range(3):
		print (i+1),"||",matriz[i][0],"||",matriz[i][1],"||",matriz[i][2],"||"
		print "  ||=============||"
		

Conectar_server()