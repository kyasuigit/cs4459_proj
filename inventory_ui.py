import tkinter as tk
from tkinter import messagebox
from functools import partial
from inventory import InventorySystem
from math import sin, cos, pi


class InventoryApp:
    def __init__(self, master, inventory_instance):
        self.master = master
        master.title("Inventory Management System (Chord Consistent Hashing)")

        self.ui_frame = tk.Frame(master)
        self.ui_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.item_label = tk.Label(self.ui_frame, text="Item Name:")
        self.item_label.grid(row=0, column=0)
        self.item_entry_field = tk.Entry(self.ui_frame)
        self.item_entry_field.grid(row=0, column=1)
        self.quantity_label = tk.Label(self.ui_frame, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)
        self.quantity_entry_field = tk.Entry(self.ui_frame)
        self.quantity_entry_field.grid(row=1, column=1)

        self.add_button = tk.Button(self.ui_frame, text="Add Item to Inventory", command=self.add_item)
        self.add_button.grid(row=2, column=1)

        self.get_button = tk.Button(self.ui_frame, text="Get Item from Inventory", command=self.get_item)
        self.get_button.grid(row=3, column=1)

        self.inventory_instance = inventory_instance


    def add_item(self):
        item_name = self.item_entry_field.get()
        item_quantity = self.quantity_entry_field.get()

        if not item_name or not item_quantity:
            messagebox.showerror("Error", "Enter a valid name and quantity please.")
            return

        self.inventory_instance.add_item(item_name, item_quantity)
        messagebox.showinfo("Success",
                            item_name + " added successfully to the inventory system!")

    def get_item(self):
        item_name = self.item_entry_field.get()

        if not item_name:
            messagebox.showerror("Error", "Enter a valid item name please.")
            return

        quantity = self.inventory_instance.get_item_quantity(item_name)
        if quantity:
            messagebox.showinfo("Item Quantity: ",
                                "Product " + quantity[0] + " has " + quantity[1] + " items.")
        else:
            messagebox.showerror("Error", "Item not found")


if __name__ == "__main__":
    nodes = 6

    inventory = InventorySystem(nodes)

    root = tk.Tk()
    app = InventoryApp(root, inventory)
    root.mainloop()
