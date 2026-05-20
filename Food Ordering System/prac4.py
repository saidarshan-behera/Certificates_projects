import datetime
import os
import sys
import traceback
import mysql.connector
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QSize, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow, QWidget, QVBoxLayout, QLabel, \
    QPushButton, QListWidget, QListWidgetItem, QScrollArea, QSizePolicy, QDialog, QHeaderView, QSpinBox


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


class FoodItem:
    def __init__(self, name, price, image_path, description):
        self.name = name
        self.price = price
        self.image_path = image_path
        self.description = description


class DataHandler(QObject):
    data_received = pyqtSignal(str, float, int)


class Confirm(QDialog):
    def __init__(self, food_app, parent=None):
        super().__init__(parent)
        self.food_app = food_app

        self.setWindowTitle("Confirmation")
        self.setFixedWidth(590)
        self.setFixedHeight(550)

        background_image = resource_path('images/bg.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')
        cFont = QtGui.QFont()
        cFont.setPointSize(14)
        cFont.setFamily("Acme")
        cFont.setBold(True)

        oFont = QtGui.QFont()
        oFont.setPointSize(14)
        oFont.setFamily("Bahnschrift SemiBold Condensed")
        oFont.setBold(True)

        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )

        self.cursor = self.conn.cursor()

        self.table2 = QtWidgets.QTableWidget(self)
        self.table2.setColumnCount(3)
        self.table2.setHorizontalHeaderLabels(["Items", "Qty", "Rate"])
        self.table2.setGeometry(10, 140, 345, 400)
        self.table2.setFont(QFont("Minion Pro Med", 10))
        self.table2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table2.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.table2.setStyleSheet(""" 
                    QTableWidget { 
                        background-color: transparent; 
                    } 
                    QHeaderView::section { 
                        background-color: transparent;  /* Make headers transparent */ 
                        color: black;                  /* Change header text color to white */ 
                        font-weight: bold;             /* Make header text bold */ 
                    } 
                    QTableWidget::item { 
                        color: black;                  /* Change item text color to white */ 
                        font-weight: bold;           /* Make item text normal weight */
                    }
                """)

        self.table2.setAttribute(Qt.WA_TranslucentBackground)

        self.date_lbl = QtWidgets.QLabel(self)
        self.date_lbl.setText("DATE/TIME:")
        self.date_lbl.setGeometry(20, 15, 130, 30)
        self.date_lbl.setFont(cFont)
        self.date_lbl.setStyleSheet("background: transparent; color: black;")

        self.date_le = QtWidgets.QLineEdit(self)
        self.date_le.setGeometry(145, 15, 340, 30)
        self.date_le.setFont(oFont)
        self.date_le.setReadOnly(True)
        self.date_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.name = QtWidgets.QLabel(self)
        self.name.setGeometry(QtCore.QRect(20, 35, 170, 71))
        self.name.setText("NAME:")
        self.name.setFont(cFont)
        self.name.setStyleSheet("background: transparent; color: black;")

        self.name_lbl = QtWidgets.QLineEdit(self)
        self.name_lbl.setGeometry(QtCore.QRect(145, 55, 340, 30))
        self.name_lbl.setFont(oFont)
        self.name_lbl.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.name = self.name_lbl.text()

        self.num = QtWidgets.QLabel(self)
        self.num.setGeometry(QtCore.QRect(20, 75, 170, 71))
        self.num.setText("PHONE NO.:")
        self.num.setFont(cFont)
        self.num.setStyleSheet("background: transparent; color: black;")

        self.num_lbl = QtWidgets.QLineEdit(self)
        self.num_lbl.setGeometry(QtCore.QRect(145, 95, 340, 30))
        self.num_lbl.setFont(oFont)
        self.num_lbl.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.output = QtWidgets.QLineEdit(self)
        self.output.setGeometry(360, 170, 220, 290)
        self.output.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.ord = QtWidgets.QLabel(self)
        self.ord.setGeometry(QtCore.QRect(370, 170, 210, 71))
        self.ord.setText("ORDER NO.:")
        self.ord.setFont(cFont)
        self.ord.setStyleSheet("background: transparent; color: black;")

        self.ord_lbl = QtWidgets.QLineEdit(self)
        self.ord_lbl.setGeometry(QtCore.QRect(490, 190, 80, 30))
        self.ord_lbl.setFont(oFont)
        self.ord_lbl.setReadOnly(True)
        self.ord_lbl.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.total_lbl = QtWidgets.QLabel(self)
        self.total_lbl.setText("TOTAL:")
        self.total_lbl.setGeometry(370, 235, 160, 30)
        self.total_lbl.setFont(cFont)
        self.total_lbl.setStyleSheet("background: transparent; color: black;")

        self.total_le = QtWidgets.QLineEdit(self)
        self.total_le.setGeometry(445, 235, 125, 30)
        self.total_le.setFont(oFont)
        self.total_le.setReadOnly(True)
        self.total_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.cgst_sgst = QtWidgets.QLabel(self)
        self.cgst_sgst.setGeometry(QtCore.QRect(370, 265, 170, 71))
        self.cgst_sgst.setText("CGST/SGST:")
        self.cgst_sgst.setFont(cFont)
        self.cgst_sgst.setStyleSheet("background: transparent; color: black;")

        self.cgst_sgst_lbl = QtWidgets.QLineEdit(self)
        self.cgst_sgst_lbl.setGeometry(QtCore.QRect(490, 280, 80, 30))
        self.cgst_sgst_lbl.setFont(oFont)
        self.cgst_sgst_lbl.setReadOnly(True)
        self.cgst_sgst_lbl.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.disc = QtWidgets.QLabel(self)
        self.disc.setGeometry(QtCore.QRect(370, 310, 170, 71))
        self.disc.setText("DISCOUNT:")
        self.disc.setFont(cFont)
        self.disc.setStyleSheet("background: transparent; color: black;")

        self.disc_lbl = QtWidgets.QLineEdit(self)
        self.disc_lbl.setGeometry(QtCore.QRect(490, 325, 80, 30))
        self.disc_lbl.setFont(oFont)
        self.disc_lbl.setReadOnly(True)
        self.disc_lbl.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")
        self.update()

        self.total_bill_lbl = QtWidgets.QLabel(self)
        self.total_bill_lbl.setText("TOTAL AMT:")
        self.total_bill_lbl.setGeometry(370, 370, 160, 30)
        self.total_bill_lbl.setFont(cFont)
        self.total_bill_lbl.setStyleSheet("background: transparent; color: black;")

        self.total_bill_le = QtWidgets.QLineEdit(self)
        self.total_bill_le.setGeometry(490, 370, 80, 30)
        self.total_bill_le.setFont(oFont)
        self.total_bill_le.setReadOnly(True)
        self.total_bill_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.itemsSold_lbl = QtWidgets.QLabel(self)
        self.itemsSold_lbl.setText("NO. OF ITEMS:")
        self.itemsSold_lbl.setGeometry(370, 410, 160, 30)
        self.itemsSold_lbl.setFont(cFont)
        self.itemsSold_lbl.setStyleSheet("background: transparent; color: black;")

        self.itemsSold_le = QtWidgets.QLineEdit(self)
        self.itemsSold_le.setGeometry(515, 410, 55, 30)
        self.itemsSold_le.setFont(oFont)
        self.itemsSold_le.setReadOnly(True)
        self.itemsSold_le.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: black; padding: 5px;")

        self.conf = QtWidgets.QPushButton(self)
        self.conf.setGeometry(QtCore.QRect(400, 480, 100, 50))
        self.conf.setText("CONFIRM")
        self.conf.setFont(QFont("Arial Rounded MT Bold", 12))
        self.conf.clicked.connect(self.confirm_action)
        self.conf.setStyleSheet("color: black; border: white;")

        self.back = QtWidgets.QPushButton(self)
        self.back.setText("BACK")
        self.back.setGeometry(510, 5, 70, 35)
        self.back.setFont(QFont("Arial Rounded MT Bold", 12))
        self.back.clicked.connect(self.go_back)
        self.back.setStyleSheet(" color: black; border: white;")

        self.name = []
        self.qty = []
        self.pri = []
        self.total = []
        self.total_qty = 0
        self.item_total = 0

        id = "select max(order_id) from food_txn"
        self.cursor.execute(id)
        re = self.cursor.fetchone()
        self.id = int(re[0]) + 1

        self.current_datetime = datetime.datetime.now()
        self.formatted_datetime = self.current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    def confirm_action(self):
        try:
            for row in range(self.table2.rowCount()):
                item_name = self.table2.item(row, 0).text()
                self.name.append(item_name)

                quantity = int(self.table2.item(row, 1).text())
                self.qty.append(int(quantity))

                price = float(self.table2.item(row, 2).text())
                self.pri.append(int(price))

                total_item_price = quantity * price
                self.total.append(int(total_item_price))

                self.cust = self.name_lbl.text()
                self.phone = self.num_lbl.text()

            self.total_qty = sum(self.qty)

            if self.table2.rowCount() == 0:
                QtWidgets.QMessageBox.warning(self, "ITEM ERROR", "NO ITEMS PLACED IN CART")

            if self.name_lbl.text() == "" or len(self.num_lbl.text()) != 10:
                QtWidgets.QMessageBox.warning(self, "INFORMATION ERROR", "PLEASE FILL THE NECESSARY INFORMATIONS")

            if self.name_lbl.text() != "" and len(self.num_lbl.text()) == 10:
                for i in range(self.table2.rowCount()):
                    self.item_t = int(self.pri[i]) * int(self.qty[i])
                    self.item_total = self.item_t + self.item_t * 0.05 - int(self.pri[i]) * 0.07
                    sql_query = "INSERT INTO food_txn VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        str(self.id), str(self.cust), str(self.phone), str(self.name[i]), str(self.qty[i]),
                        str(self.pri[i]), str(self.item_total), self.formatted_datetime)
                    self.cursor.execute(sql_query)

                    self.conn.commit()

                QtWidgets.QMessageBox.warning(self, 'INSERTED', "ORDER PLACED")
                self.item_total = 0

                self.id += 1

                self.total_le.clear()
                self.cgst_sgst_lbl.clear()
                self.disc_lbl.clear()
                self.ord_lbl.clear()
                self.date_le.clear()
                self.total_bill_le.clear()
                self.itemsSold_le.clear()
                self.table2.setRowCount(0)
                self.name_lbl.clear()
                self.num_lbl.clear()

                self.food_app.order_table.setRowCount(0)

                self.food_app.total_price_label.setText("Total Price: $0.00")
                self.food_app.id += 1

                self.close()
                self.destroy()
                self.food_app.show()

        except Exception as a:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(a))
            return

    def go_back(self):
        self.close()
        self.food_app.show()


class FoodApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FOOD APP")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        background_image = resource_path('images/bg.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

        self.category_list = QListWidget(self.central_widget)
        categories = ["Pizza", "Burger", "Pasta", "Momo", "Noodles", "Combos", "Donuts", "Cold Beverages",
                      "Hot Beverages"]
        for cat in categories:
            item = QListWidgetItem(cat)
            self.category_list.addItem(item)
            item.setSizeHint(QSize(100, 50))
        self.category_list.setFont(QFont("Cracked Johnnie", 12))
        self.category_list.setGeometry(QRect(20, 50, 230, 650))

        self.cat = QLabel(self)
        self.cat.setText("CATEGORY")
        self.cat.setFont(QFont("Distant Galaxy", 20))
        self.cat.setGeometry(70, 20, 150, 30)
        self.cat.setStyleSheet("background: transparent; color: black;")

        self.category_list.currentRowChanged.connect(self.show_items)

        self.menu_items = []

        self.menu_area = QScrollArea(self.central_widget)
        self.menu_area.setWidgetResizable(True)
        self.menu_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.menu_area.setGeometry(QRect(270, 50, 600, 650))
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_area.setWidget(self.menu_widget)
        self.menu_area.verticalScrollBar().setValue(0)

        self.menu = QLabel(self)
        self.menu.setText("MENU")
        self.menu.setFont(QFont("Distant Galaxy", 20))
        self.menu.setGeometry(520, 20, 150, 30)
        self.menu.setStyleSheet("background: transparent; color: black;")

        self.order_scroll_area = QScrollArea(self.central_widget)
        self.order_scroll_area.setWidgetResizable(True)
        self.order_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.order_scroll_area.setGeometry(QRect(890, 50, 450, 650))
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Item", "Price", "Quantity", "Total", "Remove"])
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)
        self.order_table.setFont(QFont("Minion Pro Med", 10))
        self.order_scroll_area.setWidget(self.order_table)

        self.order_table.setStyleSheet(""" 
                            QTableWidget { 
                                background-color: transparent; 
                            } 
                            QHeaderView::section { 
                                background-color: transparent;  /* Make headers transparent */ 
                                color: black;                  /* Change header text color to white */ 
                                font-weight: bold;             /* Make header text bold */ 
                            } 
                            QTableWidget::item { 
                                color: black;                  /* Change item text color to white */ 
                                font-weight: bold;           /* Make item text normal weight */
                            }
                        """)

        self.order_table.setAttribute(Qt.WA_TranslucentBackground)

        self.order_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.order_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.order_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.order_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.order_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.order = QLabel(self)
        self.order.setText("ORDER TABLE")
        self.order.setFont(QFont("Distant Galaxy", 20))
        self.order.setGeometry(1000, 20, 200, 30)
        self.order.setStyleSheet("background: transparent; color: black;")

        self.total_price_label = QLabel("Total Price: $0.00", self.central_widget)
        self.total_price_label.setFont(QFont("Borealis", 11))
        self.total_price_label.setGeometry(QRect(900, 700, 500, 30))
        self.total_price_label.setStyleSheet("background: transparent; color: black;")

        self.proceed_button = QPushButton("PROCEED", self.central_widget)
        self.proceed_button.setGeometry(QRect(1100, 702, 100, 30))
        self.proceed_button.clicked.connect(self.proceed_to_confirm)
        self.proceed_button.setFont(QFont("Arial Rounded MT Bold", 10))
        self.proceed_button.setStyleSheet(" color: black; border: white;")

        self.logout_button = QPushButton("LOGOUT↪", self.central_widget)
        self.logout_button.setGeometry(QRect(1270, 10, 90, 30))
        self.logout_button.clicked.connect(self.logout_action)
        self.logout_button.setFont(QFont("Arial Rounded MT Bold", 10))
        self.logout_button.setStyleSheet(" color: black; border: white;")

        self.total_price = 0.0
        self.update_total_price()

        self.data_handler = DataHandler()
        self.data_handler.data_received.connect(self.receive_data)

        self.name = []
        self.qty = []
        self.pri = []
        self.total = []
        self.id = 0
        self.total_qty = 0

        self.current_datetime = datetime.datetime.now()
        self.formatted_datetime = self.current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )

        self.cursor = self.conn.cursor()

        self.showMaximized()

    def logout_action(self):
        import Login
        self.s = Login.Login()
        self.s.show()
        self.destroy()

    def load_image(self, image_path):
        with open(image_path, 'rb') as file:
            image_data = file.read()
        self.pic = QtGui.QPixmap()
        self.pic.loadFromData(image_data)
        self.path.setPixmap(self.pic)

    def show_items(self, index):
        global image_path
        for i in reversed(range(self.menu_layout.count())):
            self.menu_layout.itemAt(i).widget().deleteLater()

        self.menu_items = []

        if index == 0:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "pizza"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 1:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "burger"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 2:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "pasta"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 3:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "momo"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 4:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "noodles"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 5:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "combos"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 6:
            try:
                self.cursor.execute('SELECT iname, amt, image_path, description FROM items WHERE category = "donuts"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 7:
            try:
                self.cursor.execute(
                    'SELECT iname, amt, image_path, description FROM items WHERE category = "cold beverages"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        if index == 8:
            try:
                self.cursor.execute(
                    'SELECT iname, amt, image_path, description FROM items WHERE category = "hot beverages"')
                data = self.cursor.fetchall()

                for row in range(len(data)):
                    name = data[row][0]
                    price = data[row][1]
                    image_path = data[row][2]
                    description = data[row][3]

                    food_item = FoodItem(name, price, image_path, description)
                    self.menu_items.append(food_item)

            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return

        try:
            for item in self.menu_items:
                item_widget = QWidget()
                item_layout = QVBoxLayout()
                item_widget.setLayout(item_layout)

                label = QLabel(f"{item.name} - ₹{item.price:}")
                label.setFont(QFont("Candles", 15))
                label.setStyleSheet("background: transparent; color: black;")

                item_layout.addWidget(label)

                if item.description:
                    description_label = QLabel(item.description)
                    description_label.setFont(QFont("Ink Free", 12))
                    description_label.setWordWrap(True)
                    description_label.setStyleSheet("background: transparent; color: black; font-weight:bold")
                    item_layout.addWidget(description_label)

                if item.image_path:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(item.image_path)

                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    image_label.setStyleSheet("background: transparent; color: black;")

                    item_layout.addWidget(image_label)

                add_button = QPushButton("Add to Order")
                add_button.setFont(QFont("Arial Rounded MT Bold", 10))
                add_button.clicked.connect(lambda _, i=item: self.add_to_order(i))
                item_layout.addWidget(add_button)

                item_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.menu_layout.addWidget(item_widget)

                self.menu_area.verticalScrollBar().setValue(0)
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return

    def add_to_order(self, item):
        try:
            for row in range(self.order_table.rowCount()):
                existing_item_name = self.order_table.item(row, 0).text()
                if existing_item_name == item.name:
                    quantity_spinbox = self.order_table.cellWidget(row, 2)

                    if quantity_spinbox:
                        new_quantity = quantity_spinbox.value() + 1
                        quantity_spinbox.setValue(new_quantity)
                        self.update_row_total(row)
                        return

            row_position = self.order_table.rowCount()
            self.order_table.insertRow(row_position)

            self.order_table.setItem(row_position, 0, QTableWidgetItem(item.name))
            self.order_table.setItem(row_position, 1, QTableWidgetItem(str(item.price)))

            quantity_spinbox = QSpinBox()
            quantity_spinbox.setMinimum(1)
            quantity_spinbox.setMaximum(100)
            quantity_spinbox.setValue(1)
            quantity_spinbox.setStyleSheet(" color: black; border: white;")

            self.order_table.setCellWidget(row_position, 2, quantity_spinbox)

            total_price_item = QTableWidgetItem(str(item.price))
            self.order_table.setItem(row_position, 3, total_price_item)

            remove_button = QPushButton("REMOVE")
            remove_button.setFont(QFont("Arial Rounded MT Bold", 10))
            remove_button.setStyleSheet("color: black; border: white;")
            self.order_table.setCellWidget(row_position, 4, remove_button)

            remove_button.clicked.connect(lambda _, r=row_position: self.remove_row())

            quantity_spinbox.valueChanged.connect(lambda _, r=row_position: self.update_row_total(r))

            self.order_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.order_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.order_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.update_total_price()

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))

    def update_row_total(self, row):
        try:
            quantity = float(self.order_table.cellWidget(row, 2).value())
            price = float(self.order_table.item(row, 1).text())
            total = quantity * price
            self.order_table.item(row, 3).setText(f"{total:.2f}")
            self.update_total_price()

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))

    def remove_row(self):
        try:
            cur_row = self.order_table.currentRow()

            self.order_table.removeRow(cur_row)

            price_item = self.order_table.item(cur_row, 1)
            quantity_item = self.order_table.cellWidget(cur_row, 2)
            self.update_total_price()

            if price_item and quantity_item:
                price = float(price_item.text())
                quantity = float(quantity_item.value())

                self.total_price -= price * quantity

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return

    def update_total_price(self):
        try:
            if self.order_table.rowCount() == 0:
                self.total_price_label.setText("Total Price: ₹0")
                return
            total_price = 0
            for row in range(self.order_table.rowCount()):
                total_price += float(self.order_table.item(row, 3).text())
            self.total_price_label.setText(f"Total Price: ₹{total_price}")
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return

    def receive_data(self, item_name, price, quantity):
        for row in range(self.order_table.rowCount()):
            if self.order_table.item(row, 0).text() == item_name:
                current_quantity = int(self.order_table.item(row, 2).text())
                new_quantity = current_quantity + quantity
                total_price = new_quantity * price
                self.order_table.setItem(row, 2, QTableWidgetItem(str(new_quantity)))
                self.order_table.setItem(row, 3, QTableWidgetItem(str(total_price)))
                self.update_total_price()
                return

        row_position = self.order_table.rowCount()
        self.order_table.insertRow(row_position)
        self.order_table.setItem(row_position, 0, QTableWidgetItem(item_name))
        self.order_table.setItem(row_position, 1, QTableWidgetItem(str(price)))
        self.order_table.setItem(row_position, 2, QTableWidgetItem(str(quantity)))
        self.order_table.setItem(row_position, 3, QTableWidgetItem(str(price * quantity)))
        self.update_total_price()

    def proceed_to_confirm(self):
        confirm_dialog = Confirm(self)
        print("procedding to confirm", confirm_dialog)

        row_count = self.order_table.rowCount()
        confirm_dialog.table2.setRowCount(row_count)

        for row in range(row_count):
            if int(self.order_table.cellWidget(row, 2).value()) > 0:
                item_name = self.order_table.item(row, 0).text()
                price = float(self.order_table.item(row, 1).text())
                quantity = int(self.order_table.cellWidget(row, 2).value())

                confirm_dialog.table2.setItem(row, 0, QTableWidgetItem(item_name))
                confirm_dialog.table2.setItem(row, 1, QTableWidgetItem(str(quantity)))
                confirm_dialog.table2.setItem(row, 2, QTableWidgetItem(f"{price:.2f}"))
                confirm_dialog.table2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
                confirm_dialog.table2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
                confirm_dialog.table2.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.name = []
        self.qty = []
        self.pri = []
        self.total = []

        try:
            for row in range(confirm_dialog.table2.rowCount()):
                item_name = confirm_dialog.table2.item(row, 0).text()
                self.name.append(item_name)

                quantity = int(confirm_dialog.table2.item(row, 1).text())
                self.qty.append(quantity)

                price = float(confirm_dialog.table2.item(row, 2).text())
                self.pri.append(price)

                total_item_price = quantity * price
                self.total.append(total_item_price)

            id_query = "SELECT MAX(order_id) FROM food_txn"
            self.cursor.execute(id_query)
            re = self.cursor.fetchone()
            self.id = int(re[0]) + 1

            self.random = confirm_dialog.id

            total_amount = sum(self.total)
            cgst_sgst = (total_amount * 0.05)
            discount = round(total_amount * 0.07)
            total_gst = cgst_sgst

            self.total_qty = sum(self.qty)

            total_amt = total_amount + total_gst - discount

            confirm_dialog.total_le.setText(f"{total_amount:.2f}")
            confirm_dialog.cgst_sgst_lbl.setText(f"{cgst_sgst:.2f}")
            confirm_dialog.disc_lbl.setText(f"{discount:.2f}")
            confirm_dialog.ord_lbl.setText(str(self.random))
            confirm_dialog.date_le.setText(self.formatted_datetime)
            confirm_dialog.total_bill_le.setText(f"{total_amt:.2f}")
            confirm_dialog.itemsSold_le.setText(str(self.total_qty))

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return
        self.close()
        confirm_dialog.exec_()


