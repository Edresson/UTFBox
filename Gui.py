# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(308, 254)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 0, 291, 211))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidgetPage1 = QtWidgets.QWidget()
        self.stackedWidgetPage1.setObjectName("stackedWidgetPage1")
        self.label_2 = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 191, 20))
        self.label_2.setObjectName("label_2")
        self.Senha = QtWidgets.QLineEdit(self.stackedWidgetPage1)
        self.Senha.setGeometry(QtCore.QRect(120, 70, 113, 25))
        self.Senha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Senha.setObjectName("Senha")
        self.Login = QtWidgets.QPushButton(self.stackedWidgetPage1)
        self.Login.setGeometry(QtCore.QRect(120, 120, 80, 25))
        self.Login.setObjectName("Login")
        self.lSenha = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.lSenha.setGeometry(QtCore.QRect(60, 70, 54, 17))
        self.lSenha.setObjectName("lSenha")
        self.label = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.label.setGeometry(QtCore.QRect(60, 20, 54, 17))
        self.label.setObjectName("label")
        self.Registrarse = QtWidgets.QPushButton(self.stackedWidgetPage1)
        self.Registrarse.setGeometry(QtCore.QRect(120, 180, 80, 25))
        self.Registrarse.setObjectName("Registrarse")
        self.Usuario = QtWidgets.QLineEdit(self.stackedWidgetPage1)
        self.Usuario.setGeometry(QtCore.QRect(120, 20, 113, 25))
        self.Usuario.setObjectName("Usuario")
        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.stackedWidgetPage2 = QtWidgets.QWidget()
        self.stackedWidgetPage2.setObjectName("stackedWidgetPage2")
        self.Registrar = QtWidgets.QPushButton(self.stackedWidgetPage2)
        self.Registrar.setGeometry(QtCore.QRect(127, 160, 80, 25))
        self.Registrar.setObjectName("Registrar")
        self.RSenha = QtWidgets.QLineEdit(self.stackedWidgetPage2)
        self.RSenha.setGeometry(QtCore.QRect(127, 70, 113, 25))
        self.RSenha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.RSenha.setObjectName("RSenha")
        self.labelsenha = QtWidgets.QLabel(self.stackedWidgetPage2)
        self.labelsenha.setGeometry(QtCore.QRect(67, 70, 54, 17))
        self.labelsenha.setObjectName("labelsenha")
        self.confSenha = QtWidgets.QLineEdit(self.stackedWidgetPage2)
        self.confSenha.setGeometry(QtCore.QRect(127, 110, 113, 25))
        self.confSenha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confSenha.setObjectName("confSenha")
        self.label_3 = QtWidgets.QLabel(self.stackedWidgetPage2)
        self.label_3.setGeometry(QtCore.QRect(67, 20, 54, 17))
        self.label_3.setObjectName("label_3")
        self.RUsuario = QtWidgets.QLineEdit(self.stackedWidgetPage2)
        self.RUsuario.setGeometry(QtCore.QRect(127, 20, 113, 25))
        self.RUsuario.setObjectName("RUsuario")
        self.labelconfsenha = QtWidgets.QLabel(self.stackedWidgetPage2)
        self.labelconfsenha.setGeometry(QtCore.QRect(20, 110, 101, 20))
        self.labelconfsenha.setObjectName("labelconfsenha")
        self.stackedWidget.addWidget(self.stackedWidgetPage2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UTFBox"))
        self.stackedWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Não possui conta ?  Registre-se"))
        self.Login.setText(_translate("MainWindow", "Login"))
        self.lSenha.setText(_translate("MainWindow", "Senha:"))
        self.label.setText(_translate("MainWindow", "Usuario:"))
        self.Registrarse.setText(_translate("MainWindow", "Registrar-se "))
        self.Registrar.setText(_translate("MainWindow", "Registrar"))
        self.labelsenha.setText(_translate("MainWindow", "Senha:"))
        self.label_3.setText(_translate("MainWindow", "Usuario:"))
        self.labelconfsenha.setText(_translate("MainWindow", "Confirmar senha:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
