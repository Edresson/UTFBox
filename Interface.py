from Gui import *

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
    print(usuario,senha)

def registrar():
    global ui
    usuario,senha,confsenha=get_register_information(ui)
    print(usuario,senha,confsenha)

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
    
    MainWindow.show()
    sys.exit(app.exec_())
