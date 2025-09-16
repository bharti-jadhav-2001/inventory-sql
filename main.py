import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def list_items():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, quantity FROM items')
    items = cursor.fetchall()
    conn.close()
    if not items:
        print("Inventory is empty.")
    else:
        print("Current Inventory:")
        for item in items:
            print(f"- {item[0]}: {item[1]}")

def add_item():
    name = input("Enter item name: ")
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Invalid quantity. Please enter a number.")

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO items (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        print(f"Added '{name}' to inventory.")
    except sqlite3.IntegrityError:
        print(f"Item '{name}' already exists. Use 'Update Item' to change quantity.")
    conn.close()

def update_quantity():
    name = input("Enter item name to update: ")
    while True:
        try:
            quantity = int(input("Enter new quantity: "))
            break
        except ValueError:
            print("Invalid quantity. Please enter a number.")

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET quantity = ? WHERE name = ?', (quantity, name))
    if cursor.rowcount == 0:
        print(f"Item '{name}' not found.")
    else:
        conn.commit()
        print(f"Updated '{name}' quantity to {quantity}.")
    conn.close()

def remove_item():
    name = input("Enter item name to remove: ")
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE name = ?', (name,))
    if cursor.rowcount == 0:
        print(f"Item '{name}' not found.")
    else:
        conn.commit()
        print(f"Removed '{name}' from inventory.")
    conn.close()

def main():
    init_db()
    while True:
        print("\nInventory Management Menu:")
        print("1. List all items")
        print("2. Add a new item")
        print("3. Update item quantity")
        print("4. Remove an item")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            list_items()
        elif choice == '2':
            add_item()
        elif choice == '3':
            update_quantity()
        elif choice == '4':
            remove_item()
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()