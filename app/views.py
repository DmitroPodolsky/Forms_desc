from PySide6 import QtWidgets
from loguru import logger

from app.db import MANAGER

class TableWindow(QtWidgets.QWidget):
    """ Window with a table of calculations """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tables of calculations")
        self.setGeometry(100, 100, 500, 300)  # Increased width to accommodate the row index
        
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)  # Increased column count to include the id column
        self.table.setHorizontalHeaderLabels(["ID", "Form", "Calculation", "Date Created"])
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        
        # QLineEdit for id and QPushButton to delete row by id
        self.id_edit = QtWidgets.QLineEdit()
        self.id_edit.setPlaceholderText("ID to delete")
        self.delete_row_button = QtWidgets.QPushButton("Delete by ID")
        self.delete_row_button.clicked.connect(self.delete_row_by_id)
        
        layout.addWidget(self.id_edit)
        layout.addWidget(self.delete_row_button)
        self.setLayout(layout)
        
        for data in MANAGER.select_data():
            self.add_entry(*data)

    def add_entry(self, static_id: int, form: str, calculation: str, date_created: str) -> None:
        """
        Add entry to the table
        
        Args:
            static_id: ID of the entry
            form: form of the entry
            calculation: calculation of the entry
            date_created: date of creation of the entry
        """
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        # Display the id in the first column
        self.table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(static_id)))
        self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(form))
        self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(calculation))
        self.table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(date_created))
        
    # Function to delete a row by id
    def delete_row_by_id(self) -> None:
        """ Delete row by ID """
        id_to_delete = int(self.id_edit.text())
        for row in range(self.table.rowCount()):
            if int(self.table.item(row, 0).text()) == id_to_delete:
                MANAGER.delete_data(id_to_delete)
                self.table.removeRow(row)
                return
        logger.warning("ID not found")
        QtWidgets.QMessageBox.warning(self, "Warning", "ID not found")
