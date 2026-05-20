import traceback
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow
import mysql.connector


class remove(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(500)
        self.setFixedHeight(350)

        label_font = QtGui.QFont()
        label_font.setPointSize(11)
        label_font.setFamily('18th Century')

        tFont = QtGui.QFont()
        tFont.setPointSize(20)
        tFont.setFamily("Distant Galaxy")

        self.setWindowTitle("REMOVE ITEM")

        self.rem_items = QtWidgets.QLabel(self)
        self.rem_items.setGeometry(150, 20, 250, 60)
        self.rem_items.setText("REMOVE ITEM")
        self.rem_items.setFont(tFont)

        self.back = QtWidgets.QPushButton(self)
        self.back.setGeometry(400, 20, 75, 23)
        self.back.setText("BACK")
        self.back.setFont(label_font)
        self.back.clicked.connect(self.admin)

        self.item_id = QtWidgets.QLabel(self)
        self.item_id.setGeometry(70, 105, 60, 13)
        self.item_id.setText("ITEM ID")
        self.item_id.setFont(label_font)

        self.id = QtWidgets.QComboBox(self)
        self.id.setGeometry(170, 100, 171, 30)
        self.id.setFont(label_font)
        self.id.setEditable(True)
        self.id.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.id.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        self.category = QtWidgets.QLabel(self)
        self.category.setGeometry(70, 145, 80, 16)
        self.category.setText("CATEGORY")
        self.category.setFont(label_font)
        self.items = QtWidgets.QLineEdit(self)
        self.items.setGeometry(170, 140, 171, 30)
        self.items.setFont(label_font)
        self.items.setReadOnly(True)

        self.item_name = QtWidgets.QLabel(self)
        self.item_name.setGeometry(70, 185, 80, 16)
        self.item_name.setText("ITEM NAME")
        self.item_name.setFont(label_font)
        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(170, 180, 171, 30)
        self.name.setFont(label_font)
        self.name.setReadOnly(True)

        self.price = QtWidgets.QLabel(self)
        self.price.setGeometry(70, 235, 60, 13)
        self.price.setText("PRICE")
        self.price.setFont(label_font)
        self.pri = QtWidgets.QLineEdit(self)
        self.pri.setGeometry(170, 230, 171, 30)
        self.pri.setFont(label_font)
        self.pri.setReadOnly(True)

        self.remove = QtWidgets.QPushButton(self)
        self.remove.setGeometry(170, 280, 150, 30)
        self.remove.setText("REMOVE ITEM")
        self.remove.setFont(label_font)
        self.remove.clicked.connect(self.delete)

        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )

        self.cursor = self.db.cursor()

        self.num = "SELECT tid FROM items WHERE tid>0"
        self.cursor.execute(self.num)

        self.tid = [None]

        self.id.addItems([""])
        for i in self.cursor:
            self.tid = list(i)
            self.id.addItem(str(self.tid[0]))

        self.id.currentTextChanged.connect(self.info)

    def info(self):
        self.tid = self.id.currentText()
        query = "SELECT iname,category,amt FROM items WHERE tid = %s"
        self.cursor.execute(query, (self.tid,))
        result = self.cursor.fetchone()

        self.name.setText(result[0])
        self.items.setText(result[1].capitalize())
        self.pri.setText(result[2])
        self.db.commit()

    def delete(self):
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

                self.id.setCurrentText("")
                self.items.clear()
                self.name.clear()
                self.pri.clear()

                QtWidgets.QMessageBox.warning(self, "SUCCESSFUL", "ITEM DELETED")
                return

        except Exception as e:
            traceback.print_exc()

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()
