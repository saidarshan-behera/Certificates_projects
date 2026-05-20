import os
import sys
import traceback
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
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


class update(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filedata = None
        self.random = 0
        self.setFixedWidth(1200)
        self.setFixedHeight(420)

        self.setWindowTitle("UPDATE/REMOVE ITEM")

        background_image = resource_path('images/6.jpg')

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

        self.ur_items = QtWidgets.QLabel(self)
        self.ur_items.setGeometry(450, 0, 400, 60)
        self.ur_items.setText("REMOVE/UPDATE ITEM")
        self.ur_items.setFont(tFont)
        self.ur_items.setStyleSheet("background: transparent; color: white;")

        self.back = QtWidgets.QPushButton(self)
        self.back.setGeometry(1120, 10, 75, 23)
        self.back.setText("BACK")
        self.back.setFont(label_font)
        self.back.clicked.connect(self.admin)
        self.back.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

        self.item_id = QtWidgets.QLabel(self)
        self.item_id.setGeometry(70, 115, 60, 13)
        self.item_id.setText("ITEM ID")
        self.item_id.setFont(label_font)
        self.item_id.setStyleSheet("background: transparent; color: white;")

        self.id = QtWidgets.QComboBox(self)
        self.id.setGeometry(190, 110, 261, 30)
        self.id.setFont(label_font)
        self.id.setEditable(True)
        self.id.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.id.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.id.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.category = QtWidgets.QLabel(self)
        self.category.setGeometry(70, 155, 100, 16)
        self.category.setText("CATEGORY")
        self.category.setFont(label_font)
        self.category.setStyleSheet("background: transparent; color: white;")

        self.items = QtWidgets.QLineEdit(self)
        self.items.setGeometry(190, 150, 261, 30)
        self.items.setFont(label_font)
        self.items.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.item_name = QtWidgets.QLabel(self)
        self.item_name.setGeometry(70, 195, 100, 16)
        self.item_name.setText("ITEM NAME")
        self.item_name.setFont(label_font)
        self.item_name.setStyleSheet("background: transparent; color: white;")

        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(190, 190, 261, 30)
        self.name.setFont(label_font)
        self.name.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.price = QtWidgets.QLabel(self)
        self.price.setGeometry(70, 245, 60, 13)
        self.price.setText("PRICE")
        self.price.setFont(label_font)
        self.price.setStyleSheet("background: transparent; color: white;")

        self.pri = QtWidgets.QLineEdit(self)
        self.pri.setGeometry(190, 240, 261, 30)
        self.pri.setFont(label_font)
        self.pri.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.description = QtWidgets.QLabel(self)
        self.description.setGeometry(70, 285, 110, 21)
        self.description.setText('DESCRIPTION')
        self.description.setFont(label_font)
        self.description.setStyleSheet("background: transparent; color: white;")

        self.des = QtWidgets.QTextEdit(self)
        self.des.setGeometry(190, 280, 261, 55)
        self.des.setFont(label_font)
        self.des.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.path = QtWidgets.QLabel(self)
        self.path.setGeometry(545, 120,0, 0)
        self.path.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.img_path = QtWidgets.QPushButton(self)
        self.img_path.setText("UPLOAD IMAGE")
        self.img_path.setGeometry(500, 300, 150, 30)
        self.img_path.setFont(label_font)
        self.img_path.clicked.connect(self.image_path)
        self.img_path.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

        self.remove = QtWidgets.QPushButton(self)
        self.remove.setGeometry(420, 380, 150, 30)
        self.remove.setText("REMOVE ITEM")
        self.remove.setFont(label_font)
        self.remove.clicked.connect(self.delete_item)
        self.remove.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

        self.update = QtWidgets.QPushButton(self)
        self.update.setGeometry(230, 380, 150, 30)
        self.update.setText("UPDATE ITEM")
        self.update.setFont(label_font)
        self.update.clicked.connect(self.update_item)
        self.update.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;font-weight: bold;")

        self.num = "SELECT tid FROM items WHERE tid >0"
        self.cursor.execute(self.num)

        self.tid = [None]

        self.id.addItems([""])
        for i in self.cursor:
            self.tid = list(i)
            self.id.addItem(str(self.tid[0]))

        self.id.currentTextChanged.connect(self.get_info)

        self.see_id = QtWidgets.QLineEdit(self)
        self.see_id.setGeometry(700, 55, 480, 30)
        self.see_id.setFont(label_font)
        self.see_id.setPlaceholderText('SEARCH ITEM NAME 🔍')
        self.see_id.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; ")

        self.id_table = QtWidgets.QTableWidget(self)
        self.id_table.setColumnCount(4)
        self.id_table.setGeometry(700, 90, 480, 320)
        self.id_table.setHorizontalHeaderLabels(["ID", "CATEGORY", "ITEM", "PRICE"])
        self.id_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.id_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.id_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.id_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.id_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.id_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

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
                    QTableWidget::item[data-role="item"] { 
                        font-weight: bold;             /* Make item name text bold if necessary */ 
                    } 
                """)

        self.id_table.setAttribute(Qt.WA_TranslucentBackground)

        query = "SELECT tid,category,iname,amt  FROM items WHERE tid>0 ORDER BY category DESC"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        self.id_table.setRowCount(len(rows))
        self.id_table.setColumnCount(len(rows[0]))

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.id_table.setItem(i, j, QTableWidgetItem(str(col)))

        self.see_id.textEdited.connect(self.show_id)

    def show_id(self):
        try:
            self.cursor.execute(f"SELECT * FROM items WHERE iname like '%{self.see_id.text()}%' AND tid > 0")

            rows = self.cursor.fetchall()

            self.id_table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.id_table.setItem(i, j, QTableWidgetItem(str(col)))
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Table Error", str(e))
            return

    def image_path(self):
        try:
            self.file = QFileDialog()
            self.file = QFileDialog.getOpenFileName(self, "Open File", "", "JPG Files(*.jpg);;PNG Files(*.png)")
            if self.file[0]:
                self.photo = QtGui.QPixmap(self.file[0])
                self.resize = self.photo.scaled(220, 210, QtCore.Qt.KeepAspectRatio)
                self.path.setPixmap(self.resize)

                self.path.setGeometry(470, 120, self.resize.width(), self.resize.height())

                file = open(self.file[0], "rb")
                self.filedata = file.read()
                self.random += 1

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Inserting Error", str(e))
            return

    def get_info(self):
        self.tid = self.id.currentText()

        query = "SELECT iname,category,amt,description,image_path FROM items WHERE tid = %s"
        self.cursor.execute(query, (self.tid,))
        result = self.cursor.fetchone()

        try:
            self.name.setText(result[0])
            self.items.setText(result[1].capitalize())
            self.pri.setText(result[2])
            self.des.setText(result[3])

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(result[4])
            self.path.setPixmap(pixmap)
            self.path.setGeometry(480, 120, pixmap.width(), pixmap.height())

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Uploading Error", str(e))
            return

    def update_item(self):
        id = self.id.currentText()
        name = self.name.text()
        amt = self.pri.text()
        desc = self.des.toPlainText()

        if self.random != 0:
            query = 'UPDATE items SET iname = %s, amt = %s, description = %s, image_path = %s WHERE tid = %s'
            self.cursor.execute(query, (name, amt, desc, self.filedata, id))
            self.db.commit()
        else:
            query = 'UPDATE items SET iname = %s, amt = %s, description = %s WHERE tid = %s'
            self.cursor.execute(query, (name, amt, desc, id))
            self.db.commit()

        QtWidgets.QMessageBox.warning(self, "UPDAtE", "ITEM UPDATED")

        self.id.setCurrentText(" ")
        self.items.clear()
        self.name.clear()
        self.pri.clear()
        self.des.clear()
        self.path.clear()
        self.see_id.clear()

        self.id_table.clear()
        self.id_table.setHorizontalHeaderLabels(["ID", "CATEGORY", "ITEM", "PRICE"])

        query = "SELECT tid,category,iname,amt  FROM items WHERE tid>0 ORDER BY category DESC"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        self.id_table.setRowCount(len(rows))
        self.id_table.setColumnCount(len(rows[0]))

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.id_table.setItem(i, j, QTableWidgetItem(str(col)))

    def delete_item(self):
        try:
            if self.id.currentText() == "":
                QtWidgets.QMessageBox.warning(self, "ERROR", "ENTER ITEM ID")
                return
            else:
                remove = "DELETE FROM items WHERE tid = %s"
                self.cursor.execute(remove, (self.tid,))
                self.db.commit()

                index = self.id.currentIndex()
                self.id.removeItem(index)
                self.id.setCurrentText(" ")

                QtWidgets.QMessageBox.warning(self, "REMOVED", "ITEM REMOVED")

                self.items.clear()
                self.name.clear()
                self.pri.clear()
                self.des.clear()
                self.path.clear()
                self.see_id.clear()

                self.id_table.clear()
                self.id_table.setHorizontalHeaderLabels(["ID", "CATEGORY", "ITEM", "PRICE"])

                query = "SELECT tid,category,iname,amt  FROM items WHERE tid>0 ORDER BY category DESC"
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

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()

