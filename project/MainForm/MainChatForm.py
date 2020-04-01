import time
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from UI.MainWindow import Ui_Form
from PyQt5 import QtWidgets
from project.Public.PublicValue import PublicValue
from project.JionGroup.JoinGroupForm import JoingroupForm
import socket,threading
from Server import getIp,getport
import random

ck = None  # 用于储存客户端的信息

class MainchatForm(QtWidgets.QWidget,Ui_Form):
    global ck

    #信号定义
    send_signal = pyqtSignal(str)  #发送到显示框信号
    send_over_signal = pyqtSignal(str)  #发送结束后需要清空发送框内容信号

    #用户字体颜色定义
    color_num = random.randint(0,11)
    color = PublicValue.Colors[color_num]

    def __init__(self):
        super(MainchatForm,self).__init__()
        self.setupUi(self)
        self.username = PublicValue.Username
        self.setWindowTitle('聊天室---{}'.format(self.username))
        self.setWindowIcon(QIcon('Images/login.jfif'))
        self.connectServer()


        #信号绑定
        self.pushButton_addgroup.clicked.connect(self.show_addgroup_ui)   #加群按钮绑定显示加群界面
        self.pushButton_zhangsan.clicked.connect(self.connectServer)    #对象按钮绑定
        self.pushButton_SendMessageInterface.clicked.connect(self.sendMail)
        self.pushButton_lisi.clicked.connect(self.connectServer)
        self.send_signal.connect(self.sendTxt)
        self.send_over_signal.connect(self.clear_send)


    def sendTxt(self, content):
        # self.textEdit_chat.setPlainText(content)
        #self.textEdit_chat.append(content)

        self.textEdit_chat.append("<p align='left' style='color:blue'>我来了</p>"

                                  )


    #清空发送消息框，将发送内容写到消息框中
    def clear_send(self,content):
        self.textEdit_SendMessageInterface.clear()  #清空发送消息框内容
        self.textEdit_chat.append("<p style='text-align:right;color:red'>{}</p>".format(content))

        #self.textEdit_chat.setAlignment()


    def show_addgroup_ui(self):
        self.addgroup = JoingroupForm()
        self.addgroup.show()

    def getInfo(self):
        global ck
        try:
            while True:
                data = ck.recv(1024)  # 用于接受服务器发送的信息
                # 显示在信息框上
                self.send_signal.emit(data.decode("utf-8"))
        except Exception as e:
            print(str(e))

    def connectServer(self):
        global ck
        try:
            self.ipStr = getIp()
            self.portStr = getport()
            self.userStr = self.username
            # socked所准守ipv4或ipv6，和相关协议的
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 连接ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
            client.connect((self.ipStr, int(self.portStr)))
            # 2:bind()的参数是一个元组的形式
            client.send(self.userStr.encode("utf-8"))
            ck = client
            t = threading.Thread(target=self.getInfo)
            t.start()
        except Exception as e:
            print(str(e))

    def sendMail(self):
        global ck
        try:
            if self.username == '李四':
                friend = '张三'
            if self.username == '张三':
                friend = '李四'
            sendStr = self.textEdit_SendMessageInterface.toPlainText()  # 获取发送消息框中的发送消息内容
            sendStr = friend + ":" + sendStr
            ck.send(sendStr.encode("utf-8"))
            self.send_over_signal.emit(self.textEdit_SendMessageInterface.toPlainText())
        except Exception as e:
            print(str(e))





