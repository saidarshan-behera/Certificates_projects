import os
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication


def resource_path(relative_path):
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        resource_full_path = os.path.join(base_path, relative_path)

        return resource_full_path
    except Exception as e:
        print(f"Error in resource_path: {e}")
        return relative_path


class Admin(QMainWindow):
    def __init__(self):
        super().__init__()

        label_font = QtGui.QFont()
        label_font.setPointSize(11)
        label_font.setFamily('18th Century')
        label_font.setBold(True)

        nextFont = QtGui.QFont()
        nextFont.setPointSize(25)
        nextFont.setFamily("Distant Galaxy")
        nextFont.setBold(True)

        self.setFixedWidth(500)
        self.setFixedHeight(500)

        self.setWindowTitle("ADMIN PAGE")

        background_image = resource_path('images/3.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

        self.add_item = QtWidgets.QPushButton(self)
        self.add_item.setText("ADD ITEM")
        self.add_item.setFont(label_font)
        self.add_item.setGeometry(60, 100, 180, 71)
        self.add_item.clicked.connect(self.add)
        self.add_item.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.update = QtWidgets.QPushButton(self)
        self.update.setGeometry(300, 100, 180, 71)
        self.update.setText("UPDATE/REMOVE ITEM")
        self.update.setFont(label_font)
        self.update.clicked.connect(self.update_item)
        self.update.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.bill = QtWidgets.QPushButton(self)
        self.bill.setGeometry(300, 230, 180, 71)
        self.bill.setText("VIEW BILL")
        self.bill.setFont(label_font)
        self.bill.clicked.connect(self.bill_show)
        self.bill.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.add_member = QtWidgets.QPushButton(self)
        self.add_member.setGeometry(60, 360, 180, 71)
        self.add_member.setText("ADD EMPLOYEE")
        self.add_member.setFont(label_font)
        self.add_member.clicked.connect(self.sign_up)
        self.add_member.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.report = QtWidgets.QPushButton(self)
        self.report.setGeometry(300, 360, 180, 71)
        self.report.setText("SALES REPORT")
        self.report.setFont(label_font)
        self.report.clicked.connect(self.s_report)
        self.report.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.id = QtWidgets.QPushButton(self)
        self.id.setGeometry(60, 230, 180, 71)
        self.id.setText("EMPLOYEE DETAILS")
        self.id.setFont(label_font)
        self.id.clicked.connect(self.know)
        self.id.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.back = QtWidgets.QPushButton(self)
        self.back.setGeometry(410, 10, 81, 41)
        self.back.setText("BACK")
        self.back.setFont(label_font)
        self.back.clicked.connect(self.login)
        self.back.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: black;")

        self.admin = QtWidgets.QLabel(self)
        self.admin.setGeometry(QtCore.QRect(135, 20, 220, 61))
        self.admin.setFont(label_font)
        self.admin.setText("ADMIN PAGE")
        self.admin.setFont(nextFont)
        self.admin.setStyleSheet("background: transparent; color: white;")

    def login(self):
        import Login
        self.s = Login.Login()
        self.s.show()
        self.destroy()

    def add(self):
        import addItem
        self.r = addItem.add()
        self.r.show()
        self.destroy()

    def know(self):
        import know_id
        self.r = know_id.id()
        self.r.show()
        self.destroy()

    def bill_show(self):
        import show_bill
        self.r = show_bill.bill()
        self.r.show()
        self.destroy()

    def sign_up(self):
        import signup
        self.s = signup.signup()
        self.s.show()
        self.destroy()

    def s_report(self):
        import sales_report
        self.s = sales_report.sales()
        self.s.show()
        self.destroy()

    def update_item(self):
        import update_remove_item
        self.s = update_remove_item.update()
        self.s.show()
        self.destroy()

