import tkinter as tk
from tkinter import ttk, messagebox
import copy

class ShoppingCartApp:
    def __init__(self, master):  # Rename root to master
        self.history = None
        self.root = master  # Keep the reference as self.root for clarity
        self.root.title("Shopping Cart App")
        self.root.configure(bg="#f8f9fa")  # Light background color
        self.cart = {}

        # History for Undo/Redo
        self.history = []  # Stack for undo
        self.redo_history = []  # Stack for redo

        # Configure dynamic resizing
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Main frame for content
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        # Keep the frame centered
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Header
        header = tk.Label(
            self.main_frame,
            text="Welcome to Shopping Cart",
            font=("Helvetica", 16, "bold"),
            bg="#f8f9fa",
            fg="#007bff",
        )
        header.grid(row=0, column=0, pady=10)

        # Form frame
        form_frame = ttk.Frame(self.main_frame)
        form_frame.grid(row=1, column=0, pady=20, padx=10)

        ttk.Label(form_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.item_entry = ttk.Entry(form_frame)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.price_entry = ttk.Entry(form_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=20)

        self.add_button = ttk.Button(button_frame, text="Add Item", command=self.add_item)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.view_button = ttk.Button(button_frame, text="View Cart", command=self.view_cart)
        self.view_button.grid(row=0, column=1, padx=5, pady=5)

        self.checkout_button = ttk.Button(button_frame, text="Checkout", command=self.checkout)
        self.checkout_button.grid(row=0, column=2, padx=5, pady=5)

        self.undo_button = ttk.Button(button_frame, text="Undo", command=self.undo)
        self.undo_button.grid(row=0, column=2, padx=5, pady=5)

        self.redo_button = ttk.Button(button_frame, text="Redo", command=self.redo)
        self.redo_button.grid(row=0, column=3, padx=5, pady=5)

        # Remove frame
        remove_frame = ttk.Frame(self.main_frame)
        remove_frame.grid(row=3, column=0, pady=20)

        ttk.Label(remove_frame, text="Remove Item:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.remove_item_entry = ttk.Entry(remove_frame)
        self.remove_item_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(remove_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.remove_quantity_entry = ttk.Entry(remove_frame)
        self.remove_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        self.remove_button = ttk.Button(remove_frame, text="Remove", command=self.remove_item)
        self.remove_button.grid(row=2, column=1, padx=5, pady=5)

        # Sort frame
        sort_frame = ttk.Frame(self.main_frame)
        sort_frame.grid(row=4, column=0, pady=20)

        self.sort_alpha_button = ttk.Button(sort_frame, text="Sort Alphabetically", command=self.sort_alphabetically)
        self.sort_alpha_button.grid(row=0, column=0, padx=5, pady=5)

        self.sort_price_button = ttk.Button(sort_frame, text="Sort by Price", command=self.sort_by_price)
        self.sort_price_button.grid(row=0, column=1, padx=5, pady=5)

        # Search frame
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=5, column=0, pady=20)

        ttk.Label(search_frame, text="Search Item:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_item)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Save state before performing any action
    def save_state(self):
        self.history.append(copy.deepcopy(self.cart))
        self.redo_history.clear()  # Clear redo stack when new action occurs

    def add_item(self):
        self.save_state()
        item = self.item_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            if item in self.cart:
                self.cart[item]['quantity'] += quantity
            else:
                self.cart[item] = {'quantity': quantity, 'price': price}
            messagebox.showinfo("Success", f"Added {quantity} x {item}(s) to the cart.")
            self.item_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and price.")

    def view_cart(self):
        if not self.cart:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return

        # Create a new Toplevel window for the cart
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Cart Details")
        cart_window.geometry("400x400")

        # Add scrollable canvas
        canvas = tk.Canvas(cart_window)
        scroll_y = ttk.Scrollbar(cart_window, orient="vertical", command=canvas.yview)

        # Grid the canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        # Define the frame to hold cart items
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        # Populate cart details using grid
        for i, (item, details) in enumerate(self.cart.items(), start=1):
            ttk.Label(frame, text=f"{i}. {item}: {details['quantity']} @ ${details['price']:.2f}",
                      font=("Helvetica", 12, "bold")).grid(row=i, column=0, padx=5, pady=2, sticky="w")

        # Update scroll region when the frame changes size
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def search_item(self):
        query = self.search_entry.get().lower()
        results = {
            item: details
            for item, details in self.cart.items()
            if query in item.lower()
        }

        if results:
            result_text = "\n".join(
                f"{item}: {details['quantity']} @ ${details['price']:.2f}"
                for item, details in results.items()
            )
            messagebox.showinfo("Search Results", result_text)
        else:
            messagebox.showinfo("Search Results", "No items found.")


    def remove_item(self):
        self.save_state()
        item = self.remove_item_entry.get()
        try:
            quantity = int(self.remove_quantity_entry.get())
            if item in self.cart:
                if self.cart[item]['quantity'] > quantity:
                    self.cart[item]['quantity'] -= quantity
                    messagebox.showinfo("Remove Item", f"Removed {quantity} x {item}(s) from the cart.")
                else:
                    del self.cart[item]
                    messagebox.showinfo("Remove Item", f"{item} has been removed from the cart.")
                self.remove_item_entry.delete(0, tk.END)
                self.remove_quantity_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"{item} is not in the cart.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity to remove.")

    def sort_alphabetically(self):
        self.save_state()
        if not self.cart:
            messagebox.showinfo("Sort", "Your cart is empty.")
        else:
            sorted_items = sorted(self.cart.items())
            self.cart = dict(sorted_items)
            messagebox.showinfo("Sort", "Cart has been sorted alphabetically by item name.")

    def sort_by_price(self):
        self.save_state()
        if not self.cart:
            messagebox.showinfo("Sort", "Your cart is empty.")
        else:
            sorted_items = sorted(self.cart.items(), key=lambda x: x[1]['price'])
            self.cart = dict(sorted_items)
            messagebox.showinfo("Sort", "Cart has been sorted by item price.")

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return

        total = sum(details['quantity'] * details['price'] for details in self.cart.values())
        confirm = messagebox.askyesno("Confirm Checkout", f"Your total is: ${total:.2f}\nProceed to checkout?")
        if confirm:
            messagebox.showinfo("Checkout", "Thank you for shopping!")
            self.cart.clear()

        # Undo the last action
    def undo(self):
        if self.history:
            self.redo_history.append(copy.deepcopy(self.cart))  # Save current state to redo
            self.cart = self.history.pop()  # Restore previous state
            messagebox.showinfo("Undo", "Last action undone.")
        else:
            messagebox.showinfo("Undo", "No actions to undo.")

        # Redo the last undone action
    def redo(self):
        if self.redo_history:
            self.history.append(copy.deepcopy(self.cart))  # Save current state to history
            self.cart = self.redo_history.pop()  # Restore redo state
            messagebox.showinfo("Redo", "Redo completed.")
        else:
            messagebox.showinfo("Redo", "No actions to redo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
