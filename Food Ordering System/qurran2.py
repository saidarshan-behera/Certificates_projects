from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import  QApplication,QDialog,QMessageBox
import sys
from collections import defaultdict

class confirm(QDialog):

    exp = ""

    def __init__(self):
        super(confirm, self).__init__()
        self.setFixedWidth(500)
        self.setFixedHeight(600)

        cFont = QtGui.QFont()
        cFont.setPointSize(14)
        cFont.setFamily("Ethnocentric")

        oFont = QtGui.QFont()
        oFont.setPointSize(14)
        oFont.setFamily("18th Century")

        self.table2 = QtWidgets.QTableWidget(self)
        self.table2.setRowCount(80)
        self.table2.setColumnCount(3)
        self.table2.setHorizontalHeaderLabels(["Items", "Qty", "Price"])
        self.table2.setGeometry(10, 190, 345, 400)
        self.table2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.name = QtWidgets.QLabel(self)
        self.name.setGeometry(QtCore.QRect(20, 5, 170, 71))
        self.name.setText("NAME:")
        self.name.setFont(cFont)
        self.name_lbl = QtWidgets.QLineEdit(self)
        self.name_lbl.setGeometry(QtCore.QRect(115, 25, 200, 30))
        self.name_lbl.setFont(oFont)

        self.name = self.name_lbl.text()
        print(self.name)

        self.num = QtWidgets.QLabel(self)
        self.num.setGeometry(QtCore.QRect(20, 45, 170, 71))
        self.num.setText("PHONE NO.:")
        self.num.setFont(cFont)
        self.num_lbl = QtWidgets.QLineEdit(self)
        self.num_lbl.setGeometry(QtCore.QRect(180, 65, 200, 30))
        self.num_lbl.setFont(oFont)

        self.ord = QtWidgets.QLabel(self)
        self.ord.setGeometry(QtCore.QRect(20, 85, 170, 71))
        self.ord.setText("ORDER NO.:")
        self.ord.setFont(cFont)
        self.ord_lbl = QtWidgets.QLineEdit(self)
        self.ord_lbl.setGeometry(QtCore.QRect(180, 105, 100, 30))
        self.ord_lbl.setFont(oFont)

        self.total = QtWidgets.QLabel(self)
        self.total.setGeometry(QtCore.QRect(270, 125, 170, 71))
        self.total.setText("TOTAL:")
        self.total.setFont(cFont)
        self.total_lbl = QtWidgets.QLineEdit(self)
        self.total_lbl.setGeometry(QtCore.QRect(375, 145, 100, 30))
        self.total_lbl.setFont(oFont)

        self.disc = QtWidgets.QLabel(self)
        self.disc.setGeometry(QtCore.QRect(20, 125, 170, 71))
        self.disc.setText("DISCOUNT:")
        self.disc.setFont(cFont)
        self.disc_lbl = QtWidgets.QLineEdit(self)
        self.disc_lbl.setGeometry(QtCore.QRect(170, 145, 80, 30))
        self.disc_lbl.setFont(oFont)
        self.update()

        self.conf = QtWidgets.QPushButton(self)
        self.conf.setGeometry(QtCore.QRect(360, 540, 140, 50))
        self.conf.setText("CONFIRM")
        self.conf.setFont(cFont)

        self.back = QtWidgets.QPushButton(self)
        self.back.setText("BACK")
        self.back.setGeometry(405, 5, 90, 30)
        self.back.setFont(cFont)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    s1 = confirm()
    s1.show()
    app.exec_()