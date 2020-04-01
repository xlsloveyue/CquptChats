import sys
from PyQt5 import QtWidgets,QtCore
from project.Login.LoginForm import LoginForm





if __name__ == "__main__":

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # 保证QT designer设计出来的windows视图跟运行结果视图一样
    app = QtWidgets.QApplication(sys.argv)
    Widget = LoginForm()
    Widget.show()
    sys.exit(app.exec_())