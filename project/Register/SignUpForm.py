import pymysql
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from project.Public.PublicValue import PublicValue
from UI.Sign_up import Ui_Form
from PyQt5 import QtWidgets


class signUpFrom(QtWidgets.QWidget,Ui_Form):
    global new_username, new_passwd
    #信号定义
    warning_signal = pyqtSignal(str)


    def __init__(self):
        super(signUpFrom,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('注册')
        '''图标设置'''
        self.setWindowIcon(QIcon('Images/login.jfif'))

        #信号绑定
        self.pushButton_cancle.clicked.connect(self.close)
        self.pushButton_signup.clicked.connect(self.create_information)
        self.warning_signal.connect(self.Warning_QMessageBox)

        #写入线程信号绑定
        self.writethread = WriteThread()
        self.writethread.assign_signal.connect(self.Warning_QMessageBox)
        self.writethread.succes_signal.connect(self.Information_QMessageBox)
        self.writethread.close_signal.connect(self.close)



    def create_information(self):
        global new_username,new_passwd

        new_username = self.line_account.text()
        new_passwd = self.line_passwd.text()
        if self.line_confirmpasswd.text()!=new_passwd:
            self.warning_signal.emit('密码不一致')
        else:
            self.writethread.run()

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






class WriteThread(QThread):
    global new_username, new_passwd

    #信号定义
    assign_signal = pyqtSignal(str) #信息反馈信号
    succes_signal = pyqtSignal(str) #成功信号
    close_signal = pyqtSignal()

    def __init__(self):
        super(WriteThread, self).__init__()

    def run(self) -> None:
        global new_username,new_passwd
        try:

            publicvalue = PublicValue()
            self.sqlfile = publicvalue.SQLFileName
            self.insert_sql = str(publicvalue.SQLInsert.format(
                repr(new_username),repr(new_passwd)))
            '''注意！-----------上方利用repr()函数将字符串的双引号改为了单引号，sql语言只识别单引号'''

            # 数据库连接
            self.__con = pymysql.connect('localhost','root','Xulis2017',self.sqlfile)
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cursor = self.__con.cursor()
            self.cursor.execute(self.insert_sql)
            self.__con.commit()
            self.succes_signal.emit('注册成功')
            self.close_signal.emit()
            self.__con.close()  #断开连接
            self.sleep(2)  # 即使不需要睡眠也需要添加sleep(0)，目的是让cpu让步

        except Exception as e:
            self.assign_signal.emit(str(e))