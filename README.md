FoodLoop is a Python console application designed to help reduce food waste in Monterrey by allowing users to donate, find, and pick up surplus food. It includes a user system, an inventory manager, a search function, expiration alerts, and a simple chat feature. The program uses SQLite for local data storage and automatically creates all necessary tables.
Requirements
The application requires the following:
Python 3.8 or later
Matplotlib (mandatory for the data visualization feature)
No other external programs or tools are required
SQLite is included automatically with Python

To install Matplotlib, run:
pip install matplotlib

How to Run
Download or copy the foodloop.py file.
Open a terminal in the same folder.

Run the program with:
python foodloop.py

On the first launch, the program will automatically create the database file foodloop.db.

Features
User System
Register a new account
Log in with an existing account

Inventory Management
Add food items with name, area, expiration date, and quantity
View all available food organized by expiration date
Search by area, expiration date, or donor
Receive alerts for items expiring within 3 days
Pick up items, reducing quantity or removing them when they reach zero

Chat System
Send text messages to the shared chat
View the 10 most recent messages

Data Visualization
Display donation quantities grouped by area (requires Matplotlib)


Initial Impact
This early version demonstrates that the core idea of reducing food waste through community cooperation can be implemented with simple tools. The application already supports user accounts, food listings, communication, and basic tracking. Although features like password encryption, networking, and input hardening are not yet implemented, the project provides a solid foundation for future development.

Video explaining how to use the app
https://drive.google.com/file/d/1RcPvyKXpQi75dcjA3aQHvkDPtPWFM08n/view?usp=sharing
