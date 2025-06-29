import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

# Methods
def centerScreen():
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    centerX = int(screenWidth / 2 - WINDOW_WIDTH / 2)
    centerY = int(screenHeight / 2 - WINDOW_HEIGHT / 2)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{centerX}+{centerY}")

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
HEADER_COLOR = "#1a3f73"

root = tk.Tk()
root.title("Room Details")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

centerScreen()

# === HEADER ===
header_frame = tk.Frame(root, bg=HEADER_COLOR, height=60)
header_frame.pack(fill="x")

back_btn = tk.Button(header_frame, text="← Back", bg="white", fg="black", relief="flat", command=root.destroy)
back_btn.pack(side="left", padx=10, pady=10)

title_label = tk.Label(header_frame, text="Room Details", bg=HEADER_COLOR, fg="white",
                       font=tkFont.Font(family="Arial", size=16, weight="bold"))
title_label.pack(pady=10)

# === CONTENT ===
content_frame = tk.Frame(root, bg="white")
content_frame.pack(fill="both", expand=True)

fields = ["Room Number", "Room Type", "Bed Type", "Status"]

# This contains all of the elements (Entries and Combo Box) so we can easily fetch data from it
# later on.
entries = {}

for i, field in enumerate(fields):
    label = tk.Label(content_frame, text=field, bg="white", font=("Arial", 12), anchor="w")
    label.grid(row=i, column=0, sticky="w", pady=10, padx=10)

    if field == "Status":
        combo = ttk.Combobox(content_frame,
                             values=["Available", "Occupied", "Maintenance", "Under Construction", "Not Available"],
                             state="readonly",
                             font=("Arial", 12),
                             width=28)
        combo.grid(row=i, column=1, pady=10, padx=10)
        combo.current(0)
        entries[field] = combo
    else:
        entry = tk.Entry(content_frame, width=30, font=("Arial", 12), state="readonly")
        entry.grid(row=i, column=1, pady=10, padx=10)
        entries[field] = entry

# === UPDATE BUTTON ===
update_button = tk.Button(content_frame, text="Update", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=20, pady=5)
update_button.grid(row=len(fields), column=0, columnspan=2, pady=20)

root.mainloop()
