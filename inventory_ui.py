import tkinter as tk
from tkinter import messagebox
from functools import partial
from inventory import InventorySystem
from math import sin, cos, pi


class InventoryApp:
    def __init__(self, master, inventory_instance):

        self.all_items = []

        self.master = master
        master.title("Inventory Management System (Chord Consistent Hashing)")

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
        self.quantity_label = tk.Label(self.ui_frame, text="Quantity:") #add all fields for text input and buttons
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

        self.add_node_button = tk.Button(self.button_frame, text="Add Node to Ring", command=self.add_node)
        self.add_node_button.pack(side=tk.RIGHT, padx=5)

        self.delete_node_button = tk.Button(self.button_frame, text="Delete Node From Ring", command=self.delete_node)
        self.delete_node_button.pack(side=tk.RIGHT, padx=5)

    def draw_chord_ring(self):
        self.canvas.delete("all")  
        num_nodes = len(self.inventory_instance.chord.nodes)
        radius = 180
        center_x, center_y = 220, 250
        node_angles = [2 * pi * i / num_nodes for i in range(num_nodes)]  

        for i, angle in enumerate(node_angles):
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            if self.inventory_instance.chord.nodes[i]:
                node_id = self.canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill="red")

                # Binding the items only on nodes that should store items
                on_enter_with_i = partial(self.on_enter, node_identifier=i)
                self.canvas.tag_bind(node_id, "<Enter>", on_enter_with_i)
            
            else:
                node_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")

        for i, angle in enumerate(node_angles):
            start_x = center_x + radius * cos(angle)
            start_y = center_y + radius * sin(angle)
            end_x = center_x + radius * cos(node_angles[(i + 1) % num_nodes])
            end_y = center_y + radius * sin(node_angles[(i + 1) % num_nodes])
            self.canvas.create_line(start_x, start_y, end_x, end_y)

    # Showing a box to display all items to the user 
    def on_enter(self, event, node_identifier):
        messagebox.showinfo(f"Node {node_identifier} Items", self.inventory_instance.get_all_items(node_identifier))


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

        quantity = self.inventory_instance.get_item_quantity(item_name).split(",")
        if quantity:
            messagebox.showinfo("Item Quantity: ",
                                "Product " + item_name + " has " + quantity[1] + " items.")
        else:
            messagebox.showerror("Error", "Item not found")

    # Adding and deleting nodes 
    def delete_node(self):
        number_of_nodes = self.inventory_instance.get_number_of_nodes()
        if number_of_nodes == 2:
                messagebox.showerror("Caution", "Removing more nodes after" +  str(number_of_nodes) + "nodes is not advised!")
        else:
            self.inventory_instance.delete_node()
            self.draw_chord_ring()

    def add_node(self):
        number_of_nodes = self.inventory_instance.get_number_of_nodes()
        if number_of_nodes == 100:
            messagebox.showerror("Caution", "Adding more nodes past " + str(number_of_nodes) + " nodes is not advised!")
        else:
            self.inventory_instance.add_new_node()
            self.draw_chord_ring()


if __name__ == "__main__":
    nodes = 6
    inventory = InventorySystem(nodes)
    root = tk.Tk()
    app = InventoryApp(root, inventory)
    root.mainloop()