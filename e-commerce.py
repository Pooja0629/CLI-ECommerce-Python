import mysql.connector as sql

# ---------- DATABASE CONNECTION ----------
def db_connect():
    return sql.connect(
        host="localhost",
        user="root",
        password="pooja2906",   # your password
        database="ecommerce_db"
    )

# ---------- ADMIN FUNCTIONS ----------
def add_product():
    db = db_connect()
    cur = db.cursor()

    name = input("Enter product name: ")
    price = int(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))

    cur.execute(
        "INSERT INTO products (product_name, price, stock) VALUES (%s, %s, %s)",
        (name, price, stock)
    )
    db.commit()
    print("✅ Product added successfully")

def update_product():
    db = db_connect()
    cur = db.cursor()

    pid = int(input("Enter product ID to update: "))
    new_price = int(input("Enter new price: "))
    new_stock = int(input("Enter new stock: "))

    cur.execute(
        "UPDATE products SET price=%s, stock=%s WHERE product_id=%s",
        (new_price, new_stock, pid)
    )
    db.commit()
    print("✅ Product updated successfully")

def delete_product():
    db = db_connect()
    cur = db.cursor()

    pid = int(input("Enter product ID to delete: "))
    cur.execute("DELETE FROM products WHERE product_id=%s", (pid,))
    db.commit()
    print("✅ Product deleted successfully")

def view_products():
    db = db_connect()
    cur = db.cursor()

    cur.execute("SELECT * FROM products")
    data = cur.fetchall()

    print("\n--- PRODUCT LIST ---")
    for p in data:
        print(f"ID:{p[0]}  Name:{p[1]}  Price:{p[2]}  Stock:{p[3]}")

# ---------- CUSTOMER FUNCTIONS ----------
def place_order():
    db = db_connect()
    cur = db.cursor()

    view_products()
    pid = int(input("\nEnter product ID to order: "))
    qty = int(input("Enter quantity: "))

    cur.execute("SELECT product_name, price, stock FROM products WHERE product_id=%s", (pid,))
    product = cur.fetchone()

    if product is None:
        print("❌ Product not found")
        return

    name, price, stock = product

    if qty > stock:
        print("❌ Not enough stock")
        return

    total = price * qty

    cur.execute(
        "INSERT INTO orders (product_name, quantity, total_price) VALUES (%s, %s, %s)",
        (name, qty, total)
    )

    cur.execute(
        "UPDATE products SET stock=stock-%s WHERE product_id=%s",
        (qty, pid)
    )

    db.commit()
    print(f"✅ Order placed! Total amount: ₹{total}")

def view_orders():
    db = db_connect()
    cur = db.cursor()

    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()

    print("\n--- ORDER HISTORY ---")
    for o in data:
        print(f"OrderID:{o[0]} Product:{o[1]} Qty:{o[2]} Total:{o[3]}")

# ---------- ADMIN MENU ----------
def admin_menu():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Add product")
        print("2. Update product")
        print("3. Delete product")
        print("4. View products")
        print("5. Logout")

        ch = int(input("Enter choice: "))

        if ch == 1:
            add_product()
        elif ch == 2:
            update_product()
        elif ch == 3:
            delete_product()
        elif ch == 4:
            view_products()
        elif ch == 5:
            break

# ---------- CUSTOMER MENU ----------
def customer_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. View products")
        print("2. Place order")
        print("3. View orders")
        print("4. Exit")

        ch = int(input("Enter choice: "))

        if ch == 1:
            view_products()
        elif ch == 2:
            place_order()
        elif ch == 3:
            view_orders()
        elif ch == 4:
            break

# ---------- MAIN ----------
def main():
    while True:
        print("\n====== E-COMMERCE SYSTEM ======")
        print("1. Admin Login")
        print("2. Customer")
        print("3. Exit")

        opt = int(input("Enter option: "))

        if opt == 1:
            pwd = input("Enter admin password: ")
            if pwd == "Zomato":
                admin_menu()
            else:
                print("❌ Wrong password")
        elif opt == 2:
            customer_menu()
        elif opt == 3:
            print("Thank you 🙌")
            break

main()
