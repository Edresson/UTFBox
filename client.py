# -*- coding: utf-8 -*-
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import os
from socket import *

from utils import *

DIRECTORY_TO_WATCH = "/home/edresson/UTFPR/7-periodo/sistemas-distribuidos/Trabalho-UTFBox/UTFBox/Cliente/"
SERVER= '127.0.0.1'
PORT= 80
PORTUDP = 5000
baixar = []

blockwatchdog = False

#Make a TCP socket connection to server at <IP> and <PORT>
#Example code followed from: https://pymotw.com/2/socket/tcp.html
def connect_to_server_tcp(ip, port):
    #Creating a TCP socket
    sock = socket(AF_INET, SOCK_STREAM)
    #Connect the socket to the port where the server is listening
    server_address = (ip, port)
    print ("Successfully opened socket to server at" + str(server_address))
    sock.connect((ip, port))

    return sock





@threaded
def EnviarArquivo(arquivo):
    
    
    #Bytes in Test File
    numBytesFile = determine_num_bytes(os.path.abspath(arquivo))

    #Opening the test file
    testFileObj = open_text_file(os.path.abspath(arquivo))

    #Connecting to the server
    sock = connect_to_server_tcp(SERVER, PORT)
    arquivopath = arquivo.replace(DIRECTORY_TO_WATCH,'')#usado para poder upar pastas    
    #Read the text file to the socket
    read_text_file(sock, testFileObj, numBytesFile,arquivopath)

    #serverResponse = sock.recv(1024)
    #print "Server received <" + str(serverResponse) + "> bytes."
    #Closing the test file
    testFileObj.close()

    #Close the socket
    sock.close()


@threaded
def RemoverArquivo(arquivo):
    #Connecting to the server
    sock = connect_to_server_tcp(SERVER, PORT)
    sock.send(arquivo.encode('utf-8') )#envia o nome do arquivo
    


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
        global blockwatchdog 
        print('Flag: ',blockwatchdog )
        if blockwatchdog: # ignore modified
            pass

        else:
            if event.is_directory:
                return None

            elif event.event_type == 'created':
                EnviarArquivo(event.src_path)
                # Take any action here when a file is first created.
                print("Received created event - %s." % event.src_path)

            elif event.event_type == 'modified':
                EnviarArquivo(event.src_path)
                # Taken any action here when a file is modified.
                print("Received modified event - %s." % event.src_path)
            elif event.event_type == 'deleted':
                arquivo = event.src_path.replace(DIRECTORY_TO_WATCH,'')
                RemoverArquivo('remover:'+arquivo)
                # Taken any action here when a file is modified.
                print("Received deleted event - %s." % event.src_path)

@threaded
def SolicitarDownload(filename):
    global blockwatchdog
    blockwatchdog = True
    time.sleep(2)
    print('Fazendo Download')
    connectionSocket = connect_to_server_tcp(SERVER, PORT)
    mensagem = 'download:'+filename
    connectionSocket.sendall( mensagem.encode('utf-8') )
    _= connectionSocket.recv(1024)
    connectionSocket.sendall('ok'.encode('utf-8') )
    filename= os.path.join(DIRECTORY_TO_WATCH,filename)
    print('Filename: ', filename)
    if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    pass
    file = open(filename, "w+")
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
        connectionSocket.sendall(str(bytesReceived).encode('utf-8'))
        file.close()
        connectionSocket.close()
    time.sleep(1)
    blockwatchdog = False
    print('Download Acabou') 
    


@threaded
def startwatcher():
    w = Watcher()
    w.run()

def udpthread():
    global baixar
    udp = socket(AF_INET, SOCK_DGRAM)
    destino = (SERVER,PORTUDP)
    udp.sendto('update'.encode('utf-8'),destino)
    print('enviado')   
    while True:
        msg, cliente = udp.recvfrom(1024)
        msg = msg.decode('utf-8').replace('\r\n\r\n','')
        if msg[:7] =='create:' :
            print("Create", msg)
            SolicitarDownload(msg.replace('create:',''))

        elif msg[:7] == 'update:':
            print("UPDATE: ",msg.replace('update:',''))
            SolicitarDownload(msg.replace('update:',''))
        elif msg[:7] == 'delete:':
            try:
                print("REMOVE", os.path.join(DIRECTORY_TO_WATCH,msg.replace('delete:','')))
                os.remove(os.path.join(DIRECTORY_TO_WATCH,msg.replace('delete:','')))
            except:
                pass
        

if __name__ == '__main__':
    startwatcher()
    udpthread()