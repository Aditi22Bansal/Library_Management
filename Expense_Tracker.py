from colorama import init, Fore, Style
import mysql.connector as abc

# Initialize colorama (required on Windows)
init(autoreset=True)

mycon = abc.connect(host="localhost", user="root", passwd="Aditi@2203", database="school")
cursor = mycon.cursor()

def is_registered(cursor, username, password):
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None

def register_user(cursor, name, username, password, balance, savings):
    query = "INSERT INTO users (name, username, password, balance, savings) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, username, password, balance, savings))

def update_user_info(cursor, username, password):
    print("\n** UPDATE USER INFORMATION **")
    print(f"{Fore.YELLOW}1. Change Name")
    print(f"{Fore.YELLOW}2. Change Password")
    print(f"{Fore.YELLOW}3. Change Savings Goal")
    print(f"{Fore.YELLOW}4. Go Back")

    choice = int(input(f"{Fore.GREEN}Choose an option: "))
    
    if choice == 1:
        new_name = input(f"{Fore.YELLOW}Enter your new name: ")
        query_update_name = "UPDATE users SET name = %s WHERE username = %s AND password = %s"
        cursor.execute(query_update_name, (new_name, username, password))
        print(f"{Fore.GREEN}Name updated successfully!")

    elif choice == 2:
        new_password = input(f"{Fore.YELLOW}Enter your new password: ")
        query_update_password = "UPDATE users SET password = %s WHERE username = %s AND password = %s"
        cursor.execute(query_update_password, (new_password, username, password))
        print(f"{Fore.GREEN}Password updated successfully!")

    elif choice == 3:
        new_savings_goal = float(input(f"{Fore.YELLOW}Enter your new savings goal: "))
        query_update_savings = "UPDATE users SET savings = %s WHERE username = %s AND password = %s"
        cursor.execute(query_update_savings, (new_savings_goal, username, password))
        print(f"{Fore.GREEN}Savings goal updated successfully!")

    elif choice == 4:
        return

    else:
        print(f"{Fore.RED}Invalid option. Please choose a valid option.")


def deduct_money(cursor, username, category, amount):
    query = "INSERT INTO expenses (username, expense_category, expense_amount) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, category, amount))
    print(f"{Fore.GREEN}Expense recorded successfully!")


def display_most_expensive_category(cursor, username):
    query = "SELECT expense_category, SUM(expense_amount) as total_amount FROM expenses WHERE username = %s GROUP BY expense_category ORDER BY total_amount DESC LIMIT 1"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        category, total_amount = result
        print(f"{Fore.CYAN}The category where you have spent the most is: {category} (Total amount: {total_amount})")
    else:
        print(f"{Fore.CYAN}You haven't made any expenses yet.")


while True:
    try:
        print(f"{Fore.CYAN}~~*")
        print(f"{Fore.YELLOW}CASHFLOW COMPANION - Expense Tracker")
        print()
        print(f"{Fore.MAGENTA}  :) Your Pockets Best Friend!")
        print()
        print(f"{Fore.CYAN}~~*")

        choice = int(input(f"{Fore.GREEN}Press 1 if registered, press 0 if not registered: "))
        if choice == 1:
            username = input(f"{Fore.YELLOW}Enter your username: ")
            password = input(f"{Fore.YELLOW}Enter your password: ")

            if is_registered(cursor, username, password):
                print(f"{Fore.GREEN}Welcome back!")

                query_balance = "SELECT balance FROM users WHERE username = %s AND password = %s"
                cursor.execute(query_balance, (username, password))
                user_balance = cursor.fetchone()[0]
                print(f"{Fore.CYAN}Your Bank Balance: {user_balance}")

                expense_categories = [
                    "Groceries", "Food", "Gifts", "Tax", "Petrol", "Stationary", "Personal Items", "Miscellaneous"
                ]

                while True:
                    print(f"{Fore.CYAN}Options:")
                    print(f"{Fore.YELLOW}1. Add money")
                    print(f"{Fore.YELLOW}2. Deduct money")
                    print(f"{Fore.YELLOW}3. Display Savings Report")
                    print(f"{Fore.YELLOW}4. Update User Information")
                    print(f"{Fore.YELLOW}5. Exit")

                    option = int(input(f"{Fore.GREEN}Choose an option: "))

                    if option == 1:
                        amount = float(input(f"{Fore.YELLOW}Enter the amount to add: "))
                        query_add_money = "UPDATE users SET balance = balance + %s WHERE username = %s AND password = %s"
                        cursor.execute(query_add_money, (amount, username, password))
                        print(f"{Fore.GREEN}Money added successfully!")

                    elif option == 2:
                        print(f"{Fore.YELLOW}Expense Categories:")
                        for i, category in enumerate(expense_categories, 1):
                            print(f"{Fore.YELLOW}{i}. {category}")
                        choice = int(input(f"{Fore.GREEN}Choose an expense category: "))
                        if 1 <= choice <= len(expense_categories):
                            amount_to_deduct = float(input(f"{Fore.YELLOW}Enter the amount to deduct: "))
                            if 0 < amount_to_deduct <= user_balance:
                                deduct_money(cursor, username, expense_categories[choice - 1], amount_to_deduct)
                                query_deduct_money = "UPDATE users SET balance = balance - %s WHERE username = %s AND password = %s"
                                cursor.execute(query_deduct_money, (amount_to_deduct, username, password))
                                print(f"{Fore.GREEN}Money deducted successfully!")
                            else:
                                print(f"{Fore.RED}Insufficient funds. You don't have that much money.")

                        else:
                            print(f"{Fore.RED}Invalid category choice.")

                    elif option == 3:
                        query_savings_report = "SELECT name, username, balance, savings FROM users WHERE username = %s AND password = %s"
                        cursor.execute(query_savings_report, (username, password))
                        user_data = cursor.fetchone()

                        print(f"\n{Fore.YELLOW}** SAVINGS REPORT **")
                        print(f"{Fore.YELLOW}Name: {user_data[0]}")
                        print(f"{Fore.YELLOW}Username: {user_data[1]}")
                        print(f"{Fore.YELLOW}Bank Balance: {user_data[2]}")
                        print(f"{Fore.YELLOW}Savings: {user_data[3]}")

                        if user_data[2] < user_data[3]:
                            print(f"{Fore.RED}Warning: Your balance is less than your savings. Be cautious with your spending!")
                        else:
                            print(f"{Fore.GREEN}Congratulations! Your balance is greater than or equal to your savings. Keep it up!")

                        display_most_expensive_category(cursor, username)

                    elif option == 4:
                        update_user_info(cursor, username, password)

                    elif option == 5:
                        break

                    else:
                        print(f"{Fore.RED}Invalid option. Please choose a valid option.")

                break
            else:
                print(f"{Fore.RED}Incorrect username or password. Please try again.")

        elif choice == 0:
            while True:
                name = input(f"{Fore.YELLOW}Enter your name: ")
                username = input(f"{Fore.YELLOW}Enter a unique username: ")
                password = input(f"{Fore.YELLOW}Enter your password: ")
                balance = float(input(f"{Fore.YELLOW}Enter your bank balance: "))
                savings = float(input(f"{Fore.YELLOW}Enter your savings goal: "))

                if is_registered(cursor, username, password):
                    print(f"{Fore.RED}Username already exists. Please choose a different one.")
                else:
                    register_user(cursor, name, username, password, balance, savings)
                    print(f"{Fore.GREEN}Welcome,", name)
                    break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter either 0 or 1.")

    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a valid number.")

mycon.commit()
cursor.close()
mycon.close()
