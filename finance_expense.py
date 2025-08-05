import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

# Global colors
EXPENSE_COLORS = [
    "#FFB3BA", "#FFD2B3", "#FFF4B3", "#B3E5FF", "#D4B3FF",
    "#E3B3FF", "#F7B3FF", "#E6FFFF", "#FFF9D6", "#FFE9B3",
    "#FADADD", "#FBE8EB", "#FFEDC2", "#FFF0F5", "#FFCCE5",
    "#FAF0DD", "#F3E5AB", "#ADD8E6", "#D6C8FF", "#F5CCFF"
]
INCOME_COLORS = [
    "#CFFFD0", "#B8F9B8", "#A8F0A8", "#98E998", "#88E788",
    "#78DD78", "#68D168", "#58C658", "#48BA48", "#38AD38"
]

class TrackerCSV(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Income vs Expense Pie Chart Tracker")
        self.configure(bg="#f0f0f0")
        self.csv_file = "data.csv"
        self.entries = []
        self.chart_open = False
        self.create_widgets()
        self.load_csv()  # Load existing data if CSV file is present

        # Resize window to fit all widgets
        self.update()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        self.resizable(False, False)

    def create_widgets(self):
        # Labels and input fields
        tk.Label(self, text="Date (YYYY-MM-DD)", bg=self["bg"]).grid(row=0, column=0)
        self.entry_date = tk.Entry(self)
        self.entry_date.grid(row=0, column=1)

        tk.Label(self, text="Category", bg=self["bg"]).grid(row=1, column=0)
        self.entry_cat = tk.Entry(self)
        self.entry_cat.grid(row=1, column=1)

        tk.Label(self, text="Amount", bg=self["bg"]).grid(row=2, column=0)
        self.entry_amt = tk.Entry(self)
        self.entry_amt.grid(row=2, column=1)

        tk.Label(self, text="Type", bg=self["bg"]).grid(row=3, column=0)
        self.combo_type = ttk.Combobox(self, values=["Expense", "Income"])
        self.combo_type.grid(row=3, column=1)
        self.combo_type.set("Expense")

        # Buttons
        tk.Button(self, text="Add Entry", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Delete Selected", command=self.delete_entry).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Import CSV", command=self.import_csv).grid(row=6, column=0, pady=5)
        tk.Button(self, text="Export CSV", command=self.export_csv).grid(row=6, column=1, pady=5)

        # Dropdown for filtering pie chart
        tk.Label(self, text="Chart Filter", bg=self["bg"]).grid(row=7, column=0, columnspan=2)
        self.filter_option = ttk.Combobox(self, values=["None", "Monthly", "Weekly"], justify="center", width=20)
        self.filter_option.set("None")
        self.filter_option.grid(row=8, column=0, columnspan=2, pady=2)

        tk.Button(self, text="Show Pie Chart", command=self.show_pie_chart).grid(row=9, column=0, columnspan=2, pady=5)

        # Treeview for displaying data table
        self.tree = ttk.Treeview(self, columns=("Date", "Category", "Amount", "Type"), show="headings")
        for col in ("Date", "Category", "Amount", "Type"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")
        self.tree.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    # Adds a new income or expense entry to the table
    def add_entry(self):
        date = self.entry_date.get().strip()
        category = self.entry_cat.get().strip()
        amount = self.entry_amt.get().strip()
        transaction_type = self.combo_type.get()

        if not date or not category or not amount or not transaction_type:
            messagebox.showerror("Missing", "Please fill all fields.")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Invalid", "Date must be in YYYY-MM-DD format.")
            return
        
        try:
            amount = float(amount)
        except Exception:
            messagebox.showerror("Invalid", "Amount must be a number.")
            return

        new_entry = [date, category, f"${amount:.2f}", transaction_type]
        self.entries.append(new_entry)
        self.update_tree()
        self.save_csv()
        self.entry_date.delete(0, tk.END)
        self.entry_cat.delete(0, tk.END)
        self.entry_amt.delete(0, tk.END)

    # Deletes selected entry from the table
    def delete_entry(self):
       select_item = self.tree.selection()

        if not select_item:
            messagebox.showerror("Invalid", "Please select a transaction to delete.")
            return
        
        for item in select_item:
            value = self.tree.item(item)['values']
            for i, entry in enumerate(self.entries):
                if list(entry) == list(value):
                    del self.entries[i]
                    break
            self.tree.delete(item)
        self.update_tree()
        self.save_csv()

    # Updates the treeview widget with current entry list
    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for item in self.entries:
            self.tree.insert('', tk.END, values = item)

    # Saves current data to CSV file
    def save_csv(self):
        df = pd.DataFrame(self.entries, columns = ["Date", "Category", "Amount", "Transaction Type"])
        df.to_csv(self.csv_file, index = False)

    # Loads data from the existing CSV file at startup and sort the data by Date
    def load_csv(self):
        if not os.path.exists(self.csv_file):
            messagebox.showerror("Error", "CSV file does not exist.")
            return

        df = pd.read_csv(self.csv_file)
        df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d", errors = 'coerce')
        df = df.dropna(subset = ["Date"])
        df = df.sort_values("Date")
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
        self.entries = df.values.tolist()
        self.update_tree()


    # Imports a new CSV file and replaces all current entries
    def import_csv(self):
        path = filedialog.askopenfilename(filetypes = [("CSV Files", "*.csv")])
        if path:
            df = pd.read_csv(path)
            self.entries = df.values.tolist()
            self.update_tree()
            self.save_csv()

    # Exports current data to a user-specified CSV file
    def export_csv(self):

        path = filedialog.asksaveasfilename(filetypes = [("CSV Files", "*.csv")])
        if path:
            df = pd.DataFrame(self.entries, columns = ["Date", "Category", "Amount", "Transaction Type"])
            df.to_csv(path, index = False)

    # Generates and displays a pie chart with income vs expense
    def show_pie_chart(self):
        # Read and process data
        cleaned = []
        for entry in self.entries:
            date_str, cat, amt_str, typ = entry

            # Convert to float
            amt = float(amt_str.replace("$", "").replace(",", ""))

            # Clean up date info
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            cleaned.append((date_obj, cat, amt, typ))

        # Determine averaging factor based on filter
        filter_choice = self.filter_option.get()
        if filter_choice == "Monthly":
            n = len(Transaction(self.entries).calculate_monthly_summary()) or 1
        elif filter_choice == "Weekly":
            n = len(Transaction(self.entries).calculate_weekly_summary()) or 1
        else:
            n = 1

        # Group data by Type + Category
        expense_category = {}
        income_category  = {}

        for date_obj, category, amount, typ in cleaned:
            if typ == "Expense":
                expense_category[category] = expense_category.get(category, 0) + amount
            else:
                income_category[category]  = income_category.get(category, 0)  + amount

        for cat in expense_category:
            expense_category[cat] /= n
        for cat in income_category:
            income_category[cat]  /= n

        labels = [f"Income:{cat}" for cat in income_category] \
               + [cat for cat in expense_category]
        sizes  = [income_category[cat] for cat in income_category] \
               + [expense_category[cat] for cat in expense_category]

        # Use predetermined colors for income and expenses
        num_inc  = len(income_category)
        num_exp  = len(expense_category)
        colors   = INCOME_COLORS[:num_inc] + EXPENSE_COLORS[:num_exp]

        total_inc = sum(income_category.values())
        total_exp = sum(expense_category.values())

        plt.close()
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors)
        plt.axis("equal")
        plt.title(
            f"Income: ${total_inc:.2f}\nExpenses: ${total_exp:.2f}",
            pad=20
        )   
        plt.show()
        self.chart_open = True

class Transaction:
    def __init__(self, entries):
        self.entries = entries

    # Calculate total expense and income
    def calculate_totals(self):
        total_expense = 0
        total_income = 0

        for entry in self.entries:
            amount = float(entry[2][1:])
            transaction_type = entry[3]
            
            # total expense
            if transaction_type == 'Expense':
                total_expense += amount

            # total income
            if transaction_type == 'Income':
                total_income += amount

        # OPTIONAL  
        # total_balance = total_income - total_expense

        return total_expense, total_income, total_balance

    def calculate_category_totals(self):
        categories = dict()
        total_expense, total_income = self.calculate_totals()

        for entry in self.entries:
            cat = entry[1]
            amount = float(entry[2][1:])
            transaction_type = entry[3]

            if cat not in categories:
                categories[cat] = {
                    "Income": 0,
                    "Expense": 0
                }
            if transaction_type == 'Expense':
                categories[cat]["Expense"] += amount
            elif transaction_type == 'Income':
                categories[cat]["Income"] += amount

        # for cat in categories:
        #     if total_expense > 0:
        #         expense_percent = (categories[cat]["Expense"]/ total_expense) * 100
        #         categories[cat]["Expense %"] = expense_percent
        #     if total_income > 0:
        #         income_percent = (categories[cat]["Income"] / total_income) * 100
        #         categories[cat]["Income %"] = income_percent
        
        return categories

    # OPTIONAL
    def calculate_weekly_summary(self):
        total_by_week = dict()

        for entry in self.entries:
            date = entry[0]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year, week, _ = date_obj.isocalendar()
            week_key = f"{year}-Week {week:02d}"

            if week_key not in total_by_week:
                total_by_week[week_key] = {
                    "income": 0,
                    "Expense": 0
                }
            
            amount = float(entry[2][1:])
            transaction_type = entry[3]

            if transaction_type == 'Expense':
                total_by_week[week_key]["Expense"] += amount
            elif transaction_type == 'Income':
                total_by_week[week_key]["Income"] += amount
        
        return total_by_week

    # OPTIONAL
    def calculate_monthly_summary(self):
        total_by_month = dict()

        for entry in self.entries:
            date = entry[0]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            month_key = f"{year}-Month {month:02d}"

            if month_key not in total_by_month:
                total_by_month[month_key] = {
                    "Income": 0,
                    "Expense": 0
                }
            
            amount = float(entry[2][1:])
            transaction_type = entry[3]

            if transaction_type == 'Expense':
                total_by_month[month_key]["Expense"] += amount
            elif transaction_type == 'Income':
                total_by_month[month_key]["Income"] += amount

        return total_by_month

if __name__ == "__main__":
    app = TrackerCSV()
    app.mainloop()
