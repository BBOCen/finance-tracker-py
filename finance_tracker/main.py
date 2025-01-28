"""
This program is a simple personal finance tracker that allows users to manage their expenses and income.
Through a menu, users can input their financial data, including various expense categories
and income details. The data is stored in a MySQL database, enabling persistent tracking across
sessions. Additionally, the program utilizes matplotlib to visually display the expenses by category.
"""

import mysql.connector
import matplotlib.pyplot as plt

# MySQL DB Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_tracker"
    )


# Add expense to database
def add_expense(amount, category, description):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO expenses (amount, category, description) VALUES (%s, %s, %s)"
    cursor.execute(query, (amount, category, description))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Expense of {amount} added.")


# Add income to database
def add_income(amount, description):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO income (amount, description) VALUES (%s, %s)"
    cursor.execute(query, (amount, description))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Income of {amount} added.")


# View expenses and income
def view_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print(f"Total Expenses: {total_expenses}")
    print(f"Total Income: {total_income}")
    print(f"Balance: {total_income - total_expenses}")


# Visualize expense categories
def visualise_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts, color="blue")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.title("Expenses by Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    cursor.close()
    conn.close()


# Main menu to interact with the application

exit_menu = False

while not exit_menu:
    print("--- Personal Finance Tracker ---")
    print("1. Add Expense")
    print("2. Add Income")
    print("3. View Summary")
    print("4. Visualise Expenses by Category")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        amount = float(input("Enter expense amount: "))
        category = input("Enter expense category (e.g., food, entertainment, bills): ")
        description = input("Enter expense description: ")
        add_expense(amount, category, description)

    elif choice == "2":
        amount = float(input("Enter income amount: "))
        description = input("Enter income description: ")
        add_income(amount, description)

    elif choice == "3":
        view_summary()

    elif choice == "4":
        visualise_expenses()

    elif choice == "5":
        exit_menu = True

    else:
        print("Invalid choice, please try again.")
