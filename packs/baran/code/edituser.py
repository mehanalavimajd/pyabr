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

import sys, subprocess,os,shutil

from libabr import Files, Control, Permissions, Colors, Process, Modules, Package, Commands, Res, System

modules = Modules()
files = Files()
control = Control()
colors = Colors()
process = Process()
permissions = Permissions()
pack = Package()
commands = Commands()
res = Res()

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

class MainApp (QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.SetWindowIcon(QIcon(res.get('@icon/help-about')))
        self.Widget.SetWindowTitle("Edit user")
        self.Widget.Resize(self, 336, 383)

        uic.loadUi(res.get('@layout/usermanager_edit'),self)

        self.leFirstName = self.findChild(QLineEdit,'leFirstName')
        self.leLastName = self.findChild(QLineEdit, 'leLastName')
        self.leCompany = self.findChild(QLineEdit, 'leCompany')
        self.leEmail = self.findChild(QLineEdit, 'leEmail')
        self.lePhone = self.findChild(QLineEdit, 'lePhone')
        self.cbGender = self.findChild(QComboBox, 'cbGender')
        self.leBirthday = self.findChild(QDateEdit, 'leBirthday')
        self.cbBloodtype = self.findChild(QComboBox, 'cbBloodtype')
        self.btnSave = self.findChild(QPushButton,'btnSave')

        self.typcial = self.External[0]
        self.username = self.External[1]

        if self.username==None: self.Widget.Close()

        if self.typcial=='edit':
            first_name = control.read_record('first_name',f'/etc/users/{self.username}')
            last_name = control.read_record('last_name', f'/etc/users/{self.username}')
            company = control.read_record('company', f'/etc/users/{self.username}')
            email = control.read_record('email', f'/etc/users/{self.username}')
            phone = control.read_record('phone', f'/etc/users/{self.username}')
            gender = control.read_record('gender', f'/etc/users/{self.username}')
            birthday = control.read_record('birthday', f'/etc/users/{self.username}')
            bloodtype = control.read_record('bloodtype', f'/etc/users/{self.username}')

            s = QDateEdit()
            s.setDate(QDate(2020,2,2))

            if not first_name==None:
                self.leFirstName.setText(first_name)
            if not last_name==None:
                self.leLastName.setText(last_name)
            if not company==None:
                self.leCompany.setText(company)
            if not email==None:
                self.leEmail.setText(email)
            if not phone==None:
                self.lePhone.setText(phone)
            if not gender==None:
                self.cbGender.setCurrentText(gender)
            if not birthday==None:
                birthday = birthday.split('-')
                year = int(birthday[0])
                month = int(birthday[1])
                day = int(birthday[2])

                self.leBirthday.setDate(QDate(year,month,day))
            if not bloodtype==None:
                self.cbBloodtype.setCurrentText(bloodtype)

            self.btnSave.clicked.connect (self.edit_)
        else:
            self.Widget.Close()

    def edit_(self):
        self.Env.RunApp('bool',[f'Save changes for {self.External[1]} account',f'Do you want to save changes for {self.External[1]} account?',self.edit_x])

    def edit_x (self,yes):
        if yes:
            first_name = self.leFirstName.text()
            last_name = self.leLastName.text()
            phone = self.lePhone.text()
            email = self.leEmail.text()
            company = self.leCompany.text()
            gender = self.cbGender.currentText()
            bloodtype = self.cbBloodtype.currentText()
            birthday = self.leBirthday.text()

            control.write_record('first_name',first_name,f'/etc/users/{self.External[1]}')
            control.write_record('last_name', last_name, f'/etc/users/{self.External[1]}')
            control.write_record('phone', phone, f'/etc/users/{self.External[1]}')
            control.write_record('email', email, f'/etc/users/{self.External[1]}')
            control.write_record('company', company, f'/etc/users/{self.External[1]}')
            control.write_record('gender', gender, f'/etc/users/{self.External[1]}')
            control.write_record('bloodtype', bloodtype, f'/etc/users/{self.External[1]}')
            control.write_record('birthday', birthday, f'/etc/users/{self.External[1]}')

            self.Widget.Close()
