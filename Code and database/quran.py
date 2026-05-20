import sys
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QSizePolicy,
    QHBoxLayout,
    QDialog,
    QMessageBox, QHeaderView
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QSize
import mysql.connector
import datetime



class FoodItem:
    def __init__(self, name, price, image_path, description):
        self.name = name
        self.price = price
        self.image_path = image_path
        self.description = description


class DataHandler(QObject):
    data_received = pyqtSignal(str, float, int)

    def receive_data(self, item_name, price, quantity):
        print("Received data:", item_name, price, quantity)


class Confirm(QDialog):
    def __init__(self, food_app, parent=None):
        super().__init__(parent)
        self.food_app = food_app
        self.message = ""

        self.setWindowTitle("Confirmation")
        self.setFixedWidth(580)
        self.setFixedHeight(600)

        layout = QVBoxLayout()

        cFont = QtGui.QFont()
        cFont.setPointSize(14)
        cFont.setFamily("18th Century")

        oFont = QtGui.QFont()
        oFont.setPointSize(14)
        oFont.setFamily("18th Century")

        # Initialize MySQL connection
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="sairam",
            database="project"
        )

        # Creating a cursor object
        self.cursor = self.conn.cursor()

        self.table2 = QtWidgets.QTableWidget(self)
        self.table2.setRowCount(90)
        self.table2.setColumnCount(3)
        self.table2.setHorizontalHeaderLabels(["Items", "Qty", "Rate"])
        self.table2.setGeometry(10, 190, 345, 400)
        self.table2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.date_lbl = QtWidgets.QLabel(self)
        self.date_lbl.setText("DATE/TIME:")
        self.date_lbl.setGeometry(20, 65, 110, 30)
        self.date_lbl.setFont(oFont)
        self.date_le = QtWidgets.QLineEdit(self)
        self.date_le.setGeometry(130, 65, 185, 30)
        self.date_le.setFont(oFont)

        self.name = QtWidgets.QLabel(self)
        self.name.setGeometry(QtCore.QRect(20, 85, 170, 71))
        self.name.setText("NAME:")
        self.name.setFont(cFont)
        self.name_lbl = QtWidgets.QLineEdit(self)
        self.name_lbl.setGeometry(QtCore.QRect(85, 105, 200, 30))
        self.name_lbl.setFont(oFont)

        self.name = self.name_lbl.text()
        print(self.name)

        self.num = QtWidgets.QLabel(self)
        self.num.setGeometry(QtCore.QRect(20, 125, 170, 71))
        self.num.setText("PHONE NO.:")
        self.num.setFont(cFont)
        self.num_lbl = QtWidgets.QLineEdit(self)
        self.num_lbl.setGeometry(QtCore.QRect(135, 145, 200, 30))
        self.num_lbl.setFont(oFont)

        self.output = QtWidgets.QLineEdit(self)
        self.output.setGeometry(360, 210, 200, 320)

        self.ord = QtWidgets.QLabel(self)
        self.ord.setGeometry(QtCore.QRect(370, 205, 170, 71))
        self.ord.setText("ORDER NO.:")
        self.ord.setFont(cFont)
        self.ord_lbl = QtWidgets.QLineEdit(self)
        self.ord_lbl.setGeometry(QtCore.QRect(480, 220, 60, 30))
        self.ord_lbl.setFont(oFont)

        self.total_lbl = QtWidgets.QLabel(self)
        self.total_lbl.setText("TOTAL:")
        self.total_lbl.setGeometry(370, 270, 160, 30)
        self.total_lbl.setFont(oFont)
        self.total_le = QtWidgets.QLineEdit(self)
        self.total_le.setGeometry(435, 270, 110, 30)
        self.total_le.setFont(oFont)

        self.cgst_sgst = QtWidgets.QLabel(self)
        self.cgst_sgst.setGeometry(QtCore.QRect(370, 300, 170, 71))
        self.cgst_sgst.setText("CGST/SGST:")
        self.cgst_sgst.setFont(cFont)
        self.cgst_sgst_lbl = QtWidgets.QLineEdit(self)
        self.cgst_sgst_lbl.setGeometry(QtCore.QRect(480, 320, 75, 30))
        self.cgst_sgst_lbl.setFont(oFont)

        self.disc = QtWidgets.QLabel(self)
        self.disc.setGeometry(QtCore.QRect(370, 350, 170, 71))
        self.disc.setText("DISCOUNT:")
        self.disc.setFont(cFont)
        self.disc_lbl = QtWidgets.QLineEdit(self)
        self.disc_lbl.setGeometry(QtCore.QRect(470, 370, 80, 30))
        self.disc_lbl.setFont(oFont)
        self.update()

        self.total_bill_lbl = QtWidgets.QLabel(self)
        self.total_bill_lbl.setText("TOTAL AMT:")
        self.total_bill_lbl.setGeometry(365, 420, 160, 30)
        self.total_bill_lbl.setFont(oFont)
        self.total_bill_le = QtWidgets.QLineEdit(self)
        self.total_bill_le.setGeometry(470, 420, 80, 30)
        self.total_bill_le.setFont(oFont)

        self.itemsSold_lbl = QtWidgets.QLabel(self)
        self.itemsSold_lbl.setText("NO. OF ITEMS:")
        self.itemsSold_lbl.setGeometry(370, 470, 160, 30)
        self.itemsSold_lbl.setFont(oFont)
        self.itemsSold_le = QtWidgets.QLineEdit(self)
        self.itemsSold_le.setGeometry(505, 470, 50, 30)
        self.itemsSold_le.setFont(oFont)

        self.conf = QtWidgets.QPushButton(self)
        self.conf.setGeometry(QtCore.QRect(400, 540, 100, 50))
        self.conf.setText("CONFIRM")
        self.conf.setFont(cFont)
        self.conf.clicked.connect(self.confirm_action)

        self.back = QtWidgets.QPushButton(self)
        self.back.setText("BACK")
        self.back.setGeometry(525, 5, 50, 35)
        self.back.setFont(cFont)
        self.back.clicked.connect(self.go_back)

    def confirm_action(self):
        try:
            # Get data from table2
            for row in range(self.table2.rowCount()):
                item_name = self.table2.item(row, 0).text()
                quantity = int(self.table2.item(row, 1).text())
                price = float(self.table2.item(row, 2).text())
                total_item_price = quantity * price

                # Calculate CGST, SGST, and discount
                cgst = sgst = (total_item_price * 0.05) / 2
                discount = round((total_item_price * 0.07))
                total_gst = cgst + sgst

                # Total bill amount
                total_amt = total_item_price + total_gst - discount

                # Get the current datetime
                current_datetime = datetime.datetime.now()

                # Format the datetime as a string in the MySQL format (YYYY-MM-DD HH:MM:SS)
                formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

                self.message += f"{item_name}: Quantity {quantity}: price{price}:Total = {total_amt} : gst{total_gst}: disc{discount} \n"
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Total Calculation")
                msg_box.setText(self.message)
                msg_box.exec_()

                # Insert data into the database
                sql_query = "INSERT INTO food_txn VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                     str(item_name), str(quantity), str(price), str(quantity * price),formatted_datetime
                )
                self.cursor.execute(sql_query) 

                # Commit the changes
                self.conn.commit()
                print("Data successfully inserted into the database.")

                # Close the cursor and connection
                self.cursor.close()
                self.conn.close()

                self.total_le.setText(str(total_amt))
                self.cgst_sgst_lbl.setText(str(total_gst))
                self.disc_lbl.setText(str(discount))

            self.accept()

        except mysql.connector.Error as err:
            print("MySQL Error:", err.msg)

    def go_back(self):
        self.close()
        self.food_app.show()


class FoodApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Food Ordering System")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Item categories list
        self.category_list = QListWidget()
        categories = ["Pizza", "Burger", "Pasta", "Momo", "Noodles", "Combos", "Donuts", "Cold Beverages",
                      "Hot Beverages"]
        for cat in categories:
            item = QListWidgetItem(cat)
            self.category_list.addItem(item)
            item.setSizeHint(QSize(100, 50))  # Set the size of each item
        self.category_list.setFont(QFont("Arial", 12))  # Change font and size
        self.layout.addWidget(self.category_list)

        # Connect signals
        self.category_list.currentRowChanged.connect(self.show_items)

        # Initialize menu_items
        self.menu_items = []

        # Items under selected category
        self.menu_area = QScrollArea()
        self.menu_area.setWidgetResizable(True)
        self.menu_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_area.setWidget(self.menu_widget)
        self.menu_area.verticalScrollBar().setValue(0)
        self.layout.addWidget(self.menu_area)

        # Ordered items table
        self.order_scroll_area = QScrollArea()
        self.order_scroll_area.setWidgetResizable(True)
        self.order_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Item", "Price", "Quantity", "Total", "Remove"])
        self.order_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Resize columns to contents

        self.order_scroll_area.setWidget(self.order_table)
        self.layout.addWidget(self.order_scroll_area)

        # Total price label
        self.total_price_label = QLabel()
        self.total_price_label.setFont(QFont("Arial", 12))  # Change font and size
        self.layout.addWidget(self.total_price_label)

        # Set layout for central widget
        self.central_widget.setLayout(self.layout)

        # Initialize total price
        self.total_price = 0.0
        self.update_total_price()

        # Initialize data handler
        self.data_handler = DataHandler()
        # Connect signal to the data handler
        self.data_handler.data_received.connect(self.receive_data)

        # Connect signal to quantity cell editing event
        self.order_table.itemChanged.connect(self.update_total_price_from_quantity)

        # "PROCEED" button
        self.proceed_button = QPushButton("PROCEED")
        self.proceed_button.clicked.connect(self.proceed_to_confirm)
        self.layout.addWidget(self.proceed_button, alignment=Qt.AlignBottom)

        # Logout Button
        self.logout_button = QPushButton("LOGOUT↪")
        self.logout_button.clicked.connect(self.logout_action)
        self.layout.addWidget(self.logout_button, alignment=Qt.AlignTop)

    def logout_action(self):
        # Implement the functionality for the logout button here
        pass

    def show_items(self, index):
        # Clear previous items
        for i in reversed(range(self.menu_layout.count())):
            self.menu_layout.itemAt(i).widget().deleteLater()

        self.menu_items = []  # Initialize menu_items

        # Item list
        if index == 0:
            self.menu_items = [
                FoodItem("Cosmic Crunch Pizza", 1100, "p1.jpg",
                         "A thin crust pizza topped with colorful bell peppers, red onions, mushrooms and a sprinkle of crunchy breadcrumbs."),

                FoodItem("Mediterranean Marvel Pizza", 1300, "p2.jpg",
                         "A round pizza with a golden crust, topped with creamy feta cheese, kalamata olives, sun-dried tomatoes, artichoke hearts, and fresh basil leaves."),

                FoodItem("Garden Fiesta Pizza", 1000, "p3.jpg",
                         "A veggie-packed pizza featuring a whole wheat crust topped with vibrant cherry tomatoes, spinach, sweet corn, red bell peppers, and sliced jalapeños for a kick."),

                FoodItem("Spicy Samurai Pizza", 1200, "p4.jpg",
                         " A fiery pizza with a spicy tomato sauce base topped with slices of spicy pepperoni, chunks of grilled mushrooms, red chili flakes, jalapeños, and drizzled with sriracha sauce."),

                FoodItem("Enchanted Forest Pizza", 1300, "p5.jpg",
                         "A unique pizza resembling a forest landscape with a green pesto base, topped with wild mushrooms, truffle oil, arugula leaves, and shavings of Parmesan cheese."),

                FoodItem("Zesty Zephyr Pizza", 1000, "p6.jpg",
                         "A refreshing pizza featuring a garlic and herb-infused crust, topped with juicy grilled paneer, tangy pineapple chunks, red onions, and a sprinkle of cilantro."),

                FoodItem("Smoky Mountain Meltdown Pizza", 1400, "p7.jpg",
                         "A hearty pizza with a barbecue sauce base, topped with tender pulled pork, caramelized onions, smoked Gouda cheese, and finished with a drizzle of barbecue sauce."),

                FoodItem("Tropical Tango Pizza", 1100, "p8.jpg",
                         "A taste of the tropics with a coconut-infused crust, topped with succulent pieces of grilled chicken, mango salsa, red onions, bell peppers, and a sprinkle of toasted coconut flakes."),

                FoodItem("Firecracker Fusion Pizza", 1300, "p9.jpg",
                         "An explosive combination of flavors with a spicy Thai curry sauce base, topped with shrimp, Thai basil, red bell peppers, bean sprouts, and a squeeze of lime."),

                FoodItem("Maple Glaze Delight Pizza", 1500, "p10.jpg",
                         " A sweet and savory pizza featuring a fluffy brioche crust brushed with maple glaze, topped with crispy bacon, caramelized onions, goat cheese, and a drizzle of balsamic reduction.")
            ]

        if index == 1:
            self.menu_items = [
                FoodItem("Truffle Temptation Burger", 850, "b1.jpg",
                         "Indulge in luxury with our Truffle Temptation Burger. A gourmet wild mushroom and black truffle-infused patty, topped with creamy brie cheese, caramelized onions, arugula, and a drizzle of truffle aioli, all served on a freshly baked brioche bun. Elevate your burger experience to new heights of sophistication."),

                FoodItem("Golden Beet Bliss Burger", 900, "b2.jpg",
                         "Experience culinary artistry with our Golden Beet Bliss Burger. A delicate golden beet and quinoa patty, enhanced with hints of orange zest and fresh herbs, paired with tangy goat cheese, baby spinach, roasted walnuts, and a balsamic reduction, all nestled between artisanal sourdough buns. A symphony of flavors that will delight your senses."),

                FoodItem("Saffron Sensation Burger", 950, "b3.jpg",
                         "Transport yourself to exotic lands with our Saffron Sensation Burger. A fragrant saffron-infused lentil and chickpea patty, adorned with roasted bell peppers, caramelized onions, creamy feta cheese, and a dollop of lemony tzatziki sauce, all embraced by soft Mediterranean focaccia bread. An opulent feast fit for royalty."),

                FoodItem("Epicurean Elegance Burger", 980, "b4.jpg",
                         " Immerse yourself in epicurean delight with our Epicurean Elegance Burger. A sophisticated blend of wild rice, porcini mushrooms, and truffle oil crafted into a sumptuous patty, accompanied by decadent Gruyère cheese, caramelized shallots, baby arugula, and a drizzle of aged balsamic glaze, all served on a toasted pretzel bun. An exquisite masterpiece for the discerning palate."),

                FoodItem("Provencal Perfection Burger", 1000, "b5.jpg",
                         "Revel in the flavors of Provence with our Provencal Perfection Burger. A sun-kissed vegetable medley of roasted eggplant, zucchini, and bell peppers, infused with aromatic herbs de Provence, crowned with tangy chevre cheese, grilled artichoke hearts, vine-ripened tomatoes, and a dollop of basil pesto aioli, all embraced by rustic ciabatta bread. A culinary journey through the picturesque countryside of southern France."),

                FoodItem("Royal Mushroom Medley Burger", 850, "b6.jpg",
                         "Treat yourself like royalty with our Royal Mushroom Medley Burger. A luxurious blend of exotic mushrooms including porcini, shiitake, and oyster, paired with creamy Camembert cheese, caramelized onions, baby spinach, and a drizzle of truffle-infused aioli, all nestled within a freshly baked sesame seed brioche bun. Fit for kings and queens of culinary indulgence."),

                FoodItem("Gourmet Garden Galette Burger", 900, "b7.jpg",
                         "Experience the essence of a gourmet garden with our Gourmet Garden Galette Burger. A delicate vegetable galette made with heirloom carrots, sweet potatoes, and fennel, topped with tangy goat cheese, caramelized shallots, baby kale, and a balsamic reduction, all served on a toasted multigrain bun. A masterpiece of seasonal flavors and culinary finesse."),

                FoodItem("Savory Sundried Tomato Supreme", 900, "b8.jpg",
                         "Elevate your taste buds with our Savory Sundried Tomato Supreme. A succulent sun-dried tomato and lentil patty infused with Italian herbs, paired with creamy mozzarella cheese, grilled portobello mushrooms, peppery arugula, and a drizzle of basil pesto, all hugged by a toasted ciabatta bun. A symphony of Mediterranean flavors that will leave you craving more."),

                FoodItem("Acai-infused Vitality Burger", 980, "b9.jpg",
                         "Recharge your senses with our Acai-infused Vitality Burger. A nutrient-packed patty made from a blend of black beans, quinoa, and antioxidant-rich acai berries, topped with creamy avocado slices, crunchy kale slaw, pickled red onions, and a tangy acai mayo, all served on a toasted whole grain bun. A burst of energy in every bite."),

                FoodItem("Luxurious Lentil & Leek Delight", 1000, "b10.jpg",
                         "Indulge in pure luxury with our Luxurious Lentil & Leek Delight. A velvety lentil and leek patty seasoned with fragrant spices and finished with a hint of truffle oil, paired with creamy Gouda cheese, caramelized shallots, baby spinach, and a drizzle of roasted garlic aioli, all embraced by a toasted artisanal sourdough bun. A symphony of refined flavors that epitomizes culinary elegance.")
            ]

        if index == 2:
            self.menu_items = [

                FoodItem("Mystic Mushroom Medley Fettuccine", 1200, "pa1.jpg",
                         "Fettuccine pasta tossed with a medley of exotic mushrooms such as porcini, shiitake, and chanterelle, sautéed in a garlic-infused olive oil. Finished with a sprinkle of truffle salt and freshly grated Parmesan cheese."),

                FoodItem("Heavenly Spinach and Ricotta Ravioli", 1100, "pa2.jpg",
                         "Homemade ravioli stuffed with a creamy blend of spinach, ricotta cheese, and nutmeg. Served with a light sage butter sauce and garnished with toasted pine nuts and a chiffonade of fresh basil."),

                FoodItem("Saffron Delight Risotto Pasta", 1500, "pa3.jpg",
                         "Arborio rice cooked al dente with vegetable broth, saffron threads, and a touch of white wine, creating a creamy and aromatic risotto-style pasta. Finished with roasted cherry tomatoes, grilled asparagus, and a sprinkle of Parmesan cheese."),

                FoodItem("Divine Eggplant Capellini", 1000, "pa4.jpg",
                         "Capellini pasta tossed with roasted eggplant slices, cherry tomatoes, garlic, and fresh basil in a light marinara sauce. Finished with a drizzle of aged balsamic vinegar reduction and a sprinkle of toasted breadcrumbs."),

                FoodItem("Tranquil Truffle Tagliatelle", 1800, "pa5.jpg",
                         "Tagliatelle pasta served in a creamy truffle-infused sauce, enriched with mascarpone cheese and a hint of lemon zest. Garnished with sautéed wild mushrooms, parsley, and a dusting of black pepper."),

                FoodItem("Garden Harvest Penne Primavera", 1300, "pa6.jpg",
                         "Penne pasta tossed with a colorful array of seasonal vegetables such as bell peppers, zucchini, carrots, and cherry tomatoes in a light garlic and herb-infused olive oil. Finished with a sprinkle of fresh Parmesan cheese."),

                FoodItem("Radiant Roasted Red Pepper Linguine", 1400, "pa7.jpg",
                         "Linguine pasta tossed with roasted red bell peppers, garlic, and sun-dried tomatoes in a creamy roasted red pepper sauce. Finished with a drizzle of basil-infused olive oil and a sprinkle of toasted pine nuts."),

                FoodItem("Enchanted Artichoke and Olive Orecchiette", 1600, "pa8.jpg",
                         "Orecchiette pasta served with marinated artichoke hearts, Kalamata olives, cherry tomatoes, and capers in a tangy lemon and white wine sauce. Garnished with fresh parsley and a sprinkle of vegan feta cheese."),

                FoodItem("Bountiful Butternut Squash Gnocchi", 1700, "pa9.jpg",
                         "Handmade gnocchi pillows made with roasted butternut squash and ricotta cheese, served in a brown butter and sage sauce. Finished with toasted walnuts, crispy sage leaves, and a drizzle of maple syrup."),

                FoodItem("Zen Zucchini Noodle Stir-fry", 1100, "pa10.jpg",
                         "Spiralized zucchini noodles stir-fried with tofu, bell peppers, snap peas, and broccoli in a savory soy-ginger sauce. Garnished with sesame seeds, green onions, and a squeeze of lime juice.")

            ]

        if index == 3:
            self.menu_items = [
                FoodItem("Classic Veg Momos", 450, "m1.jpg",
                         "Steamed dumplings filled with a flavorful mixture of finely chopped vegetables, garlic, and ginger. Served with a tangy and spicy dipping sauce."),

                FoodItem("Spicy Paneer Momos", 500, "m2.jpg",
                         "Delicious dumplings stuffed with a spicy mixture of paneer (Indian cottage cheese), onions, and green chilies. Served with a fiery chili garlic sauce."),

                FoodItem("Tandoori Veg Momos", 550, "m3.jpg",
                         "Tender dumplings filled with a marinated mixture of assorted vegetables, grilled to perfection in a tandoor (clay oven). Served with mint chutney."),

                FoodItem("Cheese Corn Momos", 400, "m4.jpg",
                         "Steamed dumplings filled with a delectable mixture of sweet corn kernels and melted cheese. Served with a zesty tomato salsa."),

                FoodItem("Spinach and Mushroom Momos", 400, "m5.jpg",
                         "Healthy dumplings stuffed with a nutritious blend of spinach, mushrooms, and aromatic spices. Served with a tangy tamarind chutney."),

                FoodItem("Crispy Veg Momos", 500, "m6.jpg",
                         "Deep-fried dumplings filled with a crunchy mixture of mixed vegetables and herbs. Served with a sweet and spicy dipping sauce."),

                FoodItem("Paneer Tikka Momos", 450, "m7.jpg",
                         "Succulent dumplings filled with marinated paneer cubes, grilled to perfection and served with mint yogurt dip."),

                FoodItem("Soya Chaap Momos", 550, "m8.jpg",
                         "Savory dumplings filled with spicy soya chaap (textured vegetable protein) chunks, onions, and bell peppers. Served with a creamy mayo dip."),

                FoodItem("Thai Basil Veg Momos", 450, "m9.jpg",
                         "Exotic dumplings filled with a fragrant mixture of Thai basil, tofu, and vegetables. Served with a spicy Thai dipping sauce."),

                FoodItem("BBQ Jackfruit Momos", 480, "m10.jpg",
                         "Unique dumplings filled with tender jackfruit cooked in smoky BBQ sauce. Served with a tangy pineapple salsa.")
            ]

        if index == 4:
            self.menu_items = [
                FoodItem("Hakka Noodles", 800, "n1.jpg",
                         "Stir-fried noodles cooked with assorted vegetables, ga2rlic, ginger, and soy sauce, seasoned with a blend of Chinese spices."),

                FoodItem("Schezwan Veg Noodles", 850, "n2.jpg",
                         "Spicy and flavorful noodles tossed with colorful bell peppers, carrots, onions, and cabbage in a fiery Schezwan sauce."),

                FoodItem("Chilli Garlic Noodles", 850, "n3.jpg",
                         "Garlicky noodles cooked with a spicy chili sauce and tossed with crunchy vegetables. A perfect blend of heat and flavor."),

                FoodItem("Pad Thai Noodles", 750, "n4.jpg",
                         "Thai-style stir-fried noodles cooked with tofu, bean sprouts, peanuts, and tamarind sauce, garnished with lime wedges and cilantro."),

                FoodItem("Singapore Veg Noodles", 800, "n5.jpg",
                         "Curried noodles cooked with shredded vegetables, tofu, and bean sprouts, seasoned with a blend of aromatic spices. A popular street food dish from Singapore."),

                FoodItem("Coconut Curry Veg Noodles", 700, "n6.jpg",
                         "Creamy coconut curry noodles cooked with mixed vegetables, tofu, and Thai curry paste. A comforting and flavorful noodle dish."),

                FoodItem("Miso Veggie Ramen", 900, "n7.jpg",
                         "Japanese-style ramen noodles served in a savory miso broth with mushrooms, spinach, tofu, and green onions. A hearty and nutritious meal."),

                FoodItem("Teriyaki Veggie Udon", 900, "n8.jpg",
                         "Thick and chewy udon noodles stir-fried with a sweet and savory teriyaki sauce, mixed vegetables, and tofu. A satisfying Japanese noodle dish."),

                FoodItem("Kung Pao Tofu Noodles", 880, "n9.jpg",
                         "Spicy and tangy noodles cooked with crispy tofu, peanuts, bell peppers, and onions in a flavorful Kung Pao sauce."),

                FoodItem("Vegetarian Pho", 930, "n10.jpg",
                         "Vietnamese rice noodles served in a fragrant and aromatic broth with tofu, bok choy, bean sprouts, and fresh herbs. A light and refreshing noodle soup.")
            ]

        if index == 5:
            self.menu_items = [
                FoodItem("Veg Manchurian Combo", 850, "combo.jpg",
                         "A perfect combination of vegetable Manchurian balls served with a side of Hakka noodles or fried rice, and a refreshing soft drink."),

                FoodItem("Paneer Tikka Kathi Roll Combo", 900, "combo.jpg",
                         "Grilled paneer tikka wrapped in a soft roti (Indian flatbread) with onions, bell peppers, and tangy chutneys. Served with crispy fries and a chilled beverage."),

                FoodItem("Schezwan Veggie Fried Rice Combo", 750, "combo.jpg",
                         "Spicy Schezwan fried rice cooked with mixed vegetables and served with crispy veg spring rolls and a choice of soft drink."),

                FoodItem("Veggie Burger and Fries Combo", 800, "combo.jpg",
                         "A classic veggie burger made with a hearty vegetable patty, lettuce, tomato, and mayo, served with golden fries and a refreshing beverage."),

                FoodItem("Mushroom Tikka Masala Combo", 750, "combo.jpg",
                         "Creamy and aromatic mushroom tikka masala served with fluffy basmati rice, garlic naan, and a side of cucumber raita."),

                FoodItem("Palak Paneer and Jeera Rice Combo", 800, "combo.jpg",
                         "Rich and creamy spinach gravy cooked with paneer cubes, served with fragrant jeera (cumin) rice, papadum, and a soft drink."),

                FoodItem("Veggie Wrap and Salad Combo", 850, "combo.jpg",
                         "A healthy and satisfying veggie wrap filled with assorted vegetables, hummus, and feta cheese, served with a side salad and dressing."),

                FoodItem("Falafel Platter Combo", 850, "combo.jpg",
                         "Golden and crispy falafel balls served with hummus, tabbouleh salad, pita bread, and a refreshing mint yogurt sauce."),

                FoodItem("Stuffed Bell Peppers Combo", 750, "combo.jpg",
                         "Bell peppers stuffed with a savory mixture of rice, lentils, vegetables, and spices, served with garlic bread and a soft drink."),

                FoodItem("Quinoa Salad and Soup Combo", 650, "combo.jpg",
                         "A nutritious combo featuring a refreshing quinoa salad with mixed greens, tomatoes, cucumbers, and a cup of hearty vegetable soup.")
            ]

        if index == 6:
            self.menu_items = [
                FoodItem("Assorted Veggie Donuts", 350, "d1.jpg",
                         "Soft and fluffy donuts made with a blend of mixed vegetables and spices, deep-fried to perfection. Served with a choice of dipping sauce."),

                FoodItem("Spiced Carrot Cake Donuts", 430, "d2.jpg",
                         "Moist and flavorful carrot cake donuts spiced with cinnamon, nutmeg, and ginger, topped with a cream cheese glaze."),

                FoodItem("Zucchini Chocolate Chip Donuts", 380, "d3.jpg",
                         "Healthy and indulgent chocolate chip donuts made with grated zucchini for added moisture and nutrition."),

                FoodItem("Pumpkin Spice Donuts", 340, "d4.jpg",
                         "Irresistible pumpkin spice donuts glazed with a sweet and spicy pumpkin icing, perfect for fall."),

                FoodItem("Banana Walnut Donuts", 360, "d5.jpg",
                         "Delicious banana walnut donuts made with ripe bananas and crunchy walnuts, topped with a vanilla glaze."),

                FoodItem("Blueberry Lemon Donuts", 480, "d6.jpg",
                         "Light and refreshing lemon-flavored donuts studded with juicy blueberries and drizzled with a lemon glaze."),

                FoodItem("Caramel Apple Donuts", 500, "d7.jpg",
                         "Decadent caramel apple donuts made with spiced apple cider and topped with a gooey caramel glaze."),

                FoodItem("Coconut Cream Pie Donuts", 320, "d8.jpg",
                         "Indulgent coconut cream pie donuts filled with a rich coconut custard and topped with whipped cream and toasted coconut flakes."),

                FoodItem("Matcha Green Tea Donuts", 400, "d9.jpg",
                         "Unique and flavorful matcha green tea donuts glazed with a sweet and earthy matcha icing, perfect for green tea lovers."),

                FoodItem("Raspberry Almond Donuts", 480, "d10.jpg",
                         "Delicate almond-flavored donuts filled with tangy raspberry jam and topped with sliced almonds and a raspberry glaze.")
            ]

        if index == 7:
            self.menu_items = [
                FoodItem("Mint Mojito", 500, "bv1.jpg",
                         "A refreshing mocktail made with fresh mint leaves, lime juice, sugar, and soda water, served over ice and garnished with mint sprigs and lime wedges."),

                FoodItem("Tropical Paradise Smoothie", 540, "bv2.jpg",
                         "A tropical delight blending mangoes, pineapples, bananas, and coconut milk into a creamy and refreshing smoothie."),

                FoodItem("Iced Green Tea with Lemon", 520, "bv3.jpg",
                         "Chilled green tea infused with lemon slices, served over ice for a rejuvenating and antioxidant-rich beverage."),

                FoodItem("Watermelon Basil Cooler", 530, "bv4.jpg",
                         "A cooling summer drink made with fresh watermelon juice, basil leaves, and a hint of lime, served over ice."),

                FoodItem("Virgin Pina Colada", 550, "bv5.jpg",
                         "A non-alcoholic version of the classic tropical cocktail, made with coconut cream, pineapple juice, and crushed ice."),

                FoodItem("Berry Blast Mocktail", 580, "bv6.jpg",
                         "An explosion of berry flavors with strawberries, blueberries, raspberries, and blackberries, blended with lemonade and ice."),

                FoodItem("Cucumber Mint Cooler", 550, "bv7.jpg",
                         "A refreshing drink made with cucumber juice, mint leaves, lime juice, and sparkling water, served over ice."),

                FoodItem("Orange Creamsicle Float", 540, "bv8.jpg",
                         "A nostalgic treat featuring orange soda and creamy vanilla ice cream, reminiscent of childhood summers."),

                FoodItem("Ginger Peach Iced Tea", 510, "bv9.jpg",
                         "Iced tea infused with fresh ginger and peach slices, sweetened with honey and served over ice for a refreshing twist."),

                FoodItem("Mango Lassi", 560, "bv10.jpg",
                         "A classic Indian beverage made with ripe mangoes, yogurt, milk, and a touch of cardamom, blended into a creamy and indulgent drink.")
            ]

        if index == 8:
            self.menu_items = [
                FoodItem("Cappuccino", 400, "hv1.jpg",
                         "A classic Italian coffee beverage that combines espresso, steamed milk, and a layer of frothed milk foam."),

                FoodItem("Caffe Latte", 450, "hv2.jpg",
                         "A milky coffee made with a shot of espresso and steamed milk, topped with a small amount of milk foam."),

                FoodItem("Espresso", 440, "hv3.jpg",
                         "A strong and concentrated coffee made by forcing hot water through finely-ground coffee beans, resulting in a small shot of intense flavor."),

                FoodItem("Caffe Mocha", 470, "hv4.jpg",
                         "A decadent coffee drink made with espresso, steamed milk, chocolate syrup, and topped with whipped cream."),

                FoodItem("Hot Chocolate", 500, "hv5.jpg",
                         "A comforting and indulgent beverage made with hot milk or water mixed with cocoa powder and sweetened with sugar, often topped with whipped cream or marshmallows."),

                FoodItem("Chai Latte", 400, "hv6.jpg",
                         "A spiced tea drink made with black tea, steamed milk, and a blend of aromatic spices such as cinnamon, cardamom, ginger, and cloves."),

                FoodItem("Green Tea Latte", 440, "hv7.jpg",
                         "A creamy and soothing drink made with matcha green tea powder, steamed milk, and a touch of sweetener, known for its vibrant green color and earthy flavor."),

                FoodItem("Hot Toddy", 480, "hv8.jpg",
                         "A warm and comforting cocktail made with whiskey, hot water, honey, and lemon juice, often enjoyed as a remedy for colds or simply as a winter warmer."),

                FoodItem("Mulled Wine", 590, "hv9.jpg",
                         "A festive and spiced beverage made by heating red wine with various mulling spices such as cinnamon, cloves, and orange zest, often served hot during the winter months."),

                FoodItem("Apple Cider", 600, "hv10.jpg",
                         "A cozy drink made from freshly-pressed apples, often spiced with cinnamon and cloves and served hot or warm, perfect for chilly autumn days.")
            ]

        for item in self.menu_items:
            item_widget = QWidget()
            item_layout = QVBoxLayout()
            item_widget.setLayout(item_layout)

            label = QLabel(f"{item.name} - ₹{item.price:.2f}")
            label.setFont(QFont("Arial", 12))  # Change font and size
            item_layout.addWidget(label)

            if item.description:
                description_label = QLabel(item.description)
                description_label.setFont(QFont("Arial", 10))  # Change font and size
                description_label.setWordWrap(True)  # Wrap text to fit widget width
                item_layout.addWidget(description_label)

            if item.image_path:
                pixmap = QPixmap(item.image_path)
                image_label = QLabel()
                image_label.setPixmap(pixmap)
                item_layout.addWidget(image_label)

            add_button = QPushButton("Add to Order")
            add_button.clicked.connect(lambda _, i=item: self.add_to_order(i))
            item_layout.addWidget(add_button)

            item_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.menu_layout.addWidget(item_widget)

            self.menu_area.verticalScrollBar().setValue(0)

    def add_to_order(self, item):
        self.data_handler.data_received.emit(item.name, item.price, 1)

    def update_total_price(self):
        total_price = sum(
            float(self.order_table.item(row, 3).text())
            for row in range(self.order_table.rowCount())
        )
        self.total_price_label.setText(f"Total Price: ₹{total_price:.2f}")
        self.total_price_label.setFont(QFont("Arial", 8))  # Adjust font size here

    def update_total_price_from_quantity(self, item):
        if item.column() == 2:  # Check if quantity column is edited
            quantity = float(item.text())
            row = item.row()
            price = float(self.order_table.item(row, 1).text())
            total = quantity * price
            self.order_table.setItem(row, 3, QTableWidgetItem(str(total)))  # Update total price
            self.update_total_price()  # Update total price label

    def receive_data(self, item_name, price, quantity):
        for row in range(self.order_table.rowCount()):
            if self.order_table.item(row, 0).text() == item_name:  # Check if item name matches
                # If item exists, increment the quantity and update the table
                current_quantity = int(self.order_table.item(row, 2).text())
                new_quantity = current_quantity + quantity
                total_price = new_quantity * price
                self.order_table.setItem(row, 2, QTableWidgetItem(str(new_quantity)))
                self.order_table.setItem(row, 3, QTableWidgetItem(str(total_price)))
                self.update_total_price()  # Update total price
                return  # Exit the function as item is found and updated

        # If item doesn't exist, add it to the table
        row_position = self.order_table.rowCount()
        self.order_table.insertRow(row_position)
        self.order_table.setItem(row_position, 0, QTableWidgetItem(item_name))
        self.order_table.setItem(row_position, 1, QTableWidgetItem(str(price)))
        self.order_table.setItem(row_position, 2, QTableWidgetItem(str(quantity)))
        self.order_table.setItem(row_position, 3, QTableWidgetItem(str(price * quantity)))
        self.update_total_price()  # Update total price

    def proceed_to_confirm(self):
        confirm_dialog = Confirm(self)

        # Transfer data from Table 1 to Table 2
        for row in range(self.order_table.rowCount()):
            item_name = self.order_table.item(row, 0).text()
            quantity = int(self.order_table.item(row, 2).text())
            price = float(self.order_table.item(row, 1).text())

            confirm_dialog.table2.setItem(row, 0, QTableWidgetItem(item_name))
            confirm_dialog.table2.setItem(row, 1, QTableWidgetItem(str(quantity)))
            confirm_dialog.table2.setItem(row, 2, QTableWidgetItem(str(price)))

        # Close the current window
        self.close()

        # Open the new window
        confirm_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FoodApp()
    window.show()
    sys.exit(app.exec_())
