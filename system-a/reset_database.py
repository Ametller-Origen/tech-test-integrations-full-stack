"""
Reset database script for System A
Clears and repopulates the database with mock data
"""
import os
import sqlite3
import database as db

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

    # Insert locations
    locations = [
        ('WAREHOUSE', 'Almacén Central', 'warehouse'),
        ('STORE001', 'Tienda Centro', 'store'),
        ('STORE002', 'Tienda Norte', 'store'),
        ('STORE003', 'Tienda Sur', 'store'),
    ]

    cursor.executemany(
        'INSERT INTO locations (code, name, type) VALUES (?, ?, ?)',
        locations
    )
    print(f"Inserted {len(locations)} locations")

    # Insert products
    products = [
        ('SKU001', 'Laptop HP ProBook 450', 'Laptop profesional 15.6", Intel Core i5, 8GB RAM, 256GB SSD'),
        ('SKU002', 'Mouse Logitech MX Master', 'Mouse inalámbrico ergonómico de alta precisión'),
        ('SKU003', 'Teclado Mecánico Corsair K70', 'Teclado mecánico RGB con switches Cherry MX'),
        ('SKU004', 'Monitor Dell 24" Full HD', 'Monitor LED 24 pulgadas, resolución 1920x1080'),
        ('SKU005', 'Webcam Logitech C920', 'Webcam Full HD 1080p con micrófono estéreo'),
        ('SKU006', 'Auriculares Sony WH-1000XM4', 'Auriculares inalámbricos con cancelación de ruido'),
        ('SKU007', 'Impresora HP LaserJet Pro', 'Impresora láser monocromática, velocidad 40 ppm'),
        ('SKU008', 'Disco Duro Externo 2TB', 'Disco duro portátil USB 3.0, 2TB capacidad'),
    ]

    cursor.executemany(
        'INSERT INTO products (sku, name, description) VALUES (?, ?, ?)',
        products
    )
    print(f"Inserted {len(products)} products")

    # Insert inventory data
    # Warehouse has more stock, stores have limited stock
    inventory_data = [
        # Warehouse
        (1, 1, 50),  # WAREHOUSE - Laptop HP ProBook 450
        (1, 2, 120), # WAREHOUSE - Mouse Logitech
        (1, 3, 80),  # WAREHOUSE - Teclado Corsair
        (1, 4, 45),  # WAREHOUSE - Monitor Dell
        (1, 5, 95),  # WAREHOUSE - Webcam Logitech
        (1, 6, 65),  # WAREHOUSE - Auriculares Sony
        (1, 7, 30),  # WAREHOUSE - Impresora HP
        (1, 8, 110), # WAREHOUSE - Disco Duro

        # Store 001 - Centro
        (2, 1, 5),   # Laptop
        (2, 2, 15),  # Mouse
        (2, 3, 10),  # Teclado
        (2, 4, 8),   # Monitor
        (2, 5, 12),  # Webcam
        (2, 6, 7),   # Auriculares
        (2, 7, 3),   # Impresora
        (2, 8, 20),  # Disco Duro

        # Store 002 - Norte
        (3, 1, 3),   # Laptop
        (3, 2, 18),  # Mouse
        (3, 3, 8),   # Teclado
        (3, 4, 6),   # Monitor
        (3, 5, 10),  # Webcam
        (3, 6, 5),   # Auriculares
        (3, 7, 2),   # Impresora
        (3, 8, 15),  # Disco Duro

        # Store 003 - Sur
        (4, 1, 4),   # Laptop
        (4, 2, 20),  # Mouse
        (4, 3, 12),  # Teclado
        (4, 4, 7),   # Monitor
        (4, 5, 14),  # Webcam
        (4, 6, 6),   # Auriculares
        (4, 7, 2),   # Impresora
        (4, 8, 18),  # Disco Duro
    ]

    cursor.executemany(
        'INSERT INTO inventory (location_id, product_id, quantity) VALUES (?, ?, ?)',
        inventory_data
    )
    print(f"Inserted {len(inventory_data)} inventory records")

    conn.commit()
    conn.close()

    print("\n✓ Database reset completed successfully!")
    print(f"  - Locations: {len(locations)}")
    print(f"  - Products: {len(products)}")
    print(f"  - Inventory records: {len(inventory_data)}")


if __name__ == '__main__':
    reset_database()
