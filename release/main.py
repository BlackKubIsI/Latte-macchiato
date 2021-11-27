from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHeaderView, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5 import uic
import sqlite3
import sys
from UI.main import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Form


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(100, 100, 830, 620)
        with sqlite3.connect("./data/coffee.sqlite") as con:
            self.table = con.cursor().execute(f"""select * from coffee""").fetchall()
        self.settings()
    
    def settings(self):
        self.tableWidget.setGeometry(20, 20, 790, 540)
        self.pushButton.setGeometry(20, 570, 100, 20)
        self.pushButton.clicked.connect(self.add)
        self.up_date()
    
    def up_date(self):
        with sqlite3.connect("data/coffee.sqlite") as con:
            self.table = con.cursor().execute(f"""select * from coffee""").fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(self.table))
        for i in range(len(self.table)):
            btnChange = QPushButton(self, text="Change")
            btnChange.clicked.connect(lambda btn=btnChange, id_=i: self.red(id_))
            for n in range(7):
                self.tableWidget.setItem(i, n, QTableWidgetItem(str(self.table[i][n])))
            self.tableWidget.setCellWidget(i, 7, btnChange)
    
    def add(self):
        self.okn = ADD_or_RED(True, -1, self)
        self.okn.show()

    def red(self, id_):
        self.okn = ADD_or_RED(False, id_, self)
        self.okn.show()


class ADD_or_RED(QWidget, Ui_Form):
    def __init__(self, f, id_, main):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(300, 200, 400, 500)
        self.f, self.id_, self.main = f, id_, main
        self.settings()
    
    def settings(self):
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.close)
        if not self.f:
            with sqlite3.connect("data/coffee.sqlite") as con:
                table = con.cursor().execute(f"""select * from coffee 
                where ID = {self.id_}""").fetchall()[0]
            self.lineEdit.setText(table[1])
            self.lineEdit_2.setText(table[2])
            self.lineEdit_3.setText(table[3])
            self.lineEdit_4.setText(table[4])
            self.lineEdit_5.setText(table[5])
            self.lineEdit_6.setText(table[6])
    
    def save(self):
        with sqlite3.connect("data/coffee.sqlite") as con:
            self._1 = self.lineEdit.text()
            self._2 = self.lineEdit_2.text()
            self._3 = self.lineEdit_3.text()
            self._4 = self.lineEdit_4.text()
            self._5 = self.lineEdit_5.text()
            self._6 = self.lineEdit_6.text()
            if self.f:
                con.cursor().execute(f"""INSERT INTO coffee(name_of_the_variety, degree_of_roasting,
                ground_OR_in_grains, description_of_taste, price, volume_of_packaging)
                 VALUES('{self._1}', '{self._2}', '{self._3}', '{self._4}', '{self._5}', '{self._6}')""")
            else:
                sp = [self._1, self._2, self._3, self._4, self._5, self._6]
                names = "name_of_the_variety, degree_of_roasting, \
ground_OR_in_grains, description_of_taste, price, volume_of_packaging".split(", ")
                for i in range(6):
                    con.cursor().execute(f"""UPDATE coffee
                    SET {names[i]} = '{str(sp[i])}'
                    WHERE ID = {self.id_}""")
        self.main.up_date()
        self.close()


app = QApplication(sys.argv)
main = Main()
main.show()
sys.exit(app.exec())