import os
import sys
import traceback
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem
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


class bill(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(600)
        self.setFixedHeight(620)

        self.setWindowTitle("BILL")
        background_image = resource_path('images/8.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

        try:

            nextFont = QtGui.QFont()
            nextFont.setPointSize(20)
            nextFont.setFamily("Distant Galaxy")
            nextFont.setBold(True)

            label_font = QtGui.QFont()
            label_font.setPointSize(11)
            label_font.setFamily('18th Century')
            label_font.setBold(True)

            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="sairam",
                database="project"
            )
            self.cursor = self.db.cursor()

            self.title = QtWidgets.QLabel(self)
            self.title.setGeometry(235, 10, 140, 30)
            self.title.setText("SEE BILL")
            self.title.setFont(nextFont)
            self.title.setStyleSheet("background: transparent; color: white;")

            self.id = QtWidgets.QLabel(self)
            self.id.setGeometry(20, 60, 70, 30)
            self.id.setText("O_ID :")
            self.id.setFont(label_font)
            self.id.setStyleSheet("background: transparent; color: white;")

            self.num = QtWidgets.QLineEdit(self)
            self.num.setGeometry(80, 60, 70, 30)
            self.num.setFont(label_font)
            self.num.setStyleSheet(
                "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

            self.back = QtWidgets.QPushButton(self)
            self.back.setGeometry(500, 5, 75, 23)
            self.back.setText("BACK")
            self.back.setFont(label_font)
            self.back.clicked.connect(self.admin)
            self.back.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

            self.cust = QtWidgets.QLabel(self)
            self.cust.setGeometry(160, 60, 100, 30)
            self.cust.setText("NAME :")
            self.cust.setFont(label_font)
            self.cust.setStyleSheet("background: transparent; color: white;")

            self.cust_v = QtWidgets.QLineEdit(self)
            self.cust_v.setGeometry(215, 60, 180, 30)
            self.cust_v.setFont(label_font)
            self.cust_v.setReadOnly(True)
            self.cust_v.setStyleSheet(
                "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

            self.phone = QtWidgets.QLabel(self)
            self.phone.setGeometry(400, 60, 100, 30)
            self.phone.setText("PHONE :")
            self.phone.setFont(label_font)
            self.phone.setStyleSheet("background: transparent; color: white;")

            self.phone_v = QtWidgets.QLineEdit(self)
            self.phone_v.setGeometry(470, 60, 125, 30)
            self.phone_v.setFont(label_font)
            self.phone_v.setReadOnly(True)
            self.phone_v.setStyleSheet(
                "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

            self.date = QtWidgets.QLabel(self)
            self.date.setGeometry(20, 105, 120, 30)
            self.date.setText("DATE & TIME :")
            self.date.setFont(label_font)
            self.date.setStyleSheet("background: transparent; color: white;")

            self.date_v = QtWidgets.QLineEdit(self)
            self.date_v.setGeometry(130, 105, 180, 30)
            self.date_v.setFont(label_font)
            self.date_v.setReadOnly(True)
            self.date_v.setStyleSheet(
                "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

            self.items = QtWidgets.QLabel(self)
            self.items.setGeometry(330, 105, 130, 30)
            self.items.setText("NO. OF ITEMS :")
            self.items.setFont(label_font)
            self.items.setStyleSheet("background: transparent; color: white;")

            self.t_items = QtWidgets.QLineEdit(self)
            self.t_items.setGeometry(450, 105, 50, 30)
            self.t_items.setFont(label_font)
            self.t_items.setReadOnly(True)
            self.t_items.setStyleSheet(
                "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

            self.total = QtWidgets.QLabel(self)
            self.total.setGeometry(20, 150, 110, 30)
            self.total.setText("TOTAL AMT :")
            self.total.setFont(label_font)
            self.total.setStyleSheet("background: transparent; color: white;")

            self.total_amt = QtWidgets.QLineEdit(self)
            self.total_amt.setGeometry(120, 150, 100, 30)
            self.total_amt.setFont(label_font)
            self.total_amt.setStyleSheet(
                "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")
            self.total_amt.setReadOnly(True)

            self.confirm = QtWidgets.QPushButton(self)
            self.confirm.setText("CONFIRM")
            self.confirm.setGeometry(260, 150, 100, 30)
            self.confirm.setFont(label_font)
            self.confirm.clicked.connect(self.details)
            self.confirm.setStyleSheet("background: rgba(0, 0, 0, 150); color: white; border: none;")

            self.bill_table = QtWidgets.QTableWidget(self)
            self.bill_table.setColumnCount(4)
            self.bill_table.setHorizontalHeaderLabels(["ITEM NAME", "QTY", "AMT", "TOTAL"])
            self.bill_table.setGeometry(120, 200, 345, 400)
            self.bill_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.bill_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            self.bill_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.bill_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.bill_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.bill_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.bill_table.setStyleSheet("""
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
            self.bill_table.setAttribute(Qt.WA_TranslucentBackground)
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return

    def details(self):
        self.value = self.num.text()
        try:
            if not self.value:
                QtWidgets.QMessageBox.warning(self, "Error", "PLEASE ENTER ORDER ID")
                return

            self.cursor.execute('SELECT MAX(order_id) FROM food_txn')
            value = self.cursor.fetchone()

            if int(self.value) <= (value[0]):
                try:
                    cust_name = "SELECT distinct(cust_name) From food_txn WHERE order_id = %s"
                    self.cursor.execute(cust_name, (self.value,))
                    result1 = self.cursor.fetchone()

                    if result1:
                        self.cust_v.setText(result1[0])

                    cust_num = "SELECT distinct(cust_phone) From food_txn WHERE order_id = %s"
                    self.cursor.execute(cust_num, (self.value,))
                    result2 = self.cursor.fetchone()

                    if result2:
                        self.phone_v.setText(result2[0])

                    date = "SELECT distinct(date_txn) From food_txn WHERE order_id = %s"
                    self.cursor.execute(date, (self.value,))
                    result3 = self.cursor.fetchone()

                    if result3:
                        self.date_v.setText(str(result3[0]))

                    qty = "SELECT sum(qty) From food_txn WHERE order_id = %s"
                    self.cursor.execute(qty, (self.value,))
                    result4 = self.cursor.fetchone()

                    if result4:
                        self.t_items.setText(str(int(result4[0])))

                    amt = "SELECT sum(total) From food_txn WHERE order_id = %s"
                    self.cursor.execute(amt, (self.value,))
                    result5 = self.cursor.fetchone()

                    if result5:
                        self.total_amt.setText(str(int(result5[0])))

                    content = "SELECT item_name, qty, price, total From food_txn WHERE order_id = %s"
                    self.cursor.execute(content, (self.value,))
                    rows = self.cursor.fetchall()

                    self.bill_table.setRowCount(len(rows))
                    self.bill_table.setColumnCount(len(rows[0]))

                    for i, row in enumerate(rows):
                        for j, col in enumerate(row):
                            self.bill_table.setItem(i, j, QTableWidgetItem(str(col)))

                except Exception as e:
                    traceback.print_exc()
                    QtWidgets.QMessageBox.warning(self, "Error", str(e))
                    return
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "ORDER ID NOT FOUND")
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()

