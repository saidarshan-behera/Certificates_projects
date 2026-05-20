import os
import sys
import traceback
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import mysql.connector


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


class add(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(800)
        self.setFixedHeight(420)
        self.setWindowTitle("ADD ITEM")

        background_image = resource_path('images/1.jpg')

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

        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="sairam",
                database="project"
            )
            self.cursor = self.db.cursor()
            id_query = "select max(tid) from items"
            self.cursor.execute(id_query)
            re = self.cursor.fetchone()
            self.tid = int(re[0]) + 1
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Sql Error", str(e))
            return

        self.add_items = QtWidgets.QLabel(self)
        self.add_items.setGeometry(350, 35, 220, 60)
        self.add_items.setText("ADD ITEM")
        self.add_items.setFont(tFont)
        self.add_items.setStyleSheet("background: transparent; color: black;")

        self.back = QtWidgets.QPushButton(self)
        self.back.setGeometry(720, 15, 75, 23)
        self.back.setText("BACK")
        self.back.setFont(label_font)
        self.back.clicked.connect(self.admin)
        self.back.setStyleSheet("color: black; border: black;")

        self.item_id = QtWidgets.QLabel(self)
        self.item_id.setGeometry(70, 115, 60, 13)
        self.item_id.setText("ITEM ID")
        self.item_id.setFont(label_font)
        self.item_id.setStyleSheet("background: transparent; color: black;")

        self.id = QtWidgets.QLineEdit(self)
        self.id.setGeometry(190, 110, 261, 30)
        self.id.setReadOnly(True)
        self.id.setFont(label_font)
        self.id.setText(str(self.tid))
        self.id.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.category = QtWidgets.QLabel(self)
        self.category.setGeometry(70, 155, 100, 16)
        self.category.setText("CATEGORY")
        self.category.setFont(label_font)
        self.category.setStyleSheet("background: transparent; color: black;")

        self.items = QtWidgets.QComboBox(self)
        self.items.setGeometry(190, 150, 261, 30)
        self.items.setFont(label_font)
        self.items.addItems(
            [" ", "Pizza", "Burger", "Pasta", "Momo", "Noodles", "Combos", "Donuts", "Cold Beverages", "Hot Beverages"])
        self.items.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.item_name = QtWidgets.QLabel(self)
        self.item_name.setGeometry(70, 195, 100, 16)
        self.item_name.setText("ITEM NAME")
        self.item_name.setFont(label_font)
        self.item_name.setStyleSheet("background: transparent; color: black;")

        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(190, 190, 261, 30)
        self.name.setFont(label_font)
        self.name.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.price = QtWidgets.QLabel(self)
        self.price.setGeometry(70, 245, 60, 13)
        self.price.setText("PRICE")
        self.price.setFont(label_font)
        self.price.setStyleSheet("background: transparent; color: black;")

        self.pri = QtWidgets.QLineEdit(self)
        self.pri.setGeometry(190, 240, 261, 30)
        self.pri.setFont(label_font)
        self.pri.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.description = QtWidgets.QLabel(self)
        self.description.setGeometry(70, 285, 110, 21)
        self.description.setText('DESCRIPTION')
        self.description.setFont(label_font)
        self.description.setStyleSheet("background: transparent; color: black;")

        self.des = QtWidgets.QTextEdit(self)
        self.des.setGeometry(190, 280, 261, 55)
        self.des.setFont(label_font)
        self.des.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.path = QtWidgets.QLabel(self)
        self.path.setGeometry(520, 120, 0, 0)
        self.path.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.img_path = QtWidgets.QPushButton(self)
        self.img_path.setText("UPLOAD IMAGE")
        self.img_path.setGeometry(545, 300, 150, 30)
        self.img_path.setFont(label_font)
        self.img_path.setStyleSheet("color: black; border: black;")
        self.img_path.clicked.connect(self.image_path)

        self.add = QtWidgets.QPushButton(self)
        self.add.setGeometry(350, 360, 150, 30)
        self.add.setText("ADD ITEM")
        self.add.setFont(label_font)
        self.add.setStyleSheet("color: black; border: black;")
        self.add.clicked.connect(self.insert)

    def image_path(self):
        try:
            self.file = QFileDialog.getOpenFileName(self, "Open File", "", "JPG Files(*.jpg);;PNG Files(*.png)")
            if self.file[0]:
                self.photo = QtGui.QPixmap(self.file[0])
                self.resize = self.photo.scaled(220, 250, QtCore.Qt.KeepAspectRatio)
                self.path.setPixmap(self.resize)

                self.path.setGeometry(520, 120, self.resize.width(), self.resize.height())

                file = open(self.file[0], "rb")
                self.filedata = file.read()

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Sql Error", str(e))
            return

    def insert(self):
        try:
            self.cat = self.items.currentText().lower()
            self.i_name = self.name.text()
            self.amt = self.pri.text()
            self.desc = self.des.toPlainText()

            if self.cat == " " or self.i_name == "" or self.amt == "" or self.desc == "" or self.file[0] == "":
                QtWidgets.QMessageBox.warning(self, "ERROR", 'PLEASE ENTER ALL THE ABOVE INFORMATION')
                return
            else:
                query = "INSERT INTO items (tid, category, iname, amt, description, image_path) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (self.tid, self.cat, self.i_name, self.amt, self.desc, self.filedata)

                self.cursor.execute(query, values)
                self.db.commit()

                QtWidgets.QMessageBox.warning(self, "SUCCESSFUL", f'ITEM ADDED')

                self.tid += 1
                self.id.setText(str(self.tid))
                self.items.setCurrentText(" ")
                self.name.clear()
                self.pri.clear()
                self.des.clear()
                self.path.clear()
                self.path.setStyleSheet('background:transparent')

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Sql Error", str(e))
            return

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()

