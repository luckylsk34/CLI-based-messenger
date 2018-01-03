import socket
from threading import Thread
from colorama import winterm
import sys
from msvcrt import getche, getch

###########################################################################################################

#this part is for creating sockets and connecting to the server side

w = winterm.WinTerm()

sendclient = socket.socket()
recvclient = socket.socket()

host = input('host ip : ')
recvport = 9998
sendport = 9997

recvclient.connect((host, recvport))
sendclient.connect((host, sendport))
print('connected to', sendclient.getsockname()[0], 'on', sendclient.getsockname()[1])

###########################################################################################################

#this part has functions for sending and recieving messages

n = 0
msg = ''

def sending():
    global n, msg
    while True:
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
                sendclient.send(msg.encode('ascii'))
                msg = ''

def recieving():
    global n, msg
    while True:
        while True:
            msg1 = recvclient.recv(1024)
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

#this starts the sending and recieving on two different threads

print(' ')
Thread(target = sending).start()
Thread(target = recieving).start()
