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

        self.canvas = tk.Canvas(self.canvas_frame, width=480, height=480)
        self.canvas.pack()
        self.draw_chord_ring()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.add_node_button = tk.Button(self.button_frame, text="Add Node to Ring")
        self.add_node_button.pack(side=tk.RIGHT, padx=5)

        self.delete_node_button = tk.Button(self.button_frame, text="Delete Node From Ring")
        self.delete_node_button.pack(side=tk.RIGHT, padx=5)

    def draw_chord_ring(self):
        num_nodes = len(self.inventory_instance.chord.nodes)
        radius = 180
        center_x, center_y = 220, 250
        node_angles = [2 * pi * i / num_nodes for i in range(num_nodes)]

        for i, angle in enumerate(node_angles):
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            if self.inventory_instance.chord.nodes[i]:
                self.canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill="red")
            else:
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")


        for i, angle in enumerate(node_angles):
            start_x = center_x + radius * cos(angle)
            start_y = center_y + radius * sin(angle)
            end_x = center_x + radius * cos(node_angles[(i + 1) % num_nodes])
            end_y = center_y + radius * sin(node_angles[(i + 1) % num_nodes])
            self.canvas.create_line(start_x, start_y, end_x, end_y)

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
                                "Product " + item_name + " has " + quantity + " items.")
        else:
            messagebox.showerror("Error", "Item not found")


if __name__ == "__main__":
    nodes = 6

    inventory = InventorySystem(nodes)

    root = tk.Tk()
    app = InventoryApp(root, inventory)
    root.mainloop()
