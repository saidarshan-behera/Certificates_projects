import os
import sys
import traceback
import mysql.connector
from PyQt5 import QtWidgets, QtGui, QtCore


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


class signup(QtWidgets.QDialog):

    def __init__(self):
        super(signup, self).__init__()
        self.signUp()

    def signUp(self):

        self.setFixedWidth(400)
        self.setFixedHeight(500)

        background_image = resource_path('images/4.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

        label_font = QtGui.QFont()
        label_font.setPointSize(13)
        label_font.setFamily('18th Century')
        label_font.setBold(True)

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

        self.setWindowTitle("SIGNUP PAGE")

        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="sairam",
                database="project"
            )

            self.cursor = self.db.cursor()

            try:
                id_query = "select max(uid) from users"
                self.cursor.execute(id_query)
                re = self.cursor.fetchone()
                self.uid = int(re[0]) + 1
            except Exception as t:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Sql Error", str(t))
                return
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Sql Error", str(e))
            return
        self.head_le = QtWidgets.QLabel(self)
        self.head_le.setText("ADD MEMBER")
        self.head_le.setFont(tFont)
        self.head_le.setGeometry(110, 30, 350, 50)
        self.head_le.setStyleSheet("background: transparent; color: white;")

        self.id_lbl = QtWidgets.QLabel(self)
        self.id_lbl.setFont(headFont)
        self.id_lbl.setText("EMP_ID")
        self.id_lbl.setGeometry(50, 100, 70, 30)
        self.id_lbl.setStyleSheet("background: transparent; color: white;")
        self.id_le = QtWidgets.QLineEdit(self)
        self.id_le.setGeometry(230, 100, 150, 30)
        self.id_le.setFont(headFont)
        self.id_le.setReadOnly(True)
        self.id_le.setText(str(self.uid))
        self.id_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.name_lbl = QtWidgets.QLabel(self)
        self.name_lbl.setFont(headFont)
        self.name_lbl.setText("NAME")
        self.name_lbl.setStyleSheet("background: transparent; color: white;")
        self.name_lbl.setGeometry(50, 140, 70, 30)
        self.name_le = QtWidgets.QLineEdit(self)
        self.name_le.setGeometry(230, 140, 150, 30)
        self.name_le.setFont(headFont)
        self.name_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.gender_lbl = QtWidgets.QLabel(self)
        self.gender_lbl.setFont(headFont)
        self.gender_lbl.setText("GENDER")
        self.gender_lbl.setStyleSheet("background: transparent; color: white;")
        self.gender_lbl.setGeometry(50, 180, 70, 30)
        self.gender_combo = QtWidgets.QComboBox(self)
        self.gender_combo.setGeometry(230, 180, 150, 30)
        self.gender_combo.setFont(headFont)
        self.gender_combo.addItems(["", "M", "F", "O"])
        self.gender_combo.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.phone_lbl = QtWidgets.QLabel(self)
        self.phone_lbl.setFont(headFont)
        self.phone_lbl.setText("PHONE")
        self.phone_lbl.setStyleSheet("background: transparent; color: white;")
        self.phone_lbl.setGeometry(50, 220, 70, 30)
        self.phone_le = QtWidgets.QLineEdit(self)
        self.phone_le.setGeometry(230, 220, 150, 30)
        self.phone_le.setFont(headFont)
        self.phone_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.address_lbl = QtWidgets.QLabel(self)
        self.address_lbl.setFont(headFont)
        self.address_lbl.setText("ADDRESS")
        self.address_lbl.setStyleSheet("background: transparent; color: white;")
        self.address_lbl.setGeometry(50, 260, 100, 30)
        self.address_le = QtWidgets.QLineEdit(self)
        self.address_le.setGeometry(230, 260, 150, 30)
        self.address_le.setFont(headFont)
        self.address_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.email_lbl = QtWidgets.QLabel(self)
        self.email_lbl.setFont(label_font)
        self.email_lbl.setText("EMAIL")
        self.email_lbl.setFont(headFont)
        self.email_lbl.setStyleSheet("background: transparent; color: white;")
        self.email_lbl.setGeometry(50, 300, 70, 30)
        self.email_le = QtWidgets.QLineEdit(self)
        self.email_le.setGeometry(230, 300, 150, 30)
        self.email_le.setFont(headFont)
        self.email_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.password_lbl = QtWidgets.QLabel(self)
        self.password_lbl.setFont(label_font)
        self.password_lbl.setText("PASSWORD")
        self.password_lbl.setStyleSheet("background: transparent; color: white;")
        self.password_lbl.setGeometry(50, 340, 95, 30)
        self.password_lbl.setFont(headFont)
        self.password_le = QtWidgets.QLineEdit(self)
        self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_le.setGeometry(230, 340, 150, 30)
        self.password_le.setFont(headFont)
        self.password_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("background: transparent; color: white;")
        self.show_password_checkbox.setGeometry(230, 410, 150, 30)
        self.show_password_checkbox.stateChanged.connect(self.password_visibility)
        self.show_password_checkbox.setFont(headFont)

        self.confirm_password_lbl = QtWidgets.QLabel(self)
        self.confirm_password_lbl.setFont(label_font)
        self.confirm_password_lbl.setText("CONFIRM PASSWORD")
        self.confirm_password_lbl.setStyleSheet("background: transparent; color: white;")
        self.confirm_password_lbl.setGeometry(50, 380, 180, 30)
        self.confirm_password_lbl.setFont(headFont)
        self.confirm_password_le = QtWidgets.QLineEdit(self)
        self.confirm_password_le.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_le.setGeometry(230, 380, 150, 30)
        self.confirm_password_le.setFont(headFont)
        self.confirm_password_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.signup_btn = QtWidgets.QPushButton(self)
        self.signup_btn.setText("SIGN UP")
        self.signup_btn.setGeometry(150, 440, 100, 30)
        self.signup_btn.setFont(nextFont)
        self.signup_btn.clicked.connect(self.checkAndSave)
        self.signup_btn.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

        self.back_btn = QtWidgets.QPushButton(self)
        self.back_btn.setText("BACK")
        self.back_btn.setGeometry(315, 5, 70, 30)
        self.back_btn.setFont(nextFont)
        self.back_btn.clicked.connect(self.admin)
        self.back_btn.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

    def checkAndSave(self):
        global uid
        name = self.name_le.text()
        gender = self.gender_combo.currentText().upper()
        phone = self.phone_le.text()
        address = self.address_le.text()
        email = self.email_le.text()
        password = self.password_le.text()

        if name == "" or gender == "" or phone == "" or address == "" or email == "" or password == "":
            QtWidgets.QMessageBox.warning(self, "Please", "Fill the above information's first.")
            return

        if len(password) > 15:
            QtWidgets.QMessageBox.warning(self, "Password Limit Exceeded",
                                          "Password length should not exceed 15 characters.")
            return

        if password != self.confirm_password_le.text():
            QtWidgets.QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return

        if gender not in ('M', 'F', "O"):
            QtWidgets.QMessageBox.warning(self, "Invalid Gender", "Gender should be 'M' or 'O'.")
            return

        if len(phone) != 10:
            QtWidgets.QMessageBox.warning(self, "Invalid Number", "Phone number not valid")
            return

        query = "INSERT INTO users (uid, uname, gender, password, uaddress, email, uphone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.uid, name, gender, password, address, email, phone)
        self.cursor.execute(query, values)
        QtWidgets.QMessageBox.information(self, "Success", f"User successfully registered. ID is {self.uid}")
        self.db.commit()

        self.uid += 1
        self.id_le.setText(str(self.uid))
        self.name_le.clear()
        self.gender_combo.setCurrentText("")
        self.phone_le.clear()
        self.address_le.clear()
        self.email_le.clear()
        self.password_le.clear()
        self.confirm_password_le.clear()

    def password_visibility(self, state):
        if state == QtCore.Qt.Checked:
            self.password_le.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.confirm_password_le.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)
            self.confirm_password_le.setEchoMode(QtWidgets.QLineEdit.Password)

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()

