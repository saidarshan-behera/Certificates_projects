import os
import sys
import traceback
import mysql.connector
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView


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


class id(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filedata = None
        self.setFixedWidth(980)
        self.setFixedHeight(420)

        self.setWindowTitle("UPDATE/REMOVE ITEM")

        background_image = resource_path('images/5.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

        label_font = QtGui.QFont()
        label_font.setPointSize(11)
        label_font.setFamily('18th Century')
        label_font.setBold(True)

        tFont = QtGui.QFont()
        tFont.setPointSize(24)
        tFont.setFamily("Distant Galaxy")
        tFont.setBold(True)

        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )
        self.cursor = self.db.cursor()

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setGeometry(300, 0, 400, 60)
        self.lbl.setText("EMPLOYEE DETAILS")
        self.lbl.setFont(tFont)
        self.lbl.setStyleSheet("background: transparent; color: white;")

        self.back = QtWidgets.QPushButton(self)
        self.back.setGeometry(900, 10, 75, 23)
        self.back.setText("BACK")
        self.back.setFont(label_font)
        self.back.clicked.connect(self.admin)
        self.back.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

        self.emp_id = QtWidgets.QLabel(self)
        self.emp_id.setGeometry(70, 115, 110, 13)
        self.emp_id.setText("EMPLOYEE ID")
        self.emp_id.setFont(label_font)
        self.emp_id.setStyleSheet("background: transparent; color: white;")

        self.id = QtWidgets.QComboBox(self)
        self.id.setGeometry(190, 110, 261, 30)
        self.id.setFont(label_font)
        self.id.setEditable(True)
        self.id.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.id.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.id.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.uname = QtWidgets.QLabel(self)
        self.uname.setGeometry(70, 155, 100, 16)
        self.uname.setText("NAME")
        self.uname.setFont(label_font)
        self.uname.setStyleSheet("background: transparent; color: white;")

        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(190, 150, 261, 30)
        self.name.setFont(label_font)
        self.name.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.address = QtWidgets.QLabel(self)
        self.address.setGeometry(70, 195, 100, 16)
        self.address.setText("ADDRESS")
        self.address.setFont(label_font)
        self.address.setStyleSheet("background: transparent; color: white;")

        self.add = QtWidgets.QLineEdit(self)
        self.add.setGeometry(190, 190, 261, 30)
        self.add.setFont(label_font)
        self.add.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.email = QtWidgets.QLabel(self)
        self.email.setGeometry(70, 245, 60, 13)
        self.email.setText("EMAIL")
        self.email.setFont(label_font)
        self.email.setStyleSheet("background: transparent; color: white;")

        self.uemail = QtWidgets.QLineEdit(self)
        self.uemail.setGeometry(190, 240, 261, 30)
        self.uemail.setFont(label_font)
        self.uemail.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.password = QtWidgets.QLabel(self)
        self.password.setGeometry(70, 285, 110, 21)
        self.password.setText('PASSWORD')
        self.password.setFont(label_font)
        self.password.setStyleSheet("background: transparent; color: white;")

        self.upass = QtWidgets.QLineEdit(self)
        self.upass.setGeometry(190, 280, 261, 55)
        self.upass.setFont(label_font)
        self.upass.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.remove = QtWidgets.QPushButton(self)
        self.remove.setGeometry(300, 380, 150, 30)
        self.remove.setText("REMOVE ITEM")
        self.remove.setFont(label_font)
        self.remove.clicked.connect(self.delete_emp)
        self.remove.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

        self.update = QtWidgets.QPushButton(self)
        self.update.setGeometry(100, 380, 150, 30)
        self.update.setText("UPDATE ITEM")
        self.update.setFont(label_font)
        self.update.clicked.connect(self.update_emp)
        self.update.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;font-weight: bold;")

        self.num = "SELECT uid FROM users WHERE uid >0"
        self.cursor.execute(self.num)

        self.tid = [None]

        self.id.addItems([""])
        for i in self.cursor:
            self.tid = list(i)
            self.id.addItem(str(self.tid[0]))

        self.id.currentTextChanged.connect(self.get_info)

        self.see_id = QtWidgets.QLineEdit(self)
        self.see_id.setGeometry(480, 55, 480, 30)
        self.see_id.setFont(label_font)
        self.see_id.setPlaceholderText('SEARCH EMPLOYEE NAME 🔍')
        self.see_id.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; ")
        try:
            self.id_table = QtWidgets.QTableWidget(self)
            self.id_table.setColumnCount(5)
            self.id_table.setGeometry(480, 90, 480, 320)
            self.id_table.setHorizontalHeaderLabels(["UID", "NAME", "ADDRESS", "EMAIL", "PASSWORD"])
            self.id_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.id_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.id_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
            self.id_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.id_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.id_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.id_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

            self.id_table.setStyleSheet(""" 
                        QTableWidget { 
                            background-color: transparent; 
                        } 
                        QHeaderView::section { 
                            background-color: transparent;  /* Make headers transparent */ 
                            color: white;                  /* Change header text color to white */ 
                            font-weight: bold;             /* Make header text bold */ 
                        } 
                        QTableWidget::item { 
                            color: white;                  /* Change item text color to white */ 
                            font-weight: bold;           /* Make item text normal weight */
                        }
                    """)

            self.id_table.setAttribute(Qt.WA_TranslucentBackground)

            query = "SELECT uid,uname,uaddress,email,password FROM users WHERE uid>0"
            self.cursor.execute(query)

            rows = self.cursor.fetchall()

            self.id_table.setRowCount(len(rows))
            self.id_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.id_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.see_id.textEdited.connect(self.show_id)
        except Exception as e:
            print(e)

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()

    def show_id(self):
        try:
            self.cursor.execute(
                f"SELECT uid,uname,uaddress,email,password FROM users WHERE uname like '%{self.see_id.text()}%' AND uid > 0")

            rows = self.cursor.fetchall()

            self.id_table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.id_table.setItem(i, j, QTableWidgetItem(str(col)))
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Table Error", str(e))
            return

    def get_info(self):
        self.tid = self.id.currentText()

        query = "SELECT uname,uaddress,email,password FROM users WHERE uid = %s"
        self.cursor.execute(query, (self.tid,))
        result = self.cursor.fetchone()

        try:
            self.name.setText(result[0])
            self.add.setText(result[1].capitalize())
            self.uemail.setText(result[2])
            self.upass.setText(result[3])

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Uploading Error", str(e))
            return

    def update_emp(self):
        try:
            id = self.id.currentText()
            name = self.name.text()
            address = self.add.text()
            email = self.uemail.text()
            password = self.upass.text()

            query = 'UPDATE users SET uname = %s, uaddress = %s, email = %s, password = %s WHERE uid = %s'
            self.cursor.execute(query, (name, address, email, password, int(id)))
            self.db.commit()
            self.id.setCurrentText(" ")
            self.name.clear()
            self.add.clear()
            self.uemail.clear()
            self.upass.clear()

            query = "SELECT uid,uname,uaddress,email,password FROM users WHERE uid>0"
            self.cursor.execute(query)

            rows = self.cursor.fetchall()

            self.id_table.setRowCount(len(rows))
            self.id_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.id_table.setItem(i, j, QTableWidgetItem(str(col)))

            QtWidgets.QMessageBox.warning(self, "UPDATE", "INFO UPDATED")
        except Exception as e:
            print(e)
            traceback.print_exc()

    def delete_emp(self):
        try:

            if self.id.currentText() == "":
                QtWidgets.QMessageBox.warning(self, "ERROR", "ENTER ITEM ID")
            if self.id.currentText() != "":
                remove = "DELETE FROM users WHERE uid = %s"
                self.cursor.execute(remove, (self.tid,))
                self.db.commit()

                index = self.id.currentIndex()
                self.id.removeItem(index)
                self.id.setCurrentText(" ")

                self.name.clear()
                self.add.clear()
                self.uemail.clear()
                self.upass.clear()

                QtWidgets.QMessageBox.warning(self, "REMOVED", "ITEM REMOVED")

                query = "SELECT uid,uname,uaddress,email,password FROM users WHERE uid>0"
                self.cursor.execute(query)

                rows = self.cursor.fetchall()

                self.id_table.setRowCount(len(rows))
                self.id_table.setColumnCount(len(rows[0]))

                for i, row in enumerate(rows):
                    for j, col in enumerate(row):
                        self.id_table.setItem(i, j, QTableWidgetItem(str(col)))

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Sql Error", str(e))
            return

