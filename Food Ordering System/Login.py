import os
import traceback
import mysql.connector
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QDialog
import sys


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


class Login(QDialog):

    def __init__(self):
        super(Login, self).__init__()

        background_image = resource_path('images/2.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

        title_font = QtGui.QFont()
        title_font.setPointSize(21)
        title_font.setFamily("18th Century")
        title_font.setBold(True)

        headFont = QtGui.QFont()
        headFont.setPointSize(12)
        headFont.setFamily("18th Century")
        headFont.setBold(True)

        nextFont = QtGui.QFont()
        nextFont.setPointSize(12)
        nextFont.setFamily("18th Century")
        nextFont.setBold(True)

        tFont = QtGui.QFont()
        tFont.setPointSize(20)
        tFont.setFamily("Distant Galaxy")
        tFont.setBold(True)

        hFont = QtGui.QFont()
        hFont.setPointSize(8)
        hFont.setFamily("18th Century")
        hFont.setBold(True)

        self.setFixedWidth(350)
        self.setFixedHeight(300)

        self.setWindowTitle("LOGIN PAGE")

        self.head_le = QtWidgets.QLabel(self)
        self.head_le.setText("LOGIN")
        self.head_le.setFont(tFont)
        self.head_le.setGeometry(130, 30, 350, 50)
        self.head_le.setStyleSheet("background: transparent; color: white;")

        self.uid_lbl = QtWidgets.QLabel(self)
        self.uid_lbl.setText("ID")
        self.uid_lbl.setGeometry(70, 110, 70, 30)
        self.uid_lbl.setFont(headFont)
        self.uid_lbl.setStyleSheet("background: transparent; color: white;")

        self.uid_le = QtWidgets.QLineEdit(self)
        self.uid_le.setGeometry(180, 110, 120, 30)
        self.uid_le.setFont(headFont)
        self.uid_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.password_lbl = QtWidgets.QLabel(self)
        self.password_lbl.setText("PASSWORD")
        self.password_lbl.setGeometry(70, 150, 100, 30)
        self.password_lbl.setFont(headFont)
        self.password_lbl.setStyleSheet("background: transparent; color: white;")

        self.password_le = QtWidgets.QLineEdit(self)
        self.password_le.setGeometry(180, 150, 120, 30)
        self.password_le.setFont(headFont)
        self.password_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")
        self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)

        self.show_password_checkbox = QtWidgets.QCheckBox("SHOW PASSWORD", self)
        self.show_password_checkbox.setGeometry(180, 180, 120, 30)
        self.show_password_checkbox.stateChanged.connect(self.password_visibility)
        self.show_password_checkbox.setFont(hFont)
        self.show_password_checkbox.setStyleSheet("background: transparent; color: white;")

        self.login_btn = QtWidgets.QPushButton(self)
        self.login_btn.setGeometry(120, 230, 100, 30)
        self.login_btn.setText('LOGIN')
        self.login_btn.setFont(nextFont)
        self.login_btn.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")
        self.login_btn.clicked.connect(self.login)

        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="sairam",
                database="project"
            )

            self.cursor = self.db.cursor()

            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS `users` (
                        `uid` TINYINT NOT NULL,
                        `uname` VARCHAR(20) NOT NULL,
                        `nname` VARCHAR(6) DEFAULT NULL,
                        `gender` ENUM('M', 'F', 'O') DEFAULT NULL,
                        `password` VARCHAR(15) NOT NULL,
                        `uaddress` VARCHAR(100) NOT NULL,
                        `email` VARCHAR(50) NOT NULL,
                        `uphone` VARCHAR(10) NOT NULL,
                        PRIMARY KEY (`uid`)
                    )
                """)

            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS `items` (
                        `tid` INT NOT NULL,
                        `category` VARCHAR(15) DEFAULT NULL,
                        `iname` VARCHAR(50) DEFAULT NULL,
                        `amt` VARCHAR(4) DEFAULT NULL,
                        `description` VARCHAR(500) DEFAULT NULL,
                        `image_path` LONGBLOB,
                        PRIMARY KEY (`tid`)
                    )
                 """)

            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS `food_txn` (
                        `order_id` BIGINT DEFAULT NULL,
                        `cust_name` VARCHAR(50) DEFAULT NULL,
                        `cust_phone` VARCHAR(10) DEFAULT NULL,
                        `item_name` VARCHAR(100) DEFAULT NULL,
                        `qty` BIGINT DEFAULT NULL,
                        `price` VARCHAR(10) DEFAULT NULL,
                        `total` BIGINT DEFAULT NULL,
                        `date_txn` DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)

            self.cursor.execute(
                """INSERT IGNORE INTO `users` (uid, password) VALUES (0, 'password1')"""
            )

        except Exception as e:
            traceback.print_exc()
            self.show_message("Sql Error", "Table Creation Error")

    def login(self):
        self.uid = self.uid_le.text()
        password = self.password_le.text()

        query = "SELECT password FROM users WHERE uid = %s"
        self.cursor.execute(query, (self.uid,))
        result = self.cursor.fetchone()

        try:
            if result:
                if password == result[0]:
                    if self.uid == "0":
                        self.admin()
                        self.destroy()
                    else:
                        self.secondPage()
                else:
                    self.show_message("Login Error", "Incorrect password")
            else:
                self.show_message("Login Error", "Username not found")
        except Exception as e:
            traceback.print_exc()
            self.show_message('Login Error', str(e))

        self.db.commit()

    def show_message(self, title, message):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        msg_box.setStyleSheet("background-color: white; color: black;")

        msg_box.exec_()

    def secondPage(self):
        import prac4
        self.s = prac4.FoodApp()
        self.s.show()
        self.destroy()

    def password_visibility(self, state):
        if state == QtCore.Qt.Checked:
            self.password_le.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = Login()
    l.show()
    sys.exit(app.exec_())

