import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# === Configuration ===
PRICE_PER_HOUR = 100

def update_booking_info(event=None):
    try:
        hours = int(hour_cb.get())
        minutes = int(minute_cb.get())

        # Time calculations
        checkin_time = datetime.now()
        checkout_time = checkin_time + timedelta(hours=hours, minutes=minutes)
        total_time_hours = hours + (minutes / 60)

        # Pricing
        subtotal = total_time_hours * PRICE_PER_HOUR

        # Discount rules
        discount_rate = 0
        if total_time_hours >= 5:
            discount_rate = 0.20
        elif total_time_hours >= 3:
            discount_rate = 0.10

        discount_amount = subtotal * discount_rate
        total_price = subtotal - discount_amount

        # Set values
        checkin_var.set(checkin_time.strftime("%Y-%m-%d %I:%M %p"))
        checkout_var.set(checkout_time.strftime("%Y-%m-%d %I:%M %p"))
        price_var.set(f"₱ {subtotal:,.2f}")
        discount_var.set(f"− ₱ {discount_amount:,.2f} ({int(discount_rate * 100)}% off)")
        total_var.set(f"₱ {total_price:,.2f}")

    except ValueError:
        pass

# == MAIN ENTRY ==
root = tk.Tk()
root.geometry("420x400")
root.title("Check-In / Check-Out with Discounted Pricing")

tk.Label(root, text="Select Duration:").pack(pady=(10, 5))
duration_frame = tk.Frame(root)
duration_frame.pack()

# Hours
tk.Label(duration_frame, text="Hours").grid(row=0, column=0, padx=5)
hour_cb = ttk.Combobox(duration_frame, values=list(range(0, 25)), state="readonly", width=5)
hour_cb.grid(row=0, column=1)

# Minutes
tk.Label(duration_frame, text="Minutes").grid(row=0, column=2, padx=5)
minute_cb = ttk.Combobox(duration_frame, values=[0, 15, 30, 45], state="readonly", width=5)
minute_cb.grid(row=0, column=3)

# Bind both ComboBoxes
hour_cb.bind("<<ComboboxSelected>>", update_booking_info)
minute_cb.bind("<<ComboboxSelected>>", update_booking_info)

# Output fields
checkin_var = tk.StringVar()
checkout_var = tk.StringVar()
price_var = tk.StringVar()
discount_var = tk.StringVar()
total_var = tk.StringVar()

tk.Label(root, text="Check-In Time:").pack(pady=(20, 0))
tk.Label(root, textvariable=checkin_var).pack()

tk.Label(root, text="Check-Out Time:").pack(pady=(10, 0))
tk.Label(root, textvariable=checkout_var).pack()

tk.Label(root, text="Subtotal Price:").pack(pady=(10, 0))
tk.Label(root, textvariable=price_var).pack()

tk.Label(root, text="Discount:").pack(pady=(5, 0))
tk.Label(root, textvariable=discount_var, fg="orange").pack()

tk.Label(root, text="Total Price:").pack(pady=(10, 0))
tk.Label(root, textvariable=total_var, font=("Arial", 12, "bold"), fg="green").pack()

root.mainloop()
