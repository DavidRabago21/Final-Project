General description of the project:
The project, called FoodLoop, is a Python-based console application designed to reduce food waste by connecting donors and recipients in Monterrey. It provides a simple text-based interface where users can register, log in, and share surplus food through an inventory system. Additionally, the app includes a basic chat function that allows users to communicate about donations. The program stores data locally using SQLite and automatically creates the necessary tables for users, food inventory, and chat messages.

Instructions to run the code:
To run the project, the user must have Python 3.8 or later installed. No external libraries are required since the program only uses built-in modules such as sqlite3, datetime, and os. After saving the file as foodloop.py, the user can open a terminal, navigate to the file’s directory, and run python foodloop.py. On the first execution, the script automatically generates a database file named foodloop.db. All interactions occur via command-line prompts, and data is saved persistently in the local database.

Features implemented to date:
The application currently includes a working user system that allows registration and login with unique usernames. It also has an inventory feature where users can add food items by specifying details such as name, area, expiration date, and quantity. The stored data can be viewed in an organized list sorted by expiration date. The chat feature enables users to send and view recent messages, fostering communication among participants. All data is managed through SQLite tables, ensuring basic data persistence between sessions.

Comment on the initial impact of the project:
This early version demonstrates a functional prototype capable of handling simple user accounts, food listings, and basic communication. Its impact lies in proving that the core idea—reducing food waste through community sharing—can be executed even with minimal technology. However, the current implementation lacks important elements like password encryption, input validation, and network connectivity, which limits its practical use. Despite these limitations, the project lays a solid foundation for future development into a more secure and scalable application.
foodloop.py

Video of how to use it
https://drive.google.com/file/d/11SGdrgMhjt_7UFe0Yn6O9VBJJToxp6EV/view?usp=drivesdk
