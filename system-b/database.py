"""
Database layer for System B - Order Fulfillment System
"""
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Optional
from datetime import datetime

DATABASE_PATH = 'orders.db'


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

        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                location_code TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending', 'processing', 'completed', 'cancelled')),
                order_date TEXT NOT NULL,
                total_amount REAL NOT NULL DEFAULT 0
            )
        ''')

        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                sku TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')

        # Stock levels cache (received from System A)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_code TEXT NOT NULL,
                sku TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                last_updated TEXT NOT NULL,
                UNIQUE(location_code, sku)
            )
        ''')

        conn.commit()


def get_all_orders() -> List[Dict]:
    """Get all orders with their items"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get all orders
        cursor.execute('''
            SELECT id, order_number, customer_name, location_code, status, order_date, total_amount
            FROM orders
            ORDER BY order_date DESC
        ''')
        orders = [dict(row) for row in cursor.fetchall()]

        # Get items for each order
        for order in orders:
            cursor.execute('''
                SELECT sku, product_name, quantity, unit_price
                FROM order_items
                WHERE order_id = ?
            ''', (order['id'],))
            order['items'] = [dict(row) for row in cursor.fetchall()]

        return orders


def get_order_by_number(order_number: str) -> Optional[Dict]:
    """Get order by order number"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, order_number, customer_name, location_code, status, order_date, total_amount
            FROM orders
            WHERE order_number = ?
        ''', (order_number,))

        row = cursor.fetchone()
        if not row:
            return None

        order = dict(row)

        # Get items
        cursor.execute('''
            SELECT sku, product_name, quantity, unit_price
            FROM order_items
            WHERE order_id = ?
        ''', (order['id'],))
        order['items'] = [dict(row) for row in cursor.fetchall()]

        return order


def get_pending_orders() -> List[Dict]:
    """Get all pending orders"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, order_number, customer_name, location_code, status, order_date, total_amount
            FROM orders
            WHERE status = 'pending'
            ORDER BY order_date
        ''')
        orders = [dict(row) for row in cursor.fetchall()]

        # Get items for each order
        for order in orders:
            cursor.execute('''
                SELECT sku, product_name, quantity, unit_price
                FROM order_items
                WHERE order_id = ?
            ''', (order['id'],))
            order['items'] = [dict(row) for row in cursor.fetchall()]

        return orders


def update_stock_levels(stock_data: List[Dict]) -> int:
    """
    Update stock levels from external system
    stock_data: list of dicts with keys: location_code, sku, product_name, quantity
    Returns: number of records updated
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        count = 0

        for item in stock_data:
            cursor.execute('''
                INSERT INTO stock_levels (location_code, sku, product_name, quantity, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(location_code, sku)
                DO UPDATE SET
                    product_name = excluded.product_name,
                    quantity = excluded.quantity,
                    last_updated = excluded.last_updated
            ''', (
                item['location_code'],
                item['sku'],
                item['product_name'],
                item['quantity'],
                timestamp
            ))
            count += 1

        conn.commit()
        return count


def get_stock_levels() -> List[Dict]:
    """Get all cached stock levels"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT location_code, sku, product_name, quantity, last_updated
            FROM stock_levels
            ORDER BY location_code, sku
        ''')
        return [dict(row) for row in cursor.fetchall()]


def get_stock_level(location_code: str, sku: str) -> Optional[Dict]:
    """Get stock level for a specific product at a location"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT location_code, sku, product_name, quantity, last_updated
            FROM stock_levels
            WHERE location_code = ? AND sku = ?
        ''', (location_code, sku))
        row = cursor.fetchone()
        return dict(row) if row else None


def check_order_availability(order_number: str) -> Dict:
    """Check if an order can be fulfilled based on stock levels"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get order
        order = get_order_by_number(order_number)
        if not order:
            return {'available': False, 'reason': 'Order not found'}

        location_code = order['location_code']
        available_items = []
        unavailable_items = []

        for item in order['items']:
            stock = get_stock_level(location_code, item['sku'])

            if not stock:
                unavailable_items.append({
                    'sku': item['sku'],
                    'product_name': item['product_name'],
                    'required': item['quantity'],
                    'available': 0,
                    'reason': 'No stock information'
                })
            elif stock['quantity'] < item['quantity']:
                unavailable_items.append({
                    'sku': item['sku'],
                    'product_name': item['product_name'],
                    'required': item['quantity'],
                    'available': stock['quantity'],
                    'reason': 'Insufficient stock'
                })
            else:
                available_items.append({
                    'sku': item['sku'],
                    'product_name': item['product_name'],
                    'required': item['quantity'],
                    'available': stock['quantity']
                })

        return {
            'order_number': order_number,
            'location_code': location_code,
            'available': len(unavailable_items) == 0,
            'available_items': available_items,
            'unavailable_items': unavailable_items
        }
