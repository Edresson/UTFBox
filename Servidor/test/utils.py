# -*- coding: utf-8 -*-
from socket import *
import threading
import os
def threaded(func):
    def wrapper(*_args, **kwargs):
        t = threading.Thread(target=func, args=_args)
        t.start()
        return
    return wrapper

def open_text_file(filePath):
    fileObj = None

    #Try to open the file, otherwise return the exception if it cant be opened or isn't found
    try:
        fileObj = open(filePath, 'r')
        print ("Reading <" + str(filePath).upper() + "> from client file-system.")
    except Exception as e:
        print("Error for filepath " + str(filePath) + ":, " + str(e))

    return fileObj

#Determine the number of <BYTES> in text file.
def determine_num_bytes(filePath):
    fileNumBytes = 0

    #Try to determine byte size of file, otherwise return the exception if it cant be opened or isn't found
    try:
        fileNumBytes = os.path.getsize(filePath)
        print ("Total number of bytes in <" + str(filePath).upper() + "> = <" + str(fileNumBytes) + ">")
    except Exception as e:
        print("Error for filepath " + str(filePath) + ":, " + str(e) + "\n")

    return fileNumBytes


#Read the <TEXT FILE> from file system and then write to the socket. When the
#last text byte is encountered, the program will automatically append the character sequence “\r\n\r\n”
# that indicates end-of-file (EOF) and write to the socket.
def read_text_file(sock, fileObj, numBytesFile):
    sock.send(os.path.basename(fileObj.name).encode('utf-8') )#envia o nome do arquivo
    _= sock.recv(1024)# receber confirmacao continua
    for line in fileObj:
        try:
            # Send data
            message = line.encode('utf-8')
            sock.sendall(message)
        except Exception as e:
            print( "Error " + str(e))
    #When the last text byte is encountered, automatically append the character sequence “\r\n\r\n” that indicates end-of-file (EOF) and write to the socket
    sock.sendall("\r\n\r\n".encode('utf-8'))

def test_file_open(filePath):
    fileObj = open_text_file(filePath)
    return fileObj

def test_determine_num_bytes(filePath):
    numBytesFile = determine_num_bytes(filePath)
    return numBytesFile







