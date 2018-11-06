from Gui import *
from PyQt5.QtWidgets import QFileDialog
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from socket import *

import threading
import os
from utils import *

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
            
Usuario = ''
DIRECTORY_TO_WATCH = ''
SERVER= '127.0.0.1'
PORT= 80
PORTUDP = 5000
baixar = []
nologout = True
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
    arquivopath=os.path.join(Usuario,arquivopath.replace('/',''))   
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
    filename=filename.replace(Usuario+'/','')
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
    global baixar,DIRECTORY_TO_WATCH,Usuario,nologout
    udp = socket(AF_INET, SOCK_DGRAM)
    destino = (SERVER,PORTUDP)
    udp.sendto('update'.encode('utf-8'),destino)
    print('enviado')   
    while nologout:
        msg, cliente = udp.recvfrom(1024)
        msg = msg.decode('utf-8').replace('\r\n\r\n','')
        if msg[:7] =='create:' :
            print("Create", msg)
            msg2 = msg.replace('create:','')
            if msg2[:len(Usuario)+1]== Usuario+'/':
                print("Create", msg2)
                SolicitarDownload(msg2)
            
        elif msg[:7] == 'update:':
            print("UPDATE: ",msg.replace('update:',''))
            msg2 = msg.replace('update:','')
            if msg2[:len(Usuario)+1]== Usuario+'/':
                SolicitarDownload(msg2)
                print("UPDATE: ",msg2)
         
        elif msg[:7] == 'delete:':
            try:
                
                msg2 = msg.replace('delete:','')
                if msg2[:len(Usuario)+1]== Usuario+'/':
                    os.remove(os.path.join(DIRECTORY_TO_WATCH,msg2))
                    print("REMOVE", os.path.join(DIRECTORY_TO_WATCH,msg2))
            except:
                pass
        


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
                RemoverArquivo('remover:'+arquivo)
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

def get_register_information(ui):
    return ui.RUsuario.text(),ui.RSenha.text(),ui.confSenha.text()

def registrar_se():
    global ui
    ui.stackedWidget.setCurrentIndex(1)

def login():
    global ui,Usuario,nologout,DIRECTORY_TO_WATCH
    nologout = True 
    sock = connect_to_server_tcp(SERVER, PORT)
    usuario,senha=get_login_information(ui)
    msg = 'login:'+usuario+':'+senha
    sock.send(msg.encode('utf-8') )
    comando= sock.recv(1024).decode('utf-8')
    comando = comando.replace('\r\n\r\n','')
    if comando == 'ok':
        Usuario = usuario
        udpthread()
        print('tudo certo')
        for i in conf_file:
            if i.split(':')[0] == usuario:
                startwatcher(i.split(':')[1])
        ui.stackedWidget.setCurrentIndex(2)
        sock2 = connect_to_server_tcp(SERVER, PORT)
        msg = 'checkupdate:'+Usuario
        sock2.send(msg.encode('utf-8') )
        comando= sock2.recv(1024)
        arquivos =  pickle.loads(comando)
        listanome = [] 
        path = DIRECTORY_TO_WATCH
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        for n,t in arquivos:
            listanome.append(n)
            if n in onlyfiles:
                indice= onlyfiles.index(n)
                tempo = os.path.getmtime(os.path.join(path,onlyfiles[indice]))
                if tempo == t:
                    continue
                elif tempo > t:
                    EnviarArquivo(os.path.join(path, n))
                    time.sleep(1) 
                    print('atualizar mandar para o servidor ',n) 
                    #upload
                elif tempo < t:
                    SolicitarDownload(os.path.join(Usuario, n))
                    time.sleep(1) 
                    print('atualizar, baixar do servidor',n)
                    #Download
        
        downloads= set(listanome) -set(onlyfiles)
        uploads = set(onlyfiles) - set(listanome)

        for i in uploads:
            print( "upa ",i)
            EnviarArquivo(os.path.join(path, i))
            time.sleep(1) 
            #upa
            pass
        for i in downloads:
            print( 'baixar: ',i)
            SolicitarDownload(os.path.join(Usuario, i))
            time.sleep(1) 
            
            # baixa 
            pass
                
        
        
    else:
        print('login incorreto: ',comando)
    

def logout():
    global nologout
    nologout = False
    ui.stackedWidget.setCurrentIndex(0)

def change_dir():
    global Usuario,DIRECTORY_TO_WATCH,ui
    logout()
    diretorio= str(QFileDialog.getExistingDirectory(None,"Selecione o Diretorio que você deseja compartilhar")) # seleceção do diretorio
    pos=conf_file.index(Usuario+':'+DIRECTORY_TO_WATCH)
    conf_file[pos]= Usuario+':'+diretorio
    saveconf()
    ui.stackedWidget.setCurrentIndex(0)



def registrar():
    global ui
    usuario,senha,confsenha=get_register_information(ui)
    print(usuario,senha,confsenha)
    if confsenha != senha:
        print("as senhas não estão iguais")
    if usuario == '' or senha =='' or confsenha == '':
        print("Preencha todos os campos")
    sock = connect_to_server_tcp(SERVER, PORT)
    msg = 'createuser:'+usuario+':'+senha
    sock.send(msg.encode('utf-8') )
    comando= sock.recv(1024).decode('utf-8')
    comando = comando.replace('\r\n\r\n','')
    if comando == 'ok':
        
        print('tudo certo')
        diretorio= str(QFileDialog.getExistingDirectory(None,"Selecione o Diretorio que você deseja compartilhar")) # seleceção do diretorio
        conf_file.append(usuario+':'+diretorio)
        saveconf()
        #startwatcher(diretorio)
        ui.stackedWidget.setCurrentIndex(0) # return for login



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    #### buttons connections ####
    ui.Registrarse.clicked.connect(registrar_se) # o botao para ir para pagina de registro
    ui.Login.clicked.connect(login) # botao de login
    ui.Registrar.clicked.connect(registrar) # botao de registro
    ui.bt_logout.clicked.connect(logout)
    ui.bt_changedir.clicked.connect(change_dir)

    #############################

    MainWindow.show()
    sys.exit(app.exec_())
