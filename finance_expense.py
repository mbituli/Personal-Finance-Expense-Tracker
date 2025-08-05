import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

class TrackerCSV(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Finance Expense Tracker")
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
        """
        Validate the input fields:
        - Ensure all fields are filled
        - Date is in YYYY-MM-DD format
        - Amount is a valid number

        Append entry to list of entries
        Clear input fields
        Update display
        Save to CSV
        """
        pass  # algorithm placeholder

    # Deletes selected entry from the table
    def delete_entry(self):
        """
        Get selected row(s) in the tree
        Remove those entries from internal list
        Update the table
        Save the updated list to CSV
        """
        pass  # algorithm placeholder

    # Updates the treeview widget with current entry list
    def update_tree(self):
        """
        Clear existing rows in the treeview
        Loop through all entries and insert them into the tree
        """
        pass  # algorithm placeholder

    # Saves current data to CSV file
    def save_csv(self):
        """
        Convert entries to DataFrame
        Write DataFrame to CSV file
        """
        pass  # algorithm placeholder

    # Loads data from the existing CSV file at startup
    def load_csv(self):
        """
        If CSV file exists:
            Read it into DataFrame
            Convert to list of entries
            Update the treeview
        """
        pass  # algorithm placeholder

    # Imports a new CSV file and replaces all current entries
    def import_csv(self):
        """
        Open file dialog to select a CSV file
        Read data into DataFrame
        Replace current entry list with new data
        Update treeview
        Save to main CSV file
        """
        pass  # algorithm placeholder

    # Exports current data to a user-specified CSV file
    def export_csv(self):
        """
        Open file dialog to pick where to save
        Convert entry list to DataFrame
        Save it to selected location
        """
        pass  # algorithm placeholder

    # Generates and displays a pie chart with income vs expense
    def show_pie_chart(self):
        """
        Read and process data:
            - Remove dollar signs and commas
            - Convert to float
            - Apply date filtering (monthly or weekly)

        Group data by Type + Category
        Generate custom labels:
            - Prefix income categories with 'Income:'
            - Show only category name for expenses

        Sum income and expense separately
        Show a pie chart with:
            - Percentage labels
            - Custom colors (green for income, pastel for expense)
            - Title showing Income and Expenses totals
        """
        pass  # algorithm placeholder

if __name__ == "__main__":
    app = TrackerCSV()
    app.mainloop()
