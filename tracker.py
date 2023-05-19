import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt


def create_csv_file():
    if not os.path.exists('expenses.csv'):
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['description', 'cost', 'date'])


def add_expense(description, cost):
    date = datetime.now().strftime('%d-%m-%Y')
    with open('expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([description, cost, date])


def get_expenses():
    expenses = []
    with open('expenses.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            expense = {
                'description': row[0],
                'cost': float(row[1]),
                'date': datetime.strptime(row[2], '%d-%m-%Y').date()
            }
            expenses.append(expense)
    return expenses


def calculate_daily_totals(expenses):
    daily_totals = {}
    for expense in expenses:
        date = expense['date']
        cost = expense['cost']
        if date in daily_totals:
            daily_totals[date] += cost
        else:
            daily_totals[date] = cost

    result = []
    for date, total_cost in daily_totals.items():
        result.append({'date': date, 'total_cost': total_cost})

    return result


def plot_expenses(daily_totals, from_date='', to_date=''):
    from_date = datetime.strptime(from_date, '%d-%m-%Y').date() if from_date else ''
    to_date = datetime.strptime(to_date, '%d-%m-%Y').date() if to_date else ''

    dates = [data['date'] for data in daily_totals]
    total_costs = [data['total_cost'] for data in daily_totals]

    if from_date != '':
        dates = [date for date in dates if date >= from_date]
        total_costs = total_costs[dates.index(from_date):]
    if to_date != '':
        dates = [date for date in dates if date <= to_date]
        total_costs = total_costs[:dates.index(to_date) + 1]

    plt.figure(facecolor='dimgray')
    ax = plt.gca()
    ax.set_facecolor('lightgray')
    plt.plot(dates, total_costs, color='black', marker='o')
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel('Date')
    plt.ylabel('Total Cost')
    plt.title('Daily Total Costs')
    plt.xticks(rotation=45)
    plt.savefig("plot.png")


def main():
    while True:
        print("1. Add expense")
        print("2. View expenses")
        print("3. Plot expenses by date range")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter description: ")
            cost = float(input("Enter cost: "))
            add_expense(description, cost)
            print("Expense added successfully.")
        elif choice == "2":
            expenses = get_expenses()
            print("=====================")
            for expense in expenses:
                print(f"Description: {expense['description']}")
                print(f"Cost: {expense['cost']}")
                print(f"Date: {expense['date']}")
                print("=====================")
        elif choice == "3":
            from_date = str(input("Enter from date (dd-mm-yyyy): "))
            to_date = str(input("Enter to date (dd-mm-yyyy): "))
            plot_expenses(calculate_daily_totals(get_expenses()), from_date, to_date)
            return None
        elif choice == "4" or 'q':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
