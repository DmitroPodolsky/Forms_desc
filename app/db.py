from pathlib import Path
import sqlite3

from loguru import logger

project_dir = Path(__file__).parent.parent

class Manager:
    """Class for managing database connection and data"""

    def __init__(self) -> None:
        """Initialize database connection and create table if not exists"""

        self.connection = sqlite3.connect(project_dir / "data" / "statistics.db")
        self.create_table()

    def create_table(self) -> None:
        """Create table if not exists"""

        cursor = self.connection.cursor()
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            form TEXT,
            calculation TEXT,
            date_created TEXT
        )'''
        cursor.execute(create_table_sql)
        self.connection.commit()
        cursor.close()

        logger.info("Table created")

    def insert_data(self, values: tuple) -> int:
        """
        Insert data into table and return ID of the object
        
        Args:
            values: values to insert into table
            
        Returns:
            ID of the inserted object
        """

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO statistics (form, calculation, date_created) VALUES (?, ?, ?)", values)
        self.connection.commit()

        logger.info("Data inserted")
        return cursor.lastrowid 

    def select_data(self) -> list[tuple]:
        """
        Select data from table
        
        Returns:
            list of tuples with data
        """

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM statistics")
        data = cursor.fetchall()
        cursor.close()

        logger.info("Data selected")

        return data

    def delete_data(self, id_static: int) -> bool:
        """
        Delete data from table
        
        Args:
            id_static: ID of the object to delete
        """
        
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM statistics WHERE id=?", (id_static,))
        self.connection.commit()
        cursor.close()
        logger.info("Data deleted")
        return True
    
    def delete_all_data(self) -> None:
        """ Delete all data from the table """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM statistics")
        self.connection.commit()
        cursor.close()
        logger.info("All data deleted")

        
MANAGER = Manager()