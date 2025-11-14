
import sqlite3
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DB_NAME = "foodloop.db"

# ------------------ DATABASE SETUP ------------------
def init_db():
    """Initialize the SQLite database and create necessary tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    area TEXT NOT NULL,
                    expiration TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    owner TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS chat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )''')

    conn.commit()
    conn.close()

# ------------------ USER SYSTEM ------------------
def signup():
    """Register a new user in the system."""
    username = input("Enter new username: ")
    password = input("Enter password: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("That username already exists.")
    conn.close()


def login():
    """Authenticate an existing user."""
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        print(f"Welcome, {username}!")
        return username
    else:
        print("Incorrect username or password.")
        return None

# ------------------ INPUT VALIDATION ------------------
def validate_date(date_str):
    """Check if a date is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_quantity(quantity_str):
    """Check if a quantity is a valid positive integer."""
    return quantity_str.isdigit() and int(quantity_str) > 0

# ------------------ INVENTORY SYSTEM ------------------
def add_food(user):
    """Add a new food item to the inventory after validating inputs."""
    name = input("Food name: ")
    area = input("Area: ")

    expiration = input("Expiration date (YYYY-MM-DD): ")
    while not validate_date(expiration):
        expiration = input("Invalid date format. Please use YYYY-MM-DD: ")

    quantity = input("Quantity: ")
    while not validate_quantity(quantity):
        quantity = input("Invalid number. Please enter a positive integer: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, area, expiration, quantity, owner) VALUES (?, ?, ?, ?, ?)",
              (name, area, expiration, int(quantity), user))
    conn.commit()
    conn.close()
    print("Food item added successfully!")


def show_inventory():
    """Display all available food items sorted by expiration date."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM inventory ORDER BY expiration ASC")
    items = c.fetchall()
    conn.close()

    print("\n--- Available Food ---")
    if not items:
        print("No food donations available yet.")
    else:
        for item in items:
            print(f"[{item[0]}] {item[1]} | Area: {item[2]} | Exp: {item[3]} | Qty: {item[4]} | Donor: {item[5]}")
    print("------------------------\n")


def expiration_alerts():
    """Show items that will expire within the next 3 days."""
    today = datetime.now().date()
    threshold = today + timedelta(days=3)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, expiration, owner FROM inventory")
    items = c.fetchall()
    conn.close()

    print("\n--- Expiration Alerts ---")
    found = False
    for name, exp_str, owner in items:
        exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
        if today <= exp_date <= threshold:
            print(f"⚠️  {name} (by {owner}) expires on {exp_date}")
            found = True
    if not found:
        print("No items expiring soon.")
    print("-------------------------\n")


def search_inventory():
    """Search food inventory by area, expiration date, or donor."""
    print("\nSearch options:")
    print("1. By area")
    print("2. By expiration date")
    print("3. By donor")
    choice = input("Enter choice: ")

    query = "SELECT * FROM inventory WHERE "
    params = ()

    if choice == '1':
        area = input("Enter area: ")
        query += "area LIKE ?"
        params = (f"%{area}%",)
    elif choice == '2':
        date = input("Enter expiration date (YYYY-MM-DD): ")
        while not validate_date(date):
            date = input("Invalid format. Enter expiration date (YYYY-MM-DD): ")
        query += "expiration=?"
        params = (date,)
    elif choice == '3':
        donor = input("Enter donor name: ")
        query += "owner LIKE ?"
        params = (f"%{donor}%",)
    else:
        print("Invalid choice.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, params)
    results = c.fetchall()
    conn.close()

    print("\n--- Search Results ---")
    if not results:
        print("No matches found.")
    else:
        for item in results:
            print(f"[{item[0]}] {item[1]} | Area: {item[2]} | Exp: {item[3]} | Qty: {item[4]} | Donor: {item[5]}")
    print("----------------------\n")


def plot_donations_by_area():
    """Generate a bar chart showing total donations per area."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT area, SUM(quantity) FROM inventory GROUP BY area")
    data = c.fetchall()
    conn.close()

    if not data:
        print("No data available for visualization.")
        return

    areas, totals = zip(*data)
    plt.bar(areas, totals)
    plt.title("Total Items Donated by Area")
    plt.xlabel("Area")
    plt.ylabel("Total Quantity")
    plt.show()

    # ----------- PICK UP FOOD -----------
def pickup_food_item():
    item_id = input("Enter the ID of the item to pick up: ")

    if not item_id.isdigit():
        print("Invalid ID. Must be a number.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Check item exists
    c.execute("SELECT name, quantity FROM inventory WHERE id=?", (item_id,))
    item = c.fetchone()

    if not item:
        print("Item not found.")
        conn.close()
        return

    name, current_qty = item
    print(f"\n{name} currently has quantity: {current_qty}")

    pickup_qty = input("How many units were picked up? ")

    if not pickup_qty.isdigit() or int(pickup_qty) <= 0:
        print("Invalid quantity.")
        conn.close()
        return

    pickup_qty = int(pickup_qty)

    if pickup_qty > current_qty:
        print("Cannot pick up more than available.")
        conn.close()
        return

    # Calculate new quantity
    new_qty = current_qty - pickup_qty

    if new_qty == 0:
        c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        print("All units picked up — item removed from inventory.")
    else:
        c.execute("UPDATE inventory SET quantity=? WHERE id=?", (new_qty, item_id))
        print(f"Pickup recorded. New quantity: {new_qty}")

    conn.commit()
    conn.close()
# ------------------ CHAT SYSTEM ------------------
def send_message(user):
    """Add a chat message with a timestamp."""
    message = input("Type your message: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO chat (user, message, timestamp) VALUES (?, ?, ?)", (user, message, timestamp))
    conn.commit()
    conn.close()
    print("Message sent!")


def show_chat():
    """Display the 10 most recent chat messages."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM chat ORDER BY id DESC LIMIT 10")
    messages = c.fetchall()
    conn.close()

    print("\n--- Chat Messages ---")
    for msg in reversed(messages):
        print(f"{msg[3]} | {msg[1]}: {msg[2]}")
    print("-----------------------\n")

# ------------------ MAIN MENU ------------------
def main_menu(user):
    """Display the main menu for logged-in users."""
    while True:
        print(f"\nWelcome {user}! Choose an option:")
        print("1.  Add food to inventory")
        print("2.  View available food")
        print("3.  View items expiring soon")
        print("4.  Search inventory")
        print("5.  Data visualization")
        print("6.  Send chat message")
        print("7.  View chat messages")
        print("8   Pick up food")
        print("9.  Log out")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_food(user)
        elif choice == '2':
            show_inventory()

        elif choice == '3':
            expiration_alerts()
        elif choice == '4':
            search_inventory()
        elif choice == '5':
            plot_donations_by_area()
        elif choice == '6':
            send_message(user)
        elif choice == '7':
            show_chat()
        elif choice == '8':
            pickup_food_item()
        elif choice == '9':
            print("Logged out.\n")
            break
        else:
            print("Invalid option, please try again.")

# ------------------ APP ENTRY ------------------
def main():
    """Start the FoodLoop app."""
    init_db()
    while True:
        print("\n--- FOOD LOOP - Helping Monterrey Reduce Food Waste ---")
        print("1. Log in")
        print("2. Sign up")
        print("3. Exit")
        option = input("Choose an option: ")

        if option == '1':
            user = login()
            if user:
                main_menu(user)
        elif option == '2':
            signup()
        elif option == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
