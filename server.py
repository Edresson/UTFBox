# -*- coding: utf-8 -*-
from socket import *
import os.path

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import os

from utils import *

udpserver = ''
clientes =[]
DIRECTORY_TO_WATCH = "/home/edresson/UTFPR/7-periodo/sistemas-distribuidos/Trabalho-UTFBox/UTFBox/Servidor/"

#port number > 5000
serverPort = 80
PORTUDP = 5000

ignoreclient = False


class Watcher:
    
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(0)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global udpserver,clientes,ignoreclient
        print(ignoreclient)
        if ignoreclient == False:
            if event.is_directory:
                return None

            

            elif event.event_type == 'created':
                # Take any action here when a file is first created.
                for i in clientes:
                    '''print(i,ignoreclient)
                    if i[0] == ignoreclient[0] :
                        continue'''
                    udpserver.sendto('create:'+event.src_path.encode('utf-8'),i)
                print("Received created event - %s." % event.src_path)

            elif event.event_type == 'modified':
                #EnviarArquivo(event.src_path)
                # Taken any action here when a file is modified.
                for i in clientes:
                    '''print(i,ignoreclient)
                    if i[0] == ignoreclient[0] :
                        continue'''
                    udpserver.sendto('update:'+event.src_path.encode('utf-8'),i)
                print("Received modified event - %s." % event.src_path)
            elif event.event_type == 'deleted':
                for i in clientes:
                    '''if i == ignoreclient :
                        continue'''
                    udpserver.sendto('delete:'+event.src_path.encode('utf-8'),i)
                #RemoverArquivo('rm -rf '+event.src_path)
                # Taken any action here when a file is modified.
                print("Received deleted event - %s." % event.src_path)

@threaded
def startwatcher():
    w = Watcher()
    w.run()
@threaded
def udpthread():
    global udpserver,clientes
    udpserver = socket(AF_INET, SOCK_DGRAM)
    orig = ('', PORTUDP)
    udpserver.bind(orig)
    while True:
        print("aguardando")
        _, cliente = udpserver.recvfrom(1024)
        clientes.append(cliente)
        print('clientes',clientes)

@threaded       
def conectado(connectionSocket, clientAddress):
        global ignoreclient
        comando= connectionSocket.recv(1024)
        comando = comando.replace('\r\n\r\n','')
        if comando[:7] == 'upload:':
            
            print('addres',clientAddress)
            
            ignoreclient = True
            time.sleep(2)
            print('Fazendo Upload')
            filename = comando.replace('upload:','')
            filename = filename.decode('utf-8')
            connectionSocket.sendto('ok'.encode('utf-8'),clientAddress)
            file = open(DIRECTORY_TO_WATCH+filename, "w+")
            #get the first line of the file
            clientInput = connectionSocket.recv(1024).decode('utf-8')
            bytesReceived = 0

            #for each line the client sends, add it to the transf
            while clientInput != "\r\n\r\n" and clientInput != "":
                bytesReceived += len(clientInput)
                file.write(clientInput)
                clientInput = connectionSocket.recv(1024).decode('utf-8')
            

            if(clientInput == "" or clientInput == "\r\n\r\n"):
            #needs to have the double \\ to cancel out interpreting it as a string
                
                connectionSocket.sendto(str(bytesReceived).encode('utf-8'),clientAddress)
                file.close()
                connectionSocket.close()
            time.sleep(1)
            ignoreclient = False
            print('Upload Concluido')

        elif comando[:8] =='remover:':
            comando = comando.replace('remover:','')
            print('remover: '+comando)
            #os.system('rm -rf '+DIRECTORY_TO_WATCH+comando)
        
        elif comando[:9] =='download:':
            arquivo = comando.replace('download:','')
            #Bytes in Test File
            numBytesFile = determine_num_bytes(arquivo)

            #Opening the test file
            testFileObj = open_text_file(os.path.abspath(arquivo))


            #Read the text file to the socket
            read_text_file(connectionSocket, testFileObj, numBytesFile)

            #serverResponse = sock.recv(1024)
            #print "Server received <" + str(serverResponse) + "> bytes."
            #Closing the test file
            testFileObj.close()


            






if __name__ == '__main__':
    
    #creating socket with IPV4 and TCP params, and binding it to serverPort
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(4)
    print( "Starting service listening on <" + str(serverPort) + ">")
    startwatcher()
    udpthread()
    #when a connection request is recieved, a new socket is created
    while 1:
        connectionSocket, clientAddress = serverSocket.accept()
        conectado(connectionSocket, clientAddress)
        
