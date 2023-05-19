import tkinter as tk
import datetime
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import ImageTk, Image
import tracker


def add_expense():
    description = description_entry.get()
    cost = float(cost_entry.get())

    tracker.add_expense(description, cost)
    messagebox.showinfo("Expense Tracker", "Expense added successfully.")


def view_expenses():
    expenses = tracker.get_expenses()
    expenses_text.delete(1.0, tk.END)

    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    tree = ttk.Treeview(view_frame, columns=("Description", "Cost", "Date"), show="headings")
    tree.column("Description", width=200)
    tree.column("Cost", width=100, anchor=tk.CENTER)
    tree.column("Date", width=100, anchor=tk.CENTER)

    tree.heading("Description", text="Description")
    tree.heading("Cost", text="Cost")
    tree.heading("Date", text="Date")

    total_cost = 0

    for expense in expenses:
        description = expense["description"]
        cost = expense["cost"]
        date = expense["date"]
        tree.insert("", tk.END, values=(description, cost, date))
        total_cost += cost

    tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(view_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    expenses_text.insert(tk.END, f"Date Generated - {current_date}\n")
    expenses_text.insert(tk.END, f"Total Cost: {total_cost}\n")


def plot_expenses():
    from_date = from_date_entry.get()
    to_date = to_date_entry.get()

    try:
        daily_totals = tracker.calculate_daily_totals(tracker.get_expenses())
        tracker.plot_expenses(daily_totals, from_date, to_date)

        plot_image = ImageTk.PhotoImage(Image.open("plot.png"))
        plot_label = tk.Label(window, image=plot_image)
        plot_label.pack()

        window.protocol("WM_DELETE_WINDOW", lambda: [window.destroy()])

        plot_label.image = plot_image

    except ValueError:
        messagebox.showerror("Expense Tracker", "Invalid date format. Please use dd-mm-yyyy.")


window = tk.Tk()
window.title("Expense Tracker")

# Add Expense Section
add_frame = tk.Frame(window)
add_frame.pack(pady=10)

description_label = tk.Label(add_frame, text="Description:")
description_label.grid(row=0, column=0, padx=5)
description_entry = tk.Entry(add_frame, width=30)
description_entry.grid(row=0, column=1, padx=5)

cost_label = tk.Label(add_frame, text="Cost:")
cost_label.grid(row=0, column=2, padx=5)
cost_entry = tk.Entry(add_frame, width=10)
cost_entry.grid(row=0, column=3, padx=5)

add_button = tk.Button(add_frame, text="Add Expense", command=add_expense)
add_button.grid(row=0, column=4, padx=5)

# View Expenses Section
view_frame = tk.Frame(window)
view_frame.pack(pady=10)

view_button = tk.Button(view_frame, text="View Expenses", command=view_expenses)
view_button.pack()

expenses_text = ScrolledText(view_frame, width=90, height=3,
                             font=('san francisco', 14))
expenses_text.pack(padx=10)

# Plot Expenses Section
plot_frame = tk.Frame(window)
plot_frame.pack(pady=10)

from_date_label = tk.Label(plot_frame, text="From Date:")
from_date_label.grid(row=0, column=0, padx=5)
from_date_entry = tk.Entry(plot_frame, width=10)
from_date_entry.grid(row=0, column=1, padx=5)

to_date_label = tk.Label(plot_frame, text="To Date:")
to_date_label.grid(row=0, column=2, padx=5)
to_date_entry = tk.Entry(plot_frame, width=10)
to_date_entry.grid(row=0, column=3, padx=5)

plot_button = tk.Button(plot_frame, text="Plot Expenses", command=plot_expenses)
plot_button.grid(row=0, column=4, padx=5)

window.mainloop()
