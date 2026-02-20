"""
Database layer for System A - Inventory Management System
"""
import sqlite3
import json
from contextlib import contextmanager
from typing import List, Dict, Optional

DATABASE_PATH = 'inventory.db'


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize database schema"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Locations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('store', 'warehouse'))
            )
        ''')

        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

        # Inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (location_id) REFERENCES locations(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                UNIQUE(location_id, product_id)
            )
        ''')

        conn.commit()


def get_all_locations() -> List[Dict]:
    """Get all locations"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, code, name, type FROM locations ORDER BY code')
        return [dict(row) for row in cursor.fetchall()]


def get_location_by_code(code: str) -> Optional[Dict]:
    """Get location by code"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, code, name, type FROM locations WHERE code = ?', (code,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_inventory_by_location(location_code: str) -> List[Dict]:
    """Get all inventory items for a location"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                p.sku,
                p.name as product_name,
                p.description,
                i.quantity,
                l.code as location_code,
                l.name as location_name
            FROM inventory i
            JOIN products p ON i.product_id = p.id
            JOIN locations l ON i.location_id = l.id
            WHERE l.code = ?
            ORDER BY p.sku
        ''', (location_code,))
        return [dict(row) for row in cursor.fetchall()]


def get_product_by_sku(sku: str) -> Optional[Dict]:
    """Get product by SKU"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, sku, name, description FROM products WHERE sku = ?', (sku,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_inventory(location_code: str, sku: str, quantity_change: int, operation: str = 'set') -> Dict:
    """
    Update inventory for a product at a location
    operation: 'set' (absolute), 'increment', 'decrement'
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get location
        location = get_location_by_code(location_code)
        if not location:
            raise ValueError(f"Location not found: {location_code}")

        # Get product
        product = get_product_by_sku(sku)
        if not product:
            raise ValueError(f"Product not found: {sku}")

        # Get current inventory
        cursor.execute('''
            SELECT id, quantity FROM inventory
            WHERE location_id = ? AND product_id = ?
        ''', (location['id'], product['id']))

        inventory_row = cursor.fetchone()

        # Calculate new quantity
        if operation == 'set':
            new_quantity = quantity_change
        elif operation == 'increment':
            current_qty = inventory_row['quantity'] if inventory_row else 0
            new_quantity = current_qty + quantity_change
        elif operation == 'decrement':
            current_qty = inventory_row['quantity'] if inventory_row else 0
            new_quantity = current_qty - quantity_change
        else:
            raise ValueError(f"Invalid operation: {operation}")

        # Ensure non-negative
        if new_quantity < 0:
            raise ValueError(f"Insufficient stock. Current: {inventory_row['quantity'] if inventory_row else 0}, requested change: {quantity_change}")

        # Update or insert
        if inventory_row:
            cursor.execute('''
                UPDATE inventory SET quantity = ?
                WHERE location_id = ? AND product_id = ?
            ''', (new_quantity, location['id'], product['id']))
        else:
            cursor.execute('''
                INSERT INTO inventory (location_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (location['id'], product['id'], new_quantity))

        conn.commit()

        return {
            'location_code': location_code,
            'sku': sku,
            'previous_quantity': inventory_row['quantity'] if inventory_row else 0,
            'new_quantity': new_quantity,
            'operation': operation
        }


def get_all_inventory() -> List[Dict]:
    """Get complete inventory across all locations"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                l.code as location_code,
                l.name as location_name,
                l.type as location_type,
                p.sku,
                p.name as product_name,
                i.quantity
            FROM inventory i
            JOIN products p ON i.product_id = p.id
            JOIN locations l ON i.location_id = l.id
            ORDER BY l.code, p.sku
        ''')
        return [dict(row) for row in cursor.fetchall()]
