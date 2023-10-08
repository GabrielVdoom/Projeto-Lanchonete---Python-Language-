USERS = {}


def menu():
    print("\n\t\t\t\033[94m****** WELCOME ******\033[0m\n")
    print("\t\t\t- ENTER 1 TO REGISTER USER")
    print("\t\t\t- ENTER 2 TO LOG IN")
    print("\t\t\t- ENTER 3 TO DELETE USER")
    print("\t\t\t- ENTER 4 TO SHOW USERS AND PASSWORDS")
    print("\t\t\t- ENTER 'EXIT' TO QUIT THE PROGRAM")

    while True:
        choice = input("")
        if choice == "1":
            register_user()
            break
        elif choice == "2":
            login()
            break
        elif choice == "3":
            delete_user()
            break
        elif choice == "4":
            show_users()
            break
        elif choice.lower() == "exit":
            print("\033[96mPROGRAM TERMINATED\033[0m")
            break
        else:
            print("Invalid command, please enter a valid option:")


def register_user():
    global username, password
    while True:
        username = input("\nEnter a username to create your login: ").strip()
        if username == "":
            print("\nUsername is empty...")
        elif username in USERS:
            print("\nUsername already exists...")
        else:
            break

    while True:
        password = input("Enter a password: ").strip()
        if password == "":
            print("\nPassword is empty...\n")
        elif " " in password:
            print("\nPassword cannot contain spaces...\n")
        else:
            break

    USERS[username] = password
    print("\nWell done! User and password registered successfully!")
    print("Press ENTER to return to the menu...")
    input()
    menu()
    return


def login():
    username1 = input("\nTo log in, enter your username: ").strip()
    while len(USERS) == 0:
        print("\nNo registered users, press ENTER to return to the menu...")
        input()
        menu()
        return
    while username1 not in USERS:
        username1 = input("\nUser not registered, enter a valid username, or press 3 to return to the menu:").strip()
        if username1 == "3":
            menu()
            return

    attempts = 0
    while True:
        password1 = input("Enter your password: ").strip()
        if USERS[username1] == password1:
            print(f"\nACCESS GRANTED, Welcome \033[34m{username1}\033[0m")
            print("Press any key to access the Snack Bar...")
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
                print("\033[91mACCESS BLOCKED\n\033[0m")
                break


def delete_user():
    if len(USERS) == 0:
        print("No registered users, press ENTER to return to the menu...")
        input()
        menu()
        return
    delete_username = input("\nEnter the username you want to delete:").strip()
    while delete_username not in USERS:
        delete_username = input("\nUser does not exist, enter an existing username or press 3 to return to the menu:").strip()
        if delete_username == "3":
            menu()
            return
    del USERS[delete_username]
    print("\nUser deleted successfully, press a key to return to the menu...")
    input()
    menu()
    return


def snack_bar_menu():
    global total_price, unitChickenCoxinha, unitCheeseBread, unitSwissRoll, unitFrenchFries, unitHamburger, unitSoda, unitJuice
    total_price = 0
    unitChickenCoxinha = 0
    unitCheeseBread = 0
    unitSwissRoll = 0
    unitFrenchFries = 0
    unitHamburger = 0
    unitSoda = 0
    unitJuice = 0
    print("\n\t******Welcome to the Virtual Snack Bar******\n")

    print(" 1.Chicken Coxinha-----$5.00")
    print(" 2.Cheese Bread--------$4.00")
    print(" 3.Swiss Roll----------$5.50")
    print(" 4.French Fries--------$6.00")
    print(" 5.Hamburger-----------$5.00")
    print(" 6.Soda----------------$3.50")
    print(" 7.Juice---------------$3.00\n\n")
    print(
        "Enter your order, item by item (max 20 items), press 0 to finalize your order and go to Payment, enter 'back' to return to the main menu...")

    for i in range(100):
        product_choice = input("")
        if product_choice.lower().strip() in ["chicken coxinha", "1"]:
            unitChickenCoxinha += 1
            total_price += 5
        elif product_choice.lower().strip() in ["cheese bread", "2"]:
            unitCheeseBread += 1
            total_price += 4
        elif product_choice.lower().strip() in ["swiss roll", "3"]:
            unitSwissRoll += 1
            total_price += 5.5
        elif product_choice.lower().strip() in ["french fries", "4"]:
            unitFrenchFries += 1
            total_price += 6
        elif product_choice.lower().strip() in ["hamburger", "5"]:
            unitHamburger += 1
            total_price += 5
        elif product_choice.lower().strip() in ["soda", "6"]:
            unitSoda += 1
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
            print("Item not registered, please enter again:")


def cart():
    global payment_method, change_value
    change_value = 0
    print("\n***CART***")
    if unitChickenCoxinha == 1:
        print(unitChickenCoxinha, "Chicken Coxinha")
    elif unitChickenCoxinha > 1:
        print(unitChickenCoxinha, "Chicken Coxinhas")
    if unitCheeseBread == 1:
        print(unitCheeseBread, "Cheese Bread")
    elif unitCheeseBread > 1:
        print(unitCheeseBread, "Cheese Breads")
    if unitSwissRoll == 1:
        print(unitSwissRoll, "Swiss Roll")
    elif unitSwissRoll > 1:
        print(unitSwissRoll, "Swiss Rolls")
    if unitFrenchFries == 1:
        print(unitFrenchFries, "French Fries")
    elif unitFrenchFries > 1:
        print(unitFrenchFries, "French Fries")
    if unitHamburger == 1:
        print(unitHamburger, "Hamburger")
    elif unitHamburger > 1:
        print(unitHamburger, "Hamburgers")
    if unitSoda == 1:
        print(unitSoda, "Soda")
    elif unitSoda > 1:
        print(unitSoda, "Sodas")
    if unitJuice == 1:
        print(unitJuice, "Juice")
    elif unitJuice > 1:
        print(unitJuice, "Juices")

    print(f"\nTotal to pay: ${total_price}")
    print("\n\nPayment method:")

    payment_method = input("1-Cash\n2-Credit Card\n3-Debit Card\n\n")

    while payment_method not in ["1", "2", "3"]:
        payment_method = input(
            "Invalid command, choose a number corresponding to your payment method:\n\n1-Cash\n2-Credit Card\n3-Debit Card\n\n")

    if payment_method == "1":
        change_option = input("\n1-Change\n2-No Change\n\n")

        while change_option not in ["1", "2"]:
            change_option = input("\nInvalid command\n1-Change\n2-No Change\n")

        if change_option == "1":
            change_value_input = input("\nChange for how much?\n")

            while True:
                try:
                    change_value_input = float(change_value_input)
                    if change_value_input < total_price:
                        change_value_input = input("Insufficient money, please enter again:\n")
                    else:
                        break
                except ValueError:
                    change_value_input = input("Invalid command, enter a number:\n")

            change_value = float(change_value_input) - total_price
            ask_for_address()
            return
        elif change_option == "2":
            ask_for_address()
            return
    else:
        ask_for_address()
        return


def ask_for_address():
    delivery_address = []
    print("\nEnter your delivery address:\n")
    city = input("CITY:")

    while city.strip() == "":
        city = input("Mandatory field, CITY:")

    delivery_address.append(city)
    neighborhood = input("NEIGHBORHOOD:")

    while neighborhood.strip() == "":
        neighborhood = input("Mandatory field, NEIGHBORHOOD:")

    delivery_address.append(neighborhood)
    street_name = input("STREET NAME:")

    while street_name.strip() == "":
        street_name = input("Mandatory field, STREET NAME:")

    delivery_address.append(street_name)
    number = input("NUMBER:")

    while number.strip() == "":
        number = input("Mandatory field, NUMBER:")

    delivery_address.append(number)

    print("\nORDER PLACED!\n")
    print("**Order Summary**")

    if unitChickenCoxinha == 1:
        print(f"--{unitChickenCoxinha} Chicken Coxinha")
    elif unitChickenCoxinha > 1:
        print(f"--{unitChickenCoxinha} Chicken Coxinhas")

    if unitCheeseBread == 1:
        print(f"--{unitCheeseBread} Cheese Bread")
    elif unitCheeseBread > 1:
        print(f"--{unitCheeseBread} Cheese Breads")

    if unitSwissRoll == 1:
        print(f"--{unitSwissRoll} Swiss Roll")
    elif unitSwissRoll > 1:
        print(f"--{unitSwissRoll} Swiss Rolls")

    if unitFrenchFries == 1:
        print(f"--{unitFrenchFries} French Fries")
    elif unitFrenchFries > 1:
        print(f"--{unitFrenchFries} French Fries")

    if unitHamburger == 1:
        print(f"--{unitHamburger} Hamburger")
    elif unitHamburger > 1:
        print(f"--{unitHamburger} Hamburgers")

    if unitSoda == 1:
        print(f"--{unitSoda} Soda")
    elif unitSoda > 1:
        print(f"--{unitSoda} Sodas")

    if unitJuice == 1:
        print(f"--{unitJuice} Juice")
    elif unitJuice > 1:
        print(f"--{unitJuice} Juices")

    print("\nPayment method:")

    if payment_method == "1":
        print("--Cash")
    elif payment_method == "2":
        print("--Credit Card")
    elif payment_method == "3":
        print("--Debit Card")

    if change_value > 0:
        print(f"\nChange: ${change_value}")

    print("\nDelivery Address: {}, {}, {}, {}.".format(*delivery_address))


def show_users():
    print("USERS AND PASSWORDS:\n")

    if len(USERS) == 0:
        print("No registered users, press ENTER to return to the menu...")
        input()
        menu()
        return

    for key, value in USERS.items():
        value = "*" * len(value)
        print(f"USER = {key}\nPASSWORD = {value}\n")

    print("Press ENTER to return to the menu...")
    input()
    menu()
    return


menu()
