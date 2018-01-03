"""threading is used since we need take input for sending
   and listen on the recieving socket for the message and
   these both need to be done simultaneously, hence
   threading"""


import socket
from threading import Thread
from colorama import winterm
import sys
from msvcrt import getche, getch

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

#connection to the client on recieving socket on 9997 port
recvsocket.listen(5)
recvclientsocket, addr = recvsocket.accept()
print('connected to', recvclientsocket.getsockname()[0], 'on', recvclientsocket.getsockname()[1])

###########################################################################################################

#this part has the required functions for chatting by reiceving and sending the required messages

n = 0
msg = ''

def sending():
    global n, msg
    print('you: ', end = '')
    while True:
        while True:
            cha = getch()
            if cha == chr(13).encode('ascii'):
                print('\nyou: ', end = '')
                break
            elif cha == chr(8).encode('ascii'):
                position = w.get_position(-11)
                w.cursor_adjust(-1, 0)
                print(' ', end = '')
                sys.stdout.flush()
                w.cursor_adjust(-1, 0)
                msg = msg[:-1]
            else:
                try:
                    print(cha.decode('ascii'), end = '')
                    sys.stdout.flush()
                    msg+= cha.decode('ascii')
                except:
                    pass
        if msg:
            n = 0
            msg+= ' '
            sendclientsocket.send(msg.encode('ascii'))
            msg = ''

def recieving():
    global n, msg
    while True:
        msg1 = recvclientsocket.recv(1024)
        pos = w.get_position(-11)
        if n == 0:
            n = 1
            w.cursor_adjust(1-pos.X, 0)
            print('                                                                                                    ', end = '\r')
            print('\nother:', msg1.decode('ascii'))
            if msg:
                print('\nyou: '+ msg, end = '')
            else:
                print('\nyou: ', end = '')
        else:
            w.cursor_adjust(1-pos.X, -1)
            count = 0
            print('other:', msg1.decode('ascii'))
            print('                                                                                                    ', end = '\r')
            if msg:
                print('\nyou: '+ msg, end = '')
            else:
                print('\nyou: ', end = '')
            sys.stdout.flush()
#this starts the sending and recievig on two different threads
print(' ')
Thread(target = sending).start()
Thread(target = recieving).start()
