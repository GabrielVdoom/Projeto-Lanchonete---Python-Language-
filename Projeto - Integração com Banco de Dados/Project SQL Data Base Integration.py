# SQL Server table:

"""create table usuarios(
id_usuario int primary key identity,
usuário varchar(50) unique,
senha varchar(50)
)
"""

# Connection to SQL Server Database
import pyodbc

connection_data = (
    "Driver={SQL Server};"
    "Server=DESKTOP-15526VS;"
    "Database=BancoDeDados;"
)
connection = pyodbc.connect(connection_data)
cursor = connection.cursor()

def menu():
        print("\n\t\t\t\033[94m****** WELCOME ******\033[0m\n")
        print("\t\t\t- ENTER 1 TO REGISTER")
        print("\t\t\t- ENTER 2 TO LOGIN")
        print("\t\t\t- ENTER 3 TO DELETE USER")
        print("\t\t\t- ENTER 4 TO SHOW USERS AND PASSWORDS")
        print("\t\t\t- ENTER 'EXIT' TO EXIT THE PROGRAM")
        while True:
            choice = input("")
            if choice == "1":
                register()
                break
            elif choice == "2":
                login()
                break
            elif choice == "3":
                delete()
                break
            elif choice == "4":
                show_users()
                break
            elif choice == "5":
                edit_user()
                break
            elif choice.lower() == "exit":
                print("\033[96mPROGRAM ENDED\033[0m")
                break
            else:
                print("Invalid command, please enter again:")

def register():
        global username, password
        username = input("\nEnter a username to create your login: ").strip()
        while username == "":
            username = input("\nEmpty username, please enter a valid username to create your login:").strip()
        # Check if the entered username already exists in the database
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", username)
        existing_user = cursor.fetchone()
        # If it already exists, ask the user to enter another username
        while existing_user:
            print("\nUsername already exists...")
            username = input("\nEnter a username to create your login: ").strip()
            while username == "":
                username = input("\nEmpty username, please enter a valid username: ").strip()
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (username,))
            existing_user = cursor.fetchone()

        while True:
            password = input("Enter a password: ").strip()
            if password == "":
                print("\nEmpty password...\n")
            elif " " in password:
                print("\nPassword cannot contain spaces...\n")
            else:
                break
        # Insert username and password into the database
        command = f"insert into usuarios(usuario,senha) values ('{username}', '{password}')"
        cursor.execute(command)
        cursor.commit()
        print("\nCongratulations! User and password registered successfully!")
        print("Press ENTER to return to the menu...")
        input()
        menu()
        return

def login():
        # Check if the database has users
        cursor.execute('SELECT usuario,senha FROM usuarios')
        rows = cursor.fetchall()
        if not rows:
            print("No users registered, press ENTER to return to the menu...")
            input()
            menu()
            return
        username1 = input("\nEnter your username to log in: ").strip()
        # Check if the entered username exists
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", username1)
        existing_user = cursor.fetchone()
        # If the user does not exist, ask the user to enter a valid username
        while not existing_user:
            username1 = input("User not registered, enter a valid username, or press 3 to return to the menu:").strip()
            if username1 == "3":
                menu()
                return
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", username1)
            existing_user = cursor.fetchone()

        attempts = 0
        while True:
            password1 = input("Enter your password:").strip()
            cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", username1)
            stored_password = cursor.fetchone()
            # Check if the entered password matches
            if stored_password and stored_password[0] == password1:
                print(f"\nACCESS GRANTED, Welcome \033[34m{username1}\033[0m")
                print("Press any key to access the snack bar...")
                input()
                snack_bar_menu()
                return
            else:
                attempts += 1
                if attempts == 1:
                    print("\033[91mACCESS DENIED, TRY AGAIN, 3 attempts remaining...\n\033[0m")
                elif attempts == 2:
                    print("\033[91mACCESS DENIED, TRY AGAIN, 2 attempts remaining...\n\033[0m")
                elif attempts == 3:
                    print("\033[91mACCESS DENIED, TRY AGAIN, 1 attempt remaining...\n\033[0m")
                elif attempts == 4:
                    print("\033[91mACCESS BLOCKED")
                    break

def delete():
        delete_user = input("\nEnter the user you want to delete:").strip()
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", delete_user)
        existing_user = cursor.fetchone()

        while not existing_user:
            delete_user = input("\nUser not registered, enter a valid user, or press 3 to return to the menu:").strip()
            if delete_user == "3":
                menu()
                return
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", delete_user)
            existing_user = cursor.fetchone()

        password1 = input("Enter your password:").strip()
        cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", delete_user)
        stored_password = cursor.fetchone()

        if stored_password and stored_password[0] == password1:
            command = f"DELETE FROM usuarios WHERE usuario = '{delete_user}'"
            cursor.execute(command)
            connection.commit()

            print("\nUser deleted successfully. Press any key to return to the menu...")
            input()
            menu()
            return
        else:
            print("\nIncorrect password. User deletion cannot be performed.")
            menu()
            return

def snack_bar_menu():
        global total_price, unitCoxinha, unitPaodequeijo, unitRocambole, unitBatatafrita, unitHamburguer, unitRefrigerante, unitJuice
        total_price = 0
        unitCoxinha = 0
        unitPaodequeijo = 0
        unitRocambole = 0
        unitBatatafrita = 0
        unitHamburguer = 0
        unitRefrigerante = 0
        unitJuice = 0
        print("\n\t******Welcome to the Virtual Snack Bar******\n\n")

        print(" 1.Coxinha---------R$5.00")
        print(" 2.Cheese Bread----R$4.00")
        print(" 3.Rocambole-------R$5.50")
        print(" 4.French Fries----R$6.00")
        print(" 5.Hamburger-------R$5.00")
        print(" 6.Soda------------R$3.50")
        print(" 7.Juice-----------R$3.00\n\n")
        print("Enter your order, item by item (max 20 items), press 0 to finish your order and go to Payment method, enter 'back' to return to the main menu...")

        for i in range(100):
            product_choice = input("")
            if product_choice.lower().strip() in ["coxinha", "1"]:
                unitCoxinha += 1
                total_price += 5
            elif product_choice.lower().strip() in ["cheese bread", "2"]:
                unitPaodequeijo += 1
                total_price += 4
            elif product_choice.lower().strip() in ["rocambole", "3"]:
                unitRocambole += 1
                total_price += 5.5
            elif product_choice.lower().strip() in ["french fries", "4"]:
                unitBatatafrita += 1
                total_price += 6
            elif product_choice.lower().strip() in ["hamburger", "5"]:
                unitHamburguer += 1
                total_price += 5
            elif product_choice.lower().strip() in ["soda", "6"]:
                unitRefrigerante += 1
                total_price += 3.5
            elif product_choice.lower().strip() in ["juice", "7"]:
                unitJuice += 1
                total_price += 3
            elif product_choice.lower().strip() == "0":
                cart()
                return
            elif product_choice.lower().strip() == "back":
                menu()
                return
            else:
                print("Item not registered, enter again:")

def cart():
        global paymentMethod, changeValue
        changeValue = 0
        print("\n***CART***")
        if (unitCoxinha == 1):
            print(unitCoxinha, "Coxinha")
        elif (unitCoxinha > 1):
            print(unitCoxinha, "Coxinhas")
        if (unitPaodequeijo == 1):
            print(unitPaodequeijo, "Cheese Bread")
        elif (unitPaodequeijo > 1):
            print(unitPaodequeijo, "Cheese Breads")
        if (unitRocambole == 1):
            print(unitRocambole, "Rocambole")
        elif (unitRocambole > 1):
            print(unitRocambole, "Rocamboles")
        if (unitBatatafrita == 1):
            print(unitBatatafrita, "French Fries")
        elif (unitBatatafrita > 1):
            print(unitBatatafrita, "French Fries")
        if (unitHamburguer == 1):
            print(unitHamburguer, "Hamburger")
        elif (unitHamburguer > 1):
            print(unitHamburguer, "Hamburgers")
        if (unitRefrigerante == 1):
            print(unitRefrigerante, "Soda")
        elif (unitRefrigerante > 1):
            print(unitRefrigerante, "Sodas")
        if (unitJuice == 1):
            print(unitJuice, "Juice")
        elif (unitJuice > 1):
            print(unitJuice, "Juices")
        print(f"\nTotal to pay: R${total_price}")
        print("\n\nPayment method:")
        paymentMethod = input("1-Cash\n2-Credit Card\n3-Debit Card\n\n")
        while paymentMethod not in ["1", "2", "3"]:
            paymentMethod = input("Invalid command, choose a number corresponding to your payment method:\n\n1-Cash\n2-Credit Card\n3-Debit Card\n\n")
        if paymentMethod == "1":
            changeOption = input("\n1-Change\n2-No Change\n\n")
            while changeOption not in ["1", "2"]:
                changeOption = input("\nInvalid command\n1-Change\n2-No Change\n")
            if changeOption == "1":
                changeValue = input("\nChange for how much?\n")
                while True:
                    try:
                        changeValue = float(changeValue)
                        if changeValue < total_price:
                            changeValue = input("Insufficient cash, enter again:\n")
                        else:
                            break
                    except ValueError:
                        changeValue = input("Invalid command, enter a number:\n")

                changeValue = float(changeValue) - total_price
                askAddress()
                return
            elif changeOption == "2":
                askAddress()
                return

        else:
            askAddress()
            return

def askAddress():
        deliveryAddress = []
        print("\nEnter your delivery address:\n")
        city = input("CITY:").strip()
        while city.strip() == "":
            city = input("Required field, CITY:")
        deliveryAddress.append(city)
        neighborhood = input("NEIGHBORHOOD:").strip()
        while neighborhood.strip() == "":
            neighborhood = input("Required field, NEIGHBORHOOD:")
        deliveryAddress.append(neighborhood)
        streetName = input("STREET NAME:").strip()
        while streetName.strip() == "":
            streetName = input("Required field, STREET NAME:")
        deliveryAddress.append(streetName)
        number = input("NUMBER:").strip()
        while number.strip() == "":
            number = input("Required field, NUMBER:")
        deliveryAddress.append(number)
        print("\nORDER PLACED!\n")
        print("**Order Summary**")
        if (unitCoxinha == 1):
            print(f"--{unitCoxinha} Coxinha")
        elif (unitCoxinha > 1):
            print(f"--{unitCoxinha} Coxinhas")
        if (unitPaodequeijo == 1):
            print(f"--{unitPaodequeijo} Cheese Bread")
        elif (unitPaodequeijo > 1):
            print(f"--{unitPaodequeijo} Cheese Breads")
        if (unitRocambole == 1):
            print(f"--{unitRocambole} Rocambole")
        elif (unitRocambole > 1):
            print(f"--{unitRocambole} Rocamboles")
        if (unitBatatafrita == 1):
            print(f"--{unitBatatafrita} French Fries")
        elif (unitBatatafrita > 1):
            print(f"--{unitBatatafrita} French Fries")
        if (unitHamburguer == 1):
            print(f"--{unitHamburguer} Hamburger")
        elif (unitHamburguer > 1):
            print(f"--{unitHamburguer} Hamburgers")
        if (unitRefrigerante == 1):
            print(f"--{unitRefrigerante} Soda")
        elif (unitRefrigerante > 1):
            print(f"--{unitRefrigerante} Sodas")
        if (unitJuice == 1):
            print(f"--{unitJuice} Juice")
        elif (unitJuice > 1):
            print(f"--{unitJuice} Juices")

        print("\nPayment method:")
        if paymentMethod == "1":
            print("--Cash")
        elif paymentMethod == "2":
            print("--Credit Card")
        elif paymentMethod == "3":
            print("--Debit Card")

        if (changeValue > 0):
            print(f"\nChange: R${changeValue}")
        print("\nAddress: {}, {}, {}, {}.".format(*deliveryAddress))


def show_users():
        cursor.execute('SELECT usuario,senha FROM usuarios')
        rows = cursor.fetchall()
        if not rows:
            print("No users registered, press ENTER to return to the menu...")
            input()
            menu()
            return
        else:
            print("USERS AND PASSWORDS:\n")
            for row in rows:
                user = row[0]
                password = row[1]
                print(f"USUÁRIO = {user}")
                print(f"SENHA = {'*' * len(password)}\n")
        print("Press ENTER to return to the menu...")
        input()
        menu()
        return

def edit_user():
    user_to_change = input("\nEnter the user you want to edit: ")
    cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", user_to_change)
    user_exists = cursor.fetchone()

    # If it doesn't exist, ask to enter another user
    while not user_exists:
        user_to_change = input("User not registered, enter a valid user, or press 3 to return to the menu:")
        if user_to_change == "3":
            menu()
            return
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", user_to_change)
        user_exists = cursor.fetchone()

    password = input("Enter the password: ")
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", user_to_change)
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == password:
        new_user = input("Enter the new username: ")
        cursor.execute("UPDATE usuarios SET usuario = ? WHERE usuario = ?", new_user, user_to_change)
        connection.commit()
        print("\nUser changed successfully. Press any key to return to the menu...")
        input()
        menu()
        return
    else:
        print("Incorrect password. User change cannot be performed.")
        menu()
        return

menu()
