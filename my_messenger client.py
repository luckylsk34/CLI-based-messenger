import socket
from threading import Thread
from colorama import winterm
import sys

###########################################################################################################

#this part is for creating sockets and connecting to the server side

w = winterm.WinTerm()

sendclient = socket.socket()
recvclient = socket.socket()

host = '192.168.1.107' #+ input('host ip : 192.168.1.')
recvport = 9998
sendport = 9997

recvclient.connect((host, recvport))
print('recieving active')
sendclient.connect((host, sendport))
print('sending active')

###########################################################################################################

#this part has functions for sending and recieving messages

n = 0

def sending():
	global n
	while True:
		msg = input('you: ')
		n = 0
		sendclient.send(msg.encode('ascii'))

def recieving():
	global n
	while True:
		msg1 = recvclient.recv(1024)
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

#this starts the sending and recieving on two different threads

print(' ')
Thread(target = sending).start()
Thread(target = recieving).start()