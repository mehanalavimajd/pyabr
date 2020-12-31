#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import sys, os
from libabr import Files, Colors, Control, Res
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

files = Files()
colors = Colors()
control = Control()
res = Res()

class MainApp (QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        f = QFont()
        f.setPointSize(12)

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.Appname = ports[3]
        self.External = ports[4]

        self.setStyleSheet('background-color: white;')
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/help-about')))
        ## Finds ##

        self.Widget.Resize(self, int(self.Env.width() / 3), 100)

        self.lblText = QLabel()
        self.lblText.setStyleSheet('padding-left: 10%;padding-right: 10%;')
        self.lblText.resize(int(self.Env.width() / 3), 50)

        self.lblText.setFont(f)
        self.layout().addWidget(self.lblText)

        if self.External[0]=='' or self.External[0]==None:
            self.Widget.SetWindowTitle (res.get('@string/title'))
        elif self.External[1]=='' or self.External[1]==None:
            self.lblText.setText(res.get('@string/text'))
        elif (self.External[1]=='' or self.External[1]==None) and (self.External[0]=='' or self.External[0]==None):
            self.Widget.SetWindowTitle(res.get('@string/title'))
            self.lblText.setText(res.get('@string/text'))
        else:
            self.lblText.setText(self.External[1])
            self.Widget.SetWindowTitle (self.External[0])

        self.btnOK = QPushButton()
        self.btnOK.clicked.connect (self.ok_)
        self.btnOK.setText(res.get('@string/ok'))
        self.btnOK.setGeometry(0, 50, int(self.Env.width())/3, 50)
        self.layout().addWidget(self.btnOK)

    def ok_ (self):
        self.Widget.Close()