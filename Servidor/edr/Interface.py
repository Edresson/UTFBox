from Gui import *
from PyQt5.QtWidgets import QFileDialog
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from socket import *

a
a
AF_APPLETALK
aaa
bb
awdawdawd
aw
d
aw
aw
adw

wd
DeprecationWarningdddddddddddddddddddddddddddddd
aa
awdawd
awdaawdakwd


import threading
import os
from utils import *
a
abspath
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
aaaa
aaaa
aa
AF_APPLETALK
a
awjdhawjduyawd
a

editei123
awdaw
import pickle
try:
        with open('Conf-file.list', 'rb') as fp:
            conf_file = pickle.load(fp)
except:
        conf_file = [] 
        with open('Conf-file.list', 'wb') as fp:
            pickle.dump(conf_file,fp)

def saveconf():
    global conf_file
    with open('Conf-file.list', 'wb') as fp:
            pickle.dump(conf_file,fp)
            
            awdawdawd
            awd
            aw
            d
            aw
            awd

            awd
            awdawd

            wadawd

Usuario = ''
DIRECTORY_TO_WATCH = ''
SERVER= '127.0.0.1'
PORT= 80
PORTUDP = 5000
baixar = []
nologout = True
blockwatchdog = False
compfile = ''
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
    
    print('Enviar arquivo: ', arquivo)
    
    global  DIRECTORY_TO_WATCH,Usuario
    #Bytes in Test File
    numBytesFile = determine_num_bytes(os.path.abspath(arquivo))

    #Opening the test file
    testFileObj = open_text_file(os.path.abspath(arquivo))

    #Connecting to the server
    sock = connect_to_server_tcp(SERVER, PORT)
    arquivopath=None
    arquivopath = arquivo.replace(DIRECTORY_TO_WATCH,'')#usado para poder upar pastas
    arquivopath=os.path.join(Usuario,arquivopath.replace(os.path.join('sobarragambiarra123-','').replace('sobarragambiarra123-',''),''))   
    #Read the text file to the socket
    read_text_file(sock, testFileObj, numBytesFile,arquivopath)

    #serverResponse = sock.recv(1024)
    #print "Server received <" + str(serverResponse) + "> bytes."
    #Closing the test file
    testFileObj.close()
    print('Acabou de enviar:', arquivo)
    #Close the socket
    sock.close()


@threaded
def RemoverArquivo(arquivo):
    #Connecting to the server
    global Usuario
    arquivo = os.path.join(Usuario,arquivo.replace(os.path.join('sobarragambiarra123-','').replace('sobarragambiarra123-',''),''))
    print('MAndou remover: ',arquivo)
    arquivo='remover:'+arquivo
    sock = connect_to_server_tcp(SERVER, PORT)
    sock.send(arquivo.encode('utf-8') )#envia o nome do arquivo
    

@threaded
def SolicitarDownload(filename):
    global blockwatchdog
    global  DIRECTORY_TO_WATCH,Usuario
    blockwatchdog = True
    time.sleep(2)
    print('Fazendo Download:',filename)
    connectionSocket = connect_to_server_tcp(SERVER, PORT)
    #print(filename)
    mensagem = 'download:'+Usuario+':'+filename
    connectionSocket.sendall( mensagem.encode('utf-8') )
    _= connectionSocket.recv(1024)
    connectionSocket.sendall('ok'.encode('utf-8') )
    filename=filename.replace( os.path.join(Usuario,''),'')
    filename= os.path.join(DIRECTORY_TO_WATCH,filename)
    #print('Filename: ', filename)
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
    print('Download Acabou: ', filename) 
    



@threaded
def udpthread():
    global baixar,DIRECTORY_TO_WATCH,Usuario,nologout,blockwatchdog
    udp = socket(AF_INET, SOCK_DGRAM)
    destino = (SERVER,PORTUDP)
    udp.sendto('update'.encode('utf-8'),destino)
    print('enviado')   
    while nologout:
        msg, cliente = udp.recvfrom(1024)
        msg = msg.decode('utf-8').replace('\r\n\r\n','')
        if msg[:7] =='create:' :
            #print("Create", msg)
            msg2 = msg.replace('create:','')
            if msg2[:len(Usuario)+1]== os.path.join(Usuario,''):
                print("Create", msg2)
                SolicitarDownload(msg2)
            
        elif msg[:7] == 'update:':
            #print("UPDATE: ",msg.replace('update:',''))
            msg2 = msg.replace('update:','')
            if msg2[:len(Usuario)+1]== os.path.join(Usuario,''):
                SolicitarDownload(msg2)
                print("UPDATE: ",msg2)
         
        elif msg[:7] == 'delete:':
            blockwatchdog = True
            try:
                
                #msg2 = msg.replace('delete:','')
                print('delete:', msg2,msg2[:len(Usuario)+1]== os.path.join(Usuario,''))
                if msg2[:len(Usuario)+1]== os.path.join(Usuario,''):
                    os.remove(os.path.join(DIRECTORY_TO_WATCH,msg2.replace(os.path.join(Usuario,''),'')))
                    print("REMOVE", os.path.join(DIRECTORY_TO_WATCH,msg2.replace(os.path.join(Usuario,''))))
            except:
                pass
            blockwatchdog = False
        


class Watcher:
    
    def __init__(self):
        self.observer = Observer()

    def run(self,directory):
        global nologout
        event_handler = Handler()
        self.observer.schedule(event_handler, directory, recursive=True)
        self.observer.start()
        try:
            while nologout:
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
                time.sleep(1) 
                # Take any action here when a file is first created.
                print("Received created event - %s." % event.src_path)

            elif event.event_type == 'modified':
                EnviarArquivo(event.src_path)
                time.sleep(1) 
                # Taken any action here when a file is modified.
                print("Received modified event - %s." % event.src_path)
            elif event.event_type == 'deleted':
                arquivo = event.src_path.replace(DIRECTORY_TO_WATCH,'')
                RemoverArquivo(arquivo)
                # Taken any action here when a file is modified.
                print("Received deleted event - %s." % event.src_path)
                
@threaded  
def startwatcher(directory):
    global DIRECTORY_TO_WATCH
    DIRECTORY_TO_WATCH = directory
    w = Watcher()
    w.run(directory)
    


def get_login_information(ui):
    return ui.Usuario.text(),ui.Senha.text()

def get_compartilhar_information(ui):
    return ui.usuarioacomp.text()


def get_register_information(ui):
    return ui.RUsuario.text(),ui.RSenha.text(),ui.confSenha.text()

def registrar_se():
    global ui
    ui.stackedWidget.setCurrentIndex(1)

def login():ui,Usuario,nologout,DIRECTORY_TO_WATCH
    nologout = True 
    sock = connect_to_server_VER, PORT)
   usuario,senha=get_l





































































































