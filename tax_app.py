
import tkinter as tk

from tkinter import messagebox

# 2025 federal income tax brackets - Single
tax_brackets = [
    (11925, 0.10),
    (48475, 0.12),
    (103350, 0.22),
    (197300, 0.24),
    (250525, 0.32),
    (626350, 0.35),
    (float("inf"), 0.37)
]

def calculate_income_tax(taxable_income):
    tax = 0
    previous_limit = 0

    for upper_limit, rate in tax_brackets:
        income_in_bracket = min(
            taxable_income, upper_limit
        ) - previous_limit

        if income_in_bracket <= 0:
            break

        tax += income_in_bracket * rate
        previous_limit = upper_limit

    return round(tax, 2)

def calculate_tax():

    # Check for empty input fields
    entries = [
        name_entry, w2_entry, freelance_entry,
        expenses_entry, interest_entry,
        withholding_entry, payments_entry
    ]

    for entry in entries:
        if not entry.get().strip():
            messagebox.showerror(
                "Missing Information",
                "Please fill in all fields before calculating."
            )
            return

    # Read taxpayer information
    name = name_entry.get()

    # Read and validate all financial inputs
    try:
        wages = float(w2_entry.get())
        freelance = float(freelance_entry.get())
        expenses = float(expenses_entry.get())
        interest = float(interest_entry.get())
        withholding = float(withholding_entry.get())
        payments = float(payments_entry.get())

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers in all financial fields."
        )
        return
    
    # Prevent negative financial inputs
    if any(value < 0 for value in [
        wages, freelance, expenses,
        interest, withholding, payments
    ]):
        messagebox.showerror(
            "Invalid Input",
            "Please enter zero or a positive number."
        )
        return

    # Calculate net business profit
    net_profit = freelance - expenses

    # Calculate total income
    total_income = wages + net_profit + interest

    # Calculate self-employment tax
    se_earnings = max(0, net_profit) * 0.9235
    se_tax = round(se_earnings * 0.153)

    # Calculate adjusted gross income
    se_deduction = round(se_tax / 2)
    agi = total_income - se_deduction

    # 2025 standard deduction for single filers
    standard_deduction = 15750

    # Income after standard deduction
    income_after_deduction = max(0, agi - standard_deduction)

    # Qualified Business Income deduction
    qbi = max(0, net_profit - se_deduction)
    qbi_deduction = round(qbi * 0.20)

    # Taxable income
    taxable_income = max(0, income_after_deduction - qbi_deduction)
    
    # Estimate tax using IRS $50 tax table intervals
    if taxable_income < 100000:
        bracket_midpoint = (int(taxable_income) // 50) * 50 + 25
        federal_income_tax = round(
            calculate_income_tax(bracket_midpoint)
        )
    else:
        federal_income_tax = calculate_income_tax(taxable_income)


    if federal_income_tax is not None:
        # Calculate total federal tax
        total_tax = federal_income_tax + se_tax

        # Calculate refund or amount owed
        total_payments = withholding + payments
        refund = total_payments - total_tax

        if refund >= 0:
            final_result = f"Estimated Refund: ${refund:,.2f}"
        else:
            final_result = f"Estimated Amount Owed: ${abs(refund):,.2f}"

        # Display results inside the application
        summary = (
            f"Taxpayer: {name}\n"
            f"Adjusted Gross Income: ${agi:,.2f}\n"
            f"Taxable Income: ${taxable_income:,.2f}\n"
            f"Federal Income Tax: ${federal_income_tax:,.2f}\n"
            f"Self-Employment Tax: ${se_tax:,.2f}\n"
            f"Total Federal Tax: ${total_tax:,.2f}\n"
            f"{final_result}"
        )

        result_label.config(text=summary)

    else:
        result_label.config(
            text="Tax table lookup not yet available for this income."
        )

    print("QBI Deduction: $", qbi_deduction)
    print("Taxable Income: $", taxable_income)

    print("Self-Employment Tax: $", se_tax)
    print("Adjusted Gross Income: $", agi)

    print("Taxpayer:", name)
    print("W-2 Income: $", wages)
    print("Net Business Profit: $", net_profit)
    print("Interest Income: $", interest)
    print("Total Tax Payments: $", withholding + payments)

# Create the application window

window = tk.Tk()
window.title("Federal Income Tax Calculator")
window.geometry("550x850")

# Add a heading

title = tk.Label(
    window,
    text="2025 Federal Income Tax Calculator",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

# Taxpayer name input

name_label = tk.Label(window, text="Taxpayer Name:")
name_label.pack(pady=5)

name_entry = tk.Entry(window, width=35)
name_entry.pack(pady=5)

# W-2 income input

w2_label = tk.Label(window, text="W-2 Income ($):")
w2_label.pack(pady=5)

w2_entry = tk.Entry(window, width=35)
w2_entry.pack(pady=5)

# Freelance income input

freelance_label = tk.Label(window, text="Freelance Income ($):")
freelance_label.pack(pady=5)

freelance_entry = tk.Entry(window, width=35)
freelance_entry.pack(pady=5)

# Business expenses input

expenses_label = tk.Label(window, text="Business Expenses ($):")
expenses_label.pack(pady=5)

expenses_entry = tk.Entry(window, width=35)
expenses_entry.pack(pady=5)

# Taxable interest income input

interest_label = tk.Label(window, text="Taxable Interest Income ($):")
interest_label.pack(pady=5)

interest_entry = tk.Entry(window, width=35)
interest_entry.pack(pady=5)

# Federal income tax withholding input

withholding_label = tk.Label(window, text="Federal Tax Withholding ($):")
withholding_label.pack(pady=5)

withholding_entry = tk.Entry(window, width=35)
withholding_entry.pack(pady=5)

# Estimated tax payments input

payments_label = tk.Label(window, text="Estimated Tax Payments ($):")
payments_label.pack(pady=5)

payments_entry = tk.Entry(window, width=35)
payments_entry.pack(pady=5)

# Calculate button

calculate_button = tk.Button(
    window,
    command=calculate_tax,
    text="Calculate Tax",
    font=("Arial", 12, "bold"),
    bg="#2E86C1",
    fg="white"
)

calculate_button.pack(pady=15)

# Clear all input fields
def clear_fields():
    for entry in [
        name_entry, w2_entry, freelance_entry,
        expenses_entry, interest_entry,
        withholding_entry, payments_entry
    ]:
        entry.delete(0, tk.END)

    result_label.config(
        text="Your tax results will appear here."
    )

# Create Clear All button
clear_button = tk.Button(
    window,
    text="Clear All",
    command=clear_fields,
    font=("Arial", 12),
    bg="#777777",
    fg="white"
)

clear_button.pack(pady=5)

# Display tax calculation results
result_label = tk.Label(
    window,
    text="Your tax results will appear here.",
    font=("Arial", 12),
    justify="left"
)

result_label.pack(pady=10)

# Keep the window open
window.mainloop()
