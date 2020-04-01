from UI.Login_interface import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from project.Public.PublicValue import PublicValue
import pymysql
import pandas as pd
from project.Register.SignUpForm import signUpFrom
from project.MainForm.MainChatForm import MainchatForm
#from PyQt5 import Qt

class LoginForm(QtWidgets.QWidget, Ui_Form):
    '''登录账号界面类'''
    global Username,Passwd
    username = ''
    passwd = ''


    #信号定义


    def __init__(self):
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('登录')
        '''图标设置'''
        self.setWindowIcon(QIcon('Images/login.jfif'))

        '''绑定信号与槽'''
        self.pushButton_assign.clicked.connect(self.confirm_information)#登录界面确认按钮绑定函数
        self.pushButton_align.clicked.connect(self.show_signup_ui)#登录界面注册按钮绑定
        self.pushButton_cancle.clicked.connect(self.close)

        #读取线程信号绑定
        self.readthread = ReadThread()
        #self.readthread.assign_signal.connect(self.Information_QMessageBox)
        #self.readthread.startmainwindow_signal.connect()
        self.readthread.closelogin_signal.connect(self.closeLogin)
        self.readthread.labelstatus_signal.connect(self.Label_status)
        self.readthread.tomainform_signal.connect(self.show_mainchat_ui)  #转向聊天窗口的信号绑定

        '''
        self.setWindowFlag(Qt.Qt.FramelessWindowHint)  # 隐藏窗口标题栏
        self.mDragWindow = False
        self.mMousePoint = []
        '''

    def show_signup_ui(self):
        self.register = signUpFrom()
        self.register.show()

    def show_mainchat_ui(self):
        self.showmain =MainchatForm()
        self.showmain.show()



    def confirm_information(self):
        global Username,Passwd,SQlSentence

        self.username = self.line_account.text()
        self.passwd = self.line_passwd.text()
        Username = self.username
        Passwd = self.passwd
        self.label_status.setText('正在登录')
        self.readthread.start()

    '''def remember_passwd(self):
        if self.checkBox_member.isChecked():
            self.Userna'''



    def Label_status(self,content):
        self.label_status.setText(content)


    def closeLogin(self):
        self.close()



    '''
        警告提示框
        content：警告内容
    '''

    def Warning_QMessageBox(self, content):
        warning = QMessageBox.warning(
            self, ("警告"), content,
            QMessageBox.StandardButtons(QMessageBox.Retry)
        )

    '''
    信息提示框
    content:提示内容
    '''

    def Information_QMessageBox(self, content):
        information = QMessageBox.information(
            self, '提示', content,
            QMessageBox.StandardButtons(QMessageBox.Ok)
        )


    #self.setWindowFlag(Qt.Qt.FramelessWindowHint)可以把窗体的标题栏隐藏掉，为移动窗体，需要添加额外的代码：
    '''
    def mouseMoveEvent(self, event):
        e = QMouseEvent(event)
        if self.mDragWindow:
            self.move(e.globalPos() - self.mMousePoint)
            e.accept()

    def mousePressEvent(self, event):
        e = QMouseEvent(event)
        if e.button() == Qt.Qt.LeftButton:
            self.mMousePoint = e.globalPos() - self.pos()
            self.mDragWindow = True
            e.accept()

    def mouseReleaseEvent(self, event):
        self.mDragWindow = False
    '''





class ReadThread(QThread):
    global username,passwd

    #信号定义
    assign_signal = pyqtSignal(str) #信息反馈信号
    startmainwindow_signal = pyqtSignal()  #登录成功后发送可以打开聊天窗口信号
    closelogin_signal = pyqtSignal()  #关闭登录窗口信号
    labelstatus_signal = pyqtSignal(str) #登录界面左下角标签内容信号
    tomainform_signal = pyqtSignal()#转向聊天主窗口信号

    def __init__(self):
        super(ReadThread, self).__init__()

    def run(self) -> None:
        global Username,Passwd
        try:
            publicvalue = PublicValue()
            self.sqlfile = publicvalue.SQLFileName
            self.sql = str(publicvalue.SQLSentence.format(Username,Passwd))
            self.__con = pymysql.connect('localhost','root','Xulis2017',self.sqlfile)  # 数据库连接
            self.data = pd.read_sql(self.sql,self.__con)
            self.data = self.data.values
            #print(self.data)
            if len(self.data)==0:
                self.assign_signal.emit(str("不存在该用户或者输入密码错误"))
                self.labelstatus_signal.emit('登录失败')
            else:
                #print('登录成功')
                PublicValue.Username = Username
                self.labelstatus_signal.emit('登录成功')
                #self.assign_signal.emit("登录成功")
                #self.startmainwindow_signal.emit()  # 发送可以打开聊天窗口信号
                self.closelogin_signal.emit() #发送关闭登录窗口信号
                self.tomainform_signal.emit() #转向聊天窗口信号发送
            self.__con.close()
            self.sleep(2)  # 即使不需要睡眠也需要添加sleep(0)，目的是让cpu让步

        except Exception as e:
            self.assign_signal.emit(str(e))




