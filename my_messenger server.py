"""threading is used since we need take input for sending
   and listen on the recieving socket for the message and
   these both need to be done simultaneously, hence 
   threading"""


import socket
from threading import Thread
from colorama import winterm
import sys

###########################################################################################################

#this part is for creating the recieving and sending sockets and connecting them to the client's side

w = winterm.WinTerm()

sendsocket = socket.socket()
recvsocket = socket.socket()

host = socket.gethostname()
sendport = 9998    #sending port
recvport = 9997    #recieving port

sendsocket.bind((host, sendport))    #socket for sending information
recvsocket.bind((host, recvport))    #socket for recieving information

#connection to the client on sending socket on 9998 port
sendsocket.listen(5)
sendclientsocket, addr = sendsocket.accept()
print('sending active')

#connection to the client on recieving socket on 9997 port
recvsocket.listen(5)
recvclientsocket, addr = recvsocket.accept()
print('recieving active')

###########################################################################################################

#this part has the required functions for chatting by reiceving and sending the required messages

n = 0

def sending():
	global n
	while True:
		msg = input('you: ')
		n = 0
		sendclientsocket.send(msg.encode('ascii'))

def recieving():
	global n
	while True:
		msg1 = recvclientsocket.recv(1024)
		pos = w.get_position(-11)
		if n == 0:
			n = 1
			w.cursor_adjust(1-pos.X, 0)
			print('                                                                                                    ')
			print('other:', msg1.decode('ascii'))
			print('\nyou: ', end = '')
		else:
			w.cursor_adjust(1-pos.X, -1)
			print('other:', msg1.decode('ascii'))
			print('                                                                                                    ')
			print('you: ', end = '')
			sys.stdout.flush()
#this starts the sending and recievig on two different threads
print(' ')
Thread(target = sending).start()
Thread(target = recieving).start()