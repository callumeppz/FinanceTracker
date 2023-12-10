from FinanceTracker import Expense
import os
import datetime
import calendar

def main():
    print(f"Running Expense Tracker")
    expenseFilePath = "C:/Users/Callum Apps/Desktop/finance tracker/Expenses.csv"

    # calling functions
    # input for user expense
    expense = get_user_expense()
    # write to a file
    write_expense(expense, expenseFilePath)
    # read file and summarise
    summarise_expense(expenseFilePath)

    pass

#function allowing for userinput 
def get_user_expense():
        print(f"Enter Expenses")
        expenseName = input("Enter Expense Name: ")
        expenseAmount = float(input("Enter Expense Amount: "))
        print(f"{expenseAmount} Saving into {expenseName}")
        expenseCategories = [ "Food", "Rent", "Shopping", "Drinks", "Fun", "Misc", "Gifts" ]
    
        while True: # while loop, while input is true do this
            print("Select a category: ")
            for i, category_name in enumerate(expenseCategories):
                print(f"{i + 1}. {category_name}")

            value_range = f"[1 - {len(expenseCategories)}]"
            selected_index = int(input(f"Select Category Number {value_range}: ")) - 1


            if i in range(len(expenseCategories)): # if i is in range of expense (0-6)
                selectedCategory = expenseCategories[selected_index]
                newExpense = Expense(name = expenseName, amount= expenseAmount, category= selectedCategory)
                return newExpense
            else:
                print ("invalid selection")

            break

# function to write expenses to the csv

def write_expense(expense, expenseFilePath):
    print(f"Writing Expense {expense} to {expenseFilePath}")
    try:
        with open(expenseFilePath, "a") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n") # writing to the file
        print(f"Expense written to {expenseFilePath}")
    except Exception as e:
        print(f"Error writing to file: {e}") # exclaims if any errors whilst writing 


def summarise_expense(expenseFilePath):
    print(f"Summarising Expenses")
    expenses = []
    with open(expenseFilePath, "r") as f:
        lines = f.readlines()
        for line in lines:
            strippedline = line.strip()
            split_values = strippedline.split(",")
            print(split_values)
            if len(split_values) != 3:
                print(f"Issue with line: {strippedline}. Skipping...")
                continue  # Skip processing this line

            expenseName, expenseAmount, expenseCategory = split_values
            try:
                expenseAmount = float(expenseAmount)
                expenses.append(Expense(name=expenseName, category=expenseCategory, amount=expenseAmount))
                print(expenses[-1])  # Print the last added expense
            except ValueError:
                print(f"Could not convert amount to float: {expenseAmount}. Skipping...")
                continue  # Skip processing this line

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    for key, amount in amount_by_category.items():
        print (f"  {key}: ${amount:.2f}")

    # operators used to print budget for the month

    monthlybudget = 2000
    total_spent = sum([ex.amount for ex in expenses])
    print(green(f"total expenditure: ${total_spent:.2f}"))
    remainingbudget = monthlybudget - total_spent
    print(green(f"Budget Remaining for month: ${remainingbudget:.2f}"))

    now = datetime.datetime.now()
    days = calendar.monthrange(now.year, now.month)[1]
    remainingbudgetformonth = days - now.day
    remaininder = remainingbudget / days

    print(green(f"Remaining days in month: {remainingbudgetformonth} with a total spending of: ${remaininder:.2f} per day"))

def green(text): # functiion for green terminal text
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()