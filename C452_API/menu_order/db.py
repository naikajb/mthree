import mysql.connector

db_config = {
    'host': 'localhost',
    "user": 'root',
    "name": 'restaurantDB'
}

class Database: 
    
    def __init__ (self):
        self.conn = get_db_connection()
        set_up_tables()

    def get_db_connection():
        return mysql.connector.connect(**db_config)

    def set_up_tables():
        """ Iniializes the tables for Order, MenuItem and OrderItem """

        cursor = self.conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Orders(
                OrderID INT PRIMARY KEY AUTO_INCREMENT,
                ClientName VARCHAR(100) NOT NULL,
                Status ENUM('completed', 'ready', 'delivered', 'cancelled', 'preparing', 'pending') DEFAULT 'pending',
                TotalAmount FLOAT NOT NULL,
                OrderType ENUM('dine_in', 'pickup', 'delivery') DEFAULT 'dine_in',
                Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")


        cursor.execute("""CREATE TABLE IF NOT EXISTS MenuItem(
                MenuItemID INT PRIMARY KEY AUTO_INCREMENT,
                ItemName VARCHAR(100) NOT NULL,
                description TEXT,
                isAvail BOOLEAN DEFAULT TRUE,
                Price FLOAT NOT NULL);""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS OrderItem(
                OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
                MenuItemID INT REFERENCES MenuItem(MenuItemID) ON DELETE CASCADE,
                OrderID INT REFERENCES Orders(OrderID) ON DELETE CASCADE,
                Quantity INT NOT NULL);""")

        
