"""
Database module for Stock Record Keeping application.
Handles all database operations using SQLite.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple

DATABASE_FILE = "stocks.db"


class StockDatabase:
    """Manages stock records in SQLite database."""
    
    def __init__(self, db_file: str = DATABASE_FILE):
        """Initialize database connection."""
        self.db_file = db_file
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_name TEXT NOT NULL,
                ticker TEXT NOT NULL,
                price_paid REAL NOT NULL,
                amount INTEGER NOT NULL,
                current_value REAL,
                price_change_percent REAL,
                last_reviewed_date TEXT,
                notes TEXT,
                image_path TEXT,
                position_status TEXT NOT NULL,
                earnings_date TEXT,
                created_date TEXT NOT NULL,
                modified_date TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_stock(self, stock_name: str, ticker: str, price_paid: float, 
                  amount: int, position_status: str, notes: str = "",
                  image_path: str = "", current_value: float = None,
                  earnings_date: str = None) -> int:
        """Add a new stock record."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        last_reviewed = now
        
        cursor.execute("""
            INSERT INTO stocks (
                stock_name, ticker, price_paid, amount, current_value,
                last_reviewed_date, notes, image_path, position_status,
                earnings_date, created_date, modified_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (stock_name, ticker, price_paid, amount, current_value,
              last_reviewed, notes, image_path, position_status,
              earnings_date, now, now))
        
        stock_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return stock_id
    
    def update_stock(self, stock_id: int, stock_name: str, ticker: str,
                    price_paid: float, amount: int, position_status: str,
                    notes: str = "", image_path: str = "",
                    current_value: float = None, earnings_date: str = None):
        """Update an existing stock record."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            UPDATE stocks SET
                stock_name = ?,
                ticker = ?,
                price_paid = ?,
                amount = ?,
                current_value = ?,
                notes = ?,
                image_path = ?,
                position_status = ?,
                earnings_date = ?,
                modified_date = ?
            WHERE id = ?
        """, (stock_name, ticker, price_paid, amount, current_value,
              notes, image_path, position_status, earnings_date, now, stock_id))
        
        conn.commit()
        conn.close()
    
    def delete_stock(self, stock_id: int):
        """Delete a stock record."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM stocks WHERE id = ?", (stock_id,))
        
        conn.commit()
        conn.close()
    
    def get_stock(self, stock_id: int) -> Optional[sqlite3.Row]:
        """Get a single stock record by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM stocks WHERE id = ?", (stock_id,))
        stock = cursor.fetchone()
        
        conn.close()
        return stock
    
    def get_all_stocks(self, sort_by: str = "id") -> List[sqlite3.Row]:
        """Get all stock records with optional sorting."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        valid_sorts = {
            "id": "id DESC",
            "name": "stock_name ASC",
            "value": "CAST((COALESCE(current_value, price_paid) * amount) AS REAL) DESC",
            "percent": "price_change_percent DESC",
            "ticker": "ticker ASC",
            "status": "position_status ASC",
            "reviewed": "last_reviewed_date ASC"
        }
        
        order_clause = valid_sorts.get(sort_by, "id DESC")
        
        cursor.execute(f"SELECT * FROM stocks ORDER BY {order_clause}")
        stocks = cursor.fetchall()
        
        conn.close()
        return stocks
    
    def update_last_reviewed(self, stock_id: int):
        """Update last reviewed date to now."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            UPDATE stocks SET last_reviewed_date = ?, modified_date = ?
            WHERE id = ?
        """, (now, now, stock_id))
        
        conn.commit()
        conn.close()
    
    def update_current_values(self, stock_id: int, current_value: float,
                             price_change_percent: float):
        """Update current value and price change percentage."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            UPDATE stocks SET
                current_value = ?,
                price_change_percent = ?,
                modified_date = ?
            WHERE id = ?
        """, (current_value, price_change_percent, now, stock_id))
        
        conn.commit()
        conn.close()
