"""
Reset database script for System B
Clears and repopulates the database with mock data
"""
import os
import sqlite3
import database as db
from datetime import datetime, timedelta

def reset_database():
    """Clear and reset database with mock data"""
    # Remove existing database
    if os.path.exists(db.DATABASE_PATH):
        os.remove(db.DATABASE_PATH)
        print(f"Removed existing database: {db.DATABASE_PATH}")

    # Initialize schema
    db.init_database()
    print("Initialized database schema")

    # Insert mock data
    conn = sqlite3.connect(db.DATABASE_PATH)
    cursor = conn.cursor()

    # Insert mock orders
    base_date = datetime.now() - timedelta(days=7)

    orders = [
        (
            'ORD-2024-001',
            'María González',
            'STORE001',
            'pending',
            (base_date + timedelta(days=0)).isoformat(),
            1299.98
        ),
        (
            'ORD-2024-002',
            'Juan Pérez',
            'STORE002',
            'pending',
            (base_date + timedelta(days=1)).isoformat(),
            159.99
        ),
        (
            'ORD-2024-003',
            'Ana Martínez',
            'STORE001',
            'processing',
            (base_date + timedelta(days=2)).isoformat(),
            489.97
        ),
        (
            'ORD-2024-004',
            'Carlos Rodríguez',
            'STORE003',
            'pending',
            (base_date + timedelta(days=3)).isoformat(),
            2199.95
        ),
        (
            'ORD-2024-005',
            'Laura Fernández',
            'STORE002',
            'completed',
            (base_date + timedelta(days=4)).isoformat(),
            679.98
        ),
        (
            'ORD-2024-006',
            'Miguel Sánchez',
            'STORE003',
            'pending',
            (base_date + timedelta(days=5)).isoformat(),
            124.99
        ),
    ]

    cursor.executemany(
        'INSERT INTO orders (order_number, customer_name, location_code, status, order_date, total_amount) VALUES (?, ?, ?, ?, ?, ?)',
        orders
    )
    print(f"Inserted {len(orders)} orders")

    # Insert order items
    order_items = [
        # ORD-2024-001 - María González
        (1, 'SKU001', 'Laptop HP ProBook 450', 1, 649.99),
        (1, 'SKU002', 'Mouse Logitech MX Master', 2, 49.99),
        (1, 'SKU004', 'Monitor Dell 24" Full HD', 2, 199.99),

        # ORD-2024-002 - Juan Pérez
        (2, 'SKU003', 'Teclado Mecánico Corsair K70', 1, 159.99),

        # ORD-2024-003 - Ana Martínez
        (3, 'SKU005', 'Webcam Logitech C920', 1, 89.99),
        (3, 'SKU002', 'Mouse Logitech MX Master', 2, 49.99),
        (3, 'SKU008', 'Disco Duro Externo 2TB', 3, 79.99),

        # ORD-2024-004 - Carlos Rodríguez
        (4, 'SKU001', 'Laptop HP ProBook 450', 2, 649.99),
        (4, 'SKU004', 'Monitor Dell 24" Full HD', 3, 199.99),
        (4, 'SKU006', 'Auriculares Sony WH-1000XM4', 1, 249.99),

        # ORD-2024-005 - Laura Fernández
        (5, 'SKU006', 'Auriculares Sony WH-1000XM4', 2, 249.99),
        (5, 'SKU008', 'Disco Duro Externo 2TB', 2, 79.99),

        # ORD-2024-006 - Miguel Sánchez
        (6, 'SKU005', 'Webcam Logitech C920', 1, 89.99),
        (6, 'SKU002', 'Mouse Logitech MX Master', 1, 49.99),
    ]

    cursor.executemany(
        'INSERT INTO order_items (order_id, sku, product_name, quantity, unit_price) VALUES (?, ?, ?, ?, ?)',
        order_items
    )
    print(f"Inserted {len(order_items)} order items")

    # Note: Stock levels will be empty initially - they should be populated by integration with System A
    print("Stock levels table is empty (will be populated via API from System A)")

    conn.commit()
    conn.close()

    print("\n✓ Database reset completed successfully!")
    print(f"  - Orders: {len(orders)}")
    print(f"  - Order items: {len(order_items)}")
    print(f"  - Stock levels: 0 (to be synchronized from System A)")


if __name__ == '__main__':
    reset_database()
