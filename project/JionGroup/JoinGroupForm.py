from PyQt5.QtGui import QIcon
from UI.jion_group import Ui_Form
from PyQt5 import QtWidgets
from project.Public.PublicValue import PublicValue

class JoingroupForm(QtWidgets.QWidget,Ui_Form):

    def __init__(self):
        super(JoingroupForm,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('群聊---{}'.format(PublicValue.Username))
        self.setWindowIcon(QIcon('Images/login.jfif'))