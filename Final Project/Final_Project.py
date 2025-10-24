import sqlite3
import os
from datetime import datetime

DB_NAME = "foodloop.db"

# ------------------ DATABASE SETUP ------------------
def init_db():
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
    username = input("?? Enter new username: ")
    password = input("?? Enter password: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"? User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("?? That username already exists.")
    conn.close()

def login():
    username = input("?? Username: ")
    password = input("?? Password: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        print(f"? Welcome, {username}!")
        return username
    else:
        print("? Incorrect username or password.")
        return None

# ------------------ INVENTORY SYSTEM ------------------
def add_food(user):
    name = input("?? Food name: ")
    area = input("?? Area: ")
    expiration = input("?? Expiration date (YYYY-MM-DD): ")
    quantity = input("?? Quantity: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, area, expiration, quantity, owner) VALUES (?, ?, ?, ?, ?)",
              (name, area, expiration, quantity, user))
    conn.commit()
    conn.close()
    print("? Food item added successfully!")

def show_inventory():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM inventory ORDER BY expiration ASC")
    items = c.fetchall()
    conn.close()

    print("\n?? --- Available Food ---")
    if not items:
        print("No food donations available yet.")
    else:
        for item in items:
            print(f"[{item[0]}] {item[1]} | Area: {item[2]} | Exp: {item[3]} | Qty: {item[4]} | Donor: {item[5]}")
    print("------------------------\n")

# ------------------ CHAT SYSTEM ------------------
def send_message(user):
    message = input("?? Type your message: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO chat (user, message, timestamp) VALUES (?, ?, ?)", (user, message, timestamp))
    conn.commit()
    conn.close()
    print("? Message sent!")

def show_chat():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM chat ORDER BY id DESC LIMIT 10")
    messages = c.fetchall()
    conn.close()

    print("\n?? --- Chat Messages ---")
    for msg in reversed(messages):
        print(f"{msg[3]} | {msg[1]}: {msg[2]}")
    print("-----------------------\n")

# ------------------ MAIN MENU ------------------
def main_menu(user):
    while True:
        print(f"\n?? Welcome {user}! Choose an option:")
        print("1??  Add food to inventory")
        print("2??  View available food")
        print("3??  Send chat message")
        print("4??  View chat messages")
        print("5??  Log out")

        choice = input("?? Enter your choice: ")

        if choice == '1':
            add_food(user)
        elif choice == '2':
            show_inventory()
        elif choice == '3':
            send_message(user)
        elif choice == '4':
            show_chat()
        elif choice == '5':
            print("?? Logged out.\n")
            break
        else:
            print("?? Invalid option, please try again.")

# ------------------ APP ENTRY ------------------
def main():
    init_db()
    while True:
        print("\n???  FOOD LOOP - Helping Monterrey reduce food waste")
        print("1??  Log in")
        print("2??  Sign up")
        print("3??  Exit")
        option = input("?? Choose an option: ")

        if option == '1':
            user = login()
            if user:
                main_menu(user)
        elif option == '2':
            signup()
        elif option == '3':
            print("?? Goodbye!")
            break
        else:
            print("?? Invalid option.")

if __name__ == "__main__":
    main()

