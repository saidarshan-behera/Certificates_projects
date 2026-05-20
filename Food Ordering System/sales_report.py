import os
import sys
import traceback
import matplotlib.pyplot as plt
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtGui
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


class sales(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BILL")

        background_image = resource_path('images/7.jpg')

        background_image_url = background_image.replace("\\", "/")

        self.setStyleSheet(f'background-image: url({background_image_url});')

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
        self.title.setGeometry(530, 10, 380, 30)
        self.title.setText("SALES REPORT")
        self.title.setFont(nextFont)
        self.title.setStyleSheet("background: transparent; color: white;")

        self.day = QtWidgets.QLabel(self)
        self.day.setGeometry(130, 60, 70, 30)
        self.day.setText("DAYS:")
        self.day.setFont(label_font)
        self.day.setStyleSheet("background: transparent; color: white;")

        self.dname = QtWidgets.QComboBox(self)
        self.dname.setGeometry(180, 65, 161, 25)
        self.dname.setFont(label_font)
        self.dname.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")
        self.dname.addItems(
            ["ALL DAYS", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"])

        self.month = QtWidgets.QLabel(self)
        self.month.setGeometry(350, 60, 70, 30)
        self.month.setText("MONTH :")
        self.month.setFont(label_font)
        self.month.setStyleSheet("background: transparent; color: white;")

        self.mname = QtWidgets.QComboBox(self)
        self.mname.setGeometry(420, 65, 161, 25)
        self.mname.setFont(label_font)
        self.mname.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")
        self.mname.addItems(
            ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
             "NOVEMBER", "DECEMBER"])

        self.year = QtWidgets.QLabel(self)
        self.year.setGeometry(590, 60, 70, 30)
        self.year.setText("YEAR:")
        self.year.setFont(label_font)
        self.year.setStyleSheet("background: transparent; color: white;")

        self.yname = QtWidgets.QComboBox(self)
        self.yname.setGeometry(642, 65, 161, 25)
        self.yname.setFont(label_font)
        self.yname.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")
        self.yname.addItems(
            ["2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2032"])

        self.cat = QtWidgets.QLabel(self)
        self.cat.setGeometry(810, 60, 90, 30)
        self.cat.setText("CATEGORY:")
        self.cat.setFont(label_font)
        self.cat.setStyleSheet("background: transparent; color: white;")

        self.iname = QtWidgets.QComboBox(self)
        self.iname.setGeometry(903, 65, 161, 25)
        self.iname.setFont(label_font)
        self.iname.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")
        self.iname.addItems(
            ["ALL ITEMS", "PIZZA", "BURGER", "PASTA", "MOMO", "NOODLES", "COMBOS", "DONUTS",
             "COLD BEVERAGES", "HOT BEVERAGES"])

        self.back = QtWidgets.QPushButton(self)
        self.back.setText("BACK")
        self.back.setGeometry(QRect(1270, 10, 90, 30))
        self.back.setFont(label_font)
        self.back.clicked.connect(self.admin)
        self.back.setStyleSheet("color: white; border: none;")

        self.confirm = QtWidgets.QPushButton(self)
        self.confirm.setText("CONFIRM")
        self.confirm.setGeometry(1080, 65, 100, 25)
        self.confirm.setFont(label_font)
        self.confirm.clicked.connect(self.report)
        self.confirm.setStyleSheet("color: white; border: r;")

        self.item_table = QtWidgets.QTableWidget(self)
        self.item_table.setColumnCount(3)
        self.item_table.setHorizontalHeaderLabels(["ITEM NAME", "QTY", "TOTAL"])
        self.item_table.setGeometry(60, 120, 422, 530)
        self.item_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.item_table.setStyleSheet("""
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
        self.item_table.setAttribute(Qt.WA_TranslucentBackground)

        self.item_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.item_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.item_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.graph_layout = QtWidgets.QLabel(self)
        self.graph_layout.setGeometry(590, 120, 0, 0)
        self.graph_layout.setStyleSheet(
            "background: transparent; border: 1px solid rgba(255, 255, 255, 200); color: white; padding: 5px;")

        self.showMaximized()

    def report(self):
        if self.iname.currentText() != "ALL ITEMS":
            if self.dname.currentText() == "ALL DAYS":
                self.monthly()
            else:
                self.weekly()
        if self.iname.currentText() == "ALL ITEMS":
            self.category_wise_sales()

    def category_wise_sales(self):
        try:
            month_index = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            month = month_index[self.mname.currentIndex()]
            year = self.yname.currentText()
            day = self.dname.currentText()
            value = str(year) + "-" + str(month)

            if day == "ALL DAYS":
                content = """
                    SELECT i.category AS Category, SUM(f.qty) AS Quantity, SUM(f.qty * f.total) AS Total
                    FROM food_txn f
                    JOIN items i ON f.item_name = i.iname
                    WHERE LEFT(f.date_txn,7) = %s
                    GROUP BY i.category
                    ORDER BY SUM(f.qty) DESC
                """
                self.cursor.execute(content, (value,))
            else:
                content = """
                    SELECT i.category AS Category, SUM(f.qty) AS Quantity, SUM(f.qty * f.total) AS Total
                    FROM food_txn f
                    JOIN items i ON f.item_name = i.iname
                    WHERE LEFT(f.date_txn,7) = %s AND DAYNAME(f.date_txn) = %s
                    GROUP BY i.category
                    ORDER BY SUM(f.qty) DESC
                """
                self.cursor.execute(content, (value, day,))

            rows = self.cursor.fetchall()

            self.item_table.setRowCount(len(rows))
            self.item_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.item_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.item_table.setRowCount(len(rows))
            self.item_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.item_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.item_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.item_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.item_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

            categories = []
            qty_sold = []

            for row in rows:
                categories.append(row[0])
                qty_sold.append(int(row[1]))

            plt.clf()
            plt.pie(qty_sold, labels=categories, autopct='%1.1f%%', startangle=90)
            plt.title(f'SALES REPORT FOR CATEGORIES ({self.mname.currentText()}) {year}')

            file_name = f'category_sales_{self.mname.currentText()}_{year}.png'
            plt.savefig(file_name, transparent=True)

            pixmap = QPixmap(file_name)

            if not pixmap.isNull():
                self.graph_layout.setPixmap(pixmap)
                self.graph_layout.setFixedSize(pixmap.size())
                self.graph_layout.setStyleSheet("border: 2px solid white; background: transparent;")
            else:
                self.graph_layout.setStyleSheet("")

            categories = []
            qty_sold = []

        except Exception as e:
            traceback.print_exc()
            self.graph_layout.clear()
            self.graph_layout.setStyleSheet('background: transparent')

            QtWidgets.QMessageBox.warning(self, "No content", str(e))
            return

    def monthly(self):
        try:
            month_index = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            month = month_index[self.mname.currentIndex()]
            year = self.yname.currentText()
            cat = self.iname.currentText()
            value = str(year) + "-" + str(month)

            content = "SELECT i.iname as Item,SUM(f.qty) AS Quantity,SUM(f.qty * f.total) AS Total FROM food_txn f JOIN items i ON f.item_name = i.iname WHERE left(f.date_txn,7) = %s AND i.category = %s GROUP BY i.iname ORDER BY SUM(f.qty) asc"
            self.cursor.execute(content, (value, cat,))
            rows = self.cursor.fetchall()

            self.item_table.setRowCount(len(rows))
            self.item_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.item_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.item_table.setRowCount(len(rows))
            self.item_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.item_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.item_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.item_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.item_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.items = []
            self.qty_sold = []

            row_count = self.item_table.rowCount()
            for row in range(row_count):
                item = self.item_table.item(row, 0)
                if item is not None:
                    self.items.append(item.text())

            for row in range(row_count):
                item = self.item_table.item(row, 1)
                if item is not None:
                    self.qty_sold.append(int(item.text()))

            plt.clf()

            plt.pie(self.qty_sold, labels=self.items, autopct='%1.1f%%', startangle=90)
            plt.title(
                f'SALES REPORT FOR THE MONTH {self.mname.currentText()}, {year} FOR ITEM {self.iname.currentText().upper()}')

            file_name = f'{self.mname.currentText()}_{year}.png'

            plt.savefig(file_name, transparent=True)

            pixmap = QPixmap(file_name)

            if not pixmap.isNull():
                self.graph_layout.setPixmap(pixmap)

                self.graph_layout.setFixedSize(pixmap.size())

                self.graph_layout.setStyleSheet("border: 2px solid white; background: transparent;")

            else:
                self.graph_layout.setStyleSheet("")

            self.items = []
            self.qty_sold = []

        except Exception as e:
            traceback.print_exc()
            self.graph_layout.clear()
            self.graph_layout.setStyleSheet('background: transparent')

            QtWidgets.QMessageBox.warning(self, "No content", str(e))
            return

    def weekly(self):
        try:
            month_index = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            month = month_index[self.mname.currentIndex()]
            year = self.yname.currentText()
            cat = self.iname.currentText()
            day = self.dname.currentText()
            value = str(year) + "-" + str(month)

            content = "SELECT i.iname as Item,SUM(f.qty) AS Quantity,SUM(f.qty * f.total) AS Total FROM food_txn f JOIN items i ON f.item_name = i.iname WHERE left(f.date_txn,7) = %s AND DAYNAME(date_txn) = %s AND i.category = %s GROUP BY i.iname ORDER BY SUM(f.qty) asc"
            self.cursor.execute(content, (value, day, cat,))
            rows = self.cursor.fetchall()

            self.item_table.setRowCount(len(rows))
            self.item_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.item_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.item_table.setRowCount(len(rows))
            self.item_table.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    self.item_table.setItem(i, j, QTableWidgetItem(str(col)))

            self.item_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.item_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.item_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

            self.items = []
            self.qty_sold = []

            row_count = self.item_table.rowCount()
            for row in range(row_count):
                item = self.item_table.item(row, 0)
                if item is not None:
                    self.items.append(item.text())

            for row in range(row_count):
                item = self.item_table.item(row, 1)
                if item is not None:
                    self.qty_sold.append(item.text())

            plt.clf()

            plt.pie(self.qty_sold, labels=self.items, autopct='%1.1f%%', startangle=45)
            plt.title(f'SALES REPORT FOR THE DAY {self.dname.currentText()} FOR {self.mname.currentText()},{year}')

            plt.savefig(f'{self.dname.currentText()}_{self.mname.currentText()}_{year}.png', transparent=True)

            pixmap = QPixmap(f'{self.dname.currentText()}_{self.mname.currentText()}_{year}.png')
            self.graph_layout.setPixmap(pixmap)

            if not pixmap.isNull():
                self.graph_layout.setPixmap(pixmap)

                self.graph_layout.setFixedSize(pixmap.size())

                self.graph_layout.setStyleSheet("border: 2px solid white; background: transparent;")

            else:
                self.graph_layout.setStyleSheet("")

            self.items = []
            self.qty_sold = []
        except Exception as e:
            traceback.print_exc()
            self.graph_layout.clear()
            self.graph_layout.setStyleSheet('background: transparent')

            QtWidgets.QMessageBox.warning(self, "No items", str(e))
            return

    def admin(self):
        import admin_page
        self.s = admin_page.Admin()
        self.s.show()
        self.destroy()

