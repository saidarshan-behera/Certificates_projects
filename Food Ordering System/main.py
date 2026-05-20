import sys
import traceback
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import mysql.connector


class FoodApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(500)
        self.setFixedHeight(350)

        self.id = QtWidgets.QComboBox(self)
        self.id.setGeometry(170, 100, 171, 30)
        self.id.setEditable(True)
        self.id.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.id.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        self.path = QtWidgets.QLabel(self)
        self.path.setGeometry(190, 200, 251, 141)

        self.img_path = QtWidgets.QPushButton(self)
        self.img_path.setText("UPLOAD IMAGE")
        self.img_path.setGeometry(220, 130, 150, 30)
        self.img_path.clicked.connect(self.image_path)

        self.remove = QtWidgets.QPushButton(self)
        self.remove.setGeometry(50, 150, 150, 30)
        self.remove.setText("update")
        self.remove.clicked.connect(self.delete)

        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )

        self.cursor = self.db.cursor()

        self.num = "SELECT tid FROM items"
        self.cursor.execute(self.num)

        self.tid = [None]

        self.id.addItems([""])
        for i in self.cursor:
            self.tid = list(i)
            print(self.tid)
            self.id.addItem(str(self.tid[0]))

    def image_path(self):
        try:

            self.file = QFileDialog()
            self.file = QFileDialog.getOpenFileName(self, "Open File", "", "JPG Files(*.jpg);;PNG Files(*.png)")
            self.photo = QtGui.QPixmap(self.file[0])
            self.resize = self.photo.scaled(220, 250, QtCore.Qt.KeepAspectRatio)
            self.path.setPixmap(self.resize)

            file = open(self.file[0], "rb")
            self.filedata = file.read()

        except Exception as e:
            print(e)

    def delete(self):
        try:
            id = self.id.currentText()
            index = self.id.currentIndex()

            self.cursor.execute('update items set image_path = %s where tid = %s', (self.filedata, id,))
            self.db.commit()
            print('updated')

            self.id.removeItem(index)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FoodApp()
    window.show()
    sys.exit(app.exec_())
