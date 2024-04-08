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

        self.chord_visualizer=ChordRingGUI(self.canvas_frame, self.inventory_instance.chord)

    def add_item(self):
        item_name = self.item_entry_field.get()
        item_quantity = self.quantity_entry_field.get()

        if not item_name or not item_quantity:
            messagebox.showerror("Error", "Enter a valid name and quantity please.")
            return

        node = self.inventory_instance.add_item(item_name, item_quantity)
        messagebox.showinfo("Success",
                            item_name + " added successfully to the inventory system!" + " Stored at node: " + str(node))

    def get_item(self):
        item_name = self.item_entry_field.get()

        if not item_name:
            messagebox.showerror("Error", "Enter a valid item name please.")
            return

        quantity = self.inventory_instance.get_item_quantity(item_name)
        decoded_quantity = quantity.decode("utf-8")
        if quantity:
            messagebox.showinfo("Item Quantity",
                                "There are " + decoded_quantity + " " + item_name + "'s in the inventory system")
        else:
            messagebox.showerror("Error", "Item not found")


class ChordRingGUI:
    def __init__(self, master, chord):
        self.master = master
        self.canvas_width = 400
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.chord = chord
        self.draw_ring()

    def draw_ring(self):
        num_nodes = len(self.chord.sorted_keys)
        angle_increment = 2 * pi / num_nodes

        for i, ring_key in enumerate(self.chord.sorted_keys):
            x = self.canvas_width / 2 + self.canvas_width / 3 * cos(i * angle_increment)
            y = self.canvas_height / 2 + self.canvas_height / 3 * sin(i * angle_increment)
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")
            self.canvas.create_text(x, y-15, text=str(i))

        for i, ring_key in enumerate(self.chord.sorted_keys):
            successor_key = self.chord.get_successor(ring_key)
            if successor_key is not None:
                successor_index = self.chord.sorted_keys.index(successor_key)
                start_x = self.canvas_width / 2 + self.canvas_width / 3 * cos(i * angle_increment)
                start_y = self.canvas_height / 2 + self.canvas_height / 3 * sin(i * angle_increment)
                end_x = self.canvas_width / 2 + self.canvas_width / 3 * cos(successor_index * angle_increment)
                end_y = self.canvas_height / 2 + self.canvas_height / 3 * sin(successor_index * angle_increment)

                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="black")



if __name__ == "__main__":
    nodes = ['localhost']

    inventory = InventorySystem(nodes)

    root = tk.Tk()
    app = InventoryApp(root, inventory)
    root.mainloop()
