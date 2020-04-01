from PyQt5.QtWidgets import QStackedLayout
import sys
from PyQt5 import QtWidgets,QtCore
from UI.total import Ui_Form
from project.Login.One_panel import One_panel
from project.Login.Two_panel import Two_panel


class Duidie(QtWidgets.QWidget, Ui_Form):


    def __init__(self):
        super(Duidie, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.show_panel)
        self.pushButton_2.clicked.connect(self.show_panel)
        #设置堆叠布局给self.frame
        self.qsl = QStackedLayout(self.frame_2)

        one = One_panel()
        two = Two_panel()

        self.qsl.addWidget(one)
        self.qsl.addWidget(two)

    def show_panel(self):
        try:
            dic = {
                "pushButton": 0,
                "pushButton_2": 1,
            }
            index = dic[self.sender().objectName()]   #获取当前点击按钮的名称，结合字典获得索引
            self.qsl.setCurrentIndex(index) #通过索引设置堆叠布局展示的页面
        except Exception as e:
            print(str(e))




if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # 保证QT designer设计出来的windows视图跟运行结果视图一样
    app = QtWidgets.QApplication(sys.argv)
    Widget = Duidie()
    Widget.show()
    sys.exit(app.exec_())
