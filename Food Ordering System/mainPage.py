import sys
import mysql.connector
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication


class Admin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.path = QtWidgets.QLabel(self)
        self.path.setGeometry(0, 0, 251, 141)

        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )

        self.curr = self.db.cursor()

        """query1 = "select image_path from items where tid = 2"
        self.curr.execute(query1)
        data = self.curr.fetchone()[0]
        print(data)

        image = QtGui.QImage.fromData(data)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.path.setPixmap(pixmap)"""

        self.curr.execute(f'select image_path from items where tid = 2')
        data2 = self.curr.fetchall()
        self.photo = data2[0][0]
        with open(self.photo, 'rb') as file:
            image_data = file.read()
        self.pic = QtGui.QPixmap()
        self.pic.loadFromData(image_data)
        self.path.setPixmap(self.pic)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = Admin()
    l.show()
    sys.exit(app.exec_())
