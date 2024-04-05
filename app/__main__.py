from PySide6 import QtCore, QtGui, QtWidgets
from functools import partial
from app.db import MANAGER

from app.views import TableWindow

BUTTONS_INFO = [
    ("button_1x1", (0, 100, 150, 100), "background-color: rgb(215, 255, 121);", 17, True, "1x1"),
    ("button_3x5", (150, 100, 150, 100), "background-color: rgb(215, 255, 121);", 17, True, "3x5"),
    ("button_5x5", (0, 200, 150, 100), "background-color: rgb(215, 255, 121);", 17, True, "5x5"),
    ("button_7x7", (150, 200, 150, 100), "background-color: rgb(215, 255, 121);", 17, True, "7x7"),
    ("button_5x10", (0, 300, 150, 100), "background-color: rgb(215, 255, 121);", 17, True, "5x10"),
    ("button_10x10", (150, 300, 150, 100), "background-color: rgb(215, 255, 121);", 17, True, "10x10"),
]

SIZE = 300
HEIGHT = 400

class Ui_MainWindow(object):
    """ Class for UI of MainWindow """
    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """ Setup UI for MainWindow """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(SIZE, HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        for button_info in BUTTONS_INFO:
            button_name, geometry, background_color, font_size, bold, text = button_info
            button = self._create_button(button_name, geometry, background_color, font_size, bold, text)
            button.clicked.connect(partial(self.add_table_entry, text))

        self.info_label = self._create_label("info_label", (0, 0, 300, 50), "background-color: rgb(255, 85, 0);", 13, True)
        
        self.button_tables = self._create_button("button_tables", (0, 50, 300, 50), "background-color: rgb(255, 125, 127);", 13, True, "Tables of calculations")
        self.button_tables.clicked.connect(self.open_table_window)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open_table_window(self) -> None:
        """ Open class TableWindow for calculations """
        self.table_window = TableWindow()
        self.table_window.show()

    def add_table_entry(self, form: str) -> None:
        """ 
        Add entry to the table
        
        Args:
            form: form of the entry
        """
        sides = form.split('x')
        calculation = str(round(SIZE * HEIGHT / (int(sides[0]) * int(sides[1]))))
        
        date_created = QtCore.QDateTime.currentDateTime().toString()
        
        static_id = MANAGER.insert_data((form, calculation, date_created))
        
        table_window = getattr(self, 'table_window', None)
        if table_window:
            table_window.add_entry(static_id, form, calculation, date_created)
            
        self.info_label.setText(f"Form {form} added")

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """ Set text for UI elements """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Form"))
        self.info_label.setText(_translate("MainWindow", "Select Form to calculate square"))

    def _create_button(self, text: str, geometry: tuple[int, int, int, int], background_color: str, font_size: int, bold: bool, button_text: str) -> QtWidgets.QPushButton:
        """
        Create button with specified parameters 
        
        Args:
            text: object name
            geometry: button geometry
            background_color: background color
            font_size: font size
            bold: bold text
            button_text: text on the button
            
        Returns:
            created button
        """
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setGeometry(QtCore.QRect(*geometry))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(bold)
        button.setFont(font)
        button.setStyleSheet(background_color)
        button.setText(button_text)
        button.setObjectName(text)
        return button

    def _create_label(self, object_name: str, place: tuple[int,int,int,int], background_color: str, font_size: int, bold: bool) -> QtWidgets.QLabel:
        """
        Create label with specified parameters
        
        Args:
            object_name: object name
            place: label geometry
            background_color: background color
            font_size: font size
            bold: bold text
            
        Returns:
            created label
        """
        label = QtWidgets.QLabel(self.centralwidget)
        label.setGeometry(QtCore.QRect(*place))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(bold)
        label.setFont(font)
        label.setStyleSheet(background_color)
        label.setObjectName(object_name)
        return label

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
