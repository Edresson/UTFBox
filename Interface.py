from Gui import *

from PyQt5.QtWidgets import QFileDialog

import os.path

DIRETORIO_PADRAO = 'D:\Observada\Cliente'

def encontrar_string(path, string):
    with open((DIRETORIO_PADRAO + path),'r') as f:
        texto=f.readlines()
    for i in texto:
        if string in i:
            return (texto.index(i))
        else:
            print('')

def ler_linha(path,index_linha):
    with open((DIRETORIO_PADRAO + path),'r') as f:
        texto=f.readlines()
    with open((DIRETORIO_PADRAO + path),'r') as minhalista:
        for i in texto:
            if int(texto.index(i))==int(index_linha):
                password=minhalista.readline()
            else:
                minhalista.readline()
        return password

def cria_diretorio_padrao():
    if os.path.isdir(DIRETORIO_PADRAO): # vemos de este diretorio ja existe
        print ('Ja existe uma pasta com esse nome!')
    else:
        os.mkdir(DIRETORIO_PADRAO) # aqui criamos a pasta caso nao exista
        print ('Pasta criada com sucesso!')
    try:
        nome_usuarios = DIRETORIO_PADRAO + 'usuarios.txt'
        arquivo_users = open(nome_usuarios, 'r+')
    except FileNotFoundError:
        arquivo_users = open(nome_usuarios, 'w+')
        arquivo_users.writelines(u'admin\n')
    arquivo_users.close()
    try:
        nome_senhas = DIRETORIO_PADRAO + 'senhas.txt'
        arquivo_pass = open(nome_senhas, 'r+')
    except FileNotFoundError:
        arquivo_pass = open(nome_senhas, 'w+')
        arquivo_pass.writelines(u'admin\n')
    arquivo_pass.close()    


def get_login_information(ui):
    return ui.Usuario.text(),ui.Senha.text()

def get_register_information(ui):
    return ui.RUsuario.text(),ui.RSenha.text(),ui.confSenha.text()

def registrar_se():
    global ui
    ui.stackedWidget.setCurrentIndex(1)

def login():
    global ui
    usuario,senha=get_login_information(ui)
    senhaencontrada = ler_linha('senhas.txt', (encontrar_string('usuarios.txt', usuario)))
    print(senha)
    print(senhaencontrada)
    senhaencontrada=senhaencontrada.replace('\n', '')
    if str(senhaencontrada)==str(senha) :
        print('login efetuado com sucesso')
    else:
        print('Usuário não encontrado')

def registrar():
    global ui
    usuario,senha,confsenha=get_register_information(ui)
    print(usuario,senha,confsenha)
    if senha!=confsenha:
        print('Senhas diferentes!')
    
    #GRAVA USUARIO
    diretorio = DIRETORIO_PADRAO + 'usuarios.txt'
    arquivo = open(diretorio, 'r') # Abra o arquivo (leitura)
    conteudo = arquivo.readlines()
    conteudo.append(usuario + '\n')   # insira seu conteúdo
    arquivo = open(diretorio, 'w') # Abre novamente o arquivo (escrita)
    arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
    arquivo.close()
    #GRAVA SENHA
    diretorio = DIRETORIO_PADRAO + 'senhas.txt'
    arquivo = open(diretorio, 'r') # Abra o arquivo (leitura)
    conteudo = arquivo.readlines()
    conteudo.append(senha + '\n')   # insira seu conteúdo
    arquivo = open(diretorio, 'w') # Abre novamente o arquivo (escrita)
    arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
    arquivo.close()
    #diretorio= str(QFileDialog.getExistingDirectory(None,"Selecione o Diretorio que você deseja compartilhar")) # seleceção do diretorio
    if os.path.isdir(DIRETORIO_PADRAO + usuario): # vemos de este diretorio ja existe
        print ('Ja existe uma pasta com esse nome!')
    else:
        os.mkdir(DIRETORIO_PADRAO+ usuario) # aqui criamos a pasta caso nao exista
        print ('Pasta criada com sucesso!')
    print('Voltar para página principal')


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
    #############################
    cria_diretorio_padrao()
    MainWindow.show()
    sys.exit(app.exec_())
