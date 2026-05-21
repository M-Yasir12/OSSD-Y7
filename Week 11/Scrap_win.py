from Scrapper import get_car_data
from tkinter import ttk
import tkinter as tk
def display_data(car):
    data=get_car_data(car)
    text_area.delete(1.0, tk.END)  # Clear previous data
    for item in data:
        text_area.insert(tk.END, f"Name: {item['name']}, Price: {item['price']}\n")

root=tk.Tk()
root.title("Car Price Scraper")
root.geometry("600x400")


cars=['kia','honda','toyota','suzuki','hyundai']

dropdrown=ttk.Combobox(root, values=cars)
dropdrown.current(3)
dropdrown.pack(pady=20)

find=tk.Button(root, text="Find Price", command=lambda: display_data(dropdrown.get()))
find.pack(pady=10)

text_area=tk.Text(root, height=15, width=70)
text_area.pack(pady=20)





root.mainloop()



