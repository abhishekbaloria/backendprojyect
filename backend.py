#simple children's clothing store app
#Built using Tkinter and Pillow

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

# App area will handle everything from UI to logic 
class KidsClothingApp:
    def __init__(self, window):
        self.window = window
        self.window.title("TinyThreads Store")
        self.window.geometry("800x600")
        self.window.configure(bg="#e3f2fd")

        # thss will help load products from a JSON file
        self.products = self.load_product_list()
        self.shopping_cart = []

        # this area is for the main tab layout
        self.tabs = ttk.Notebook(window)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.page_home = ttk.Frame(self.tabs)
        self.page_cart = ttk.Frame(self.tabs)
        self.page_checkout = ttk.Frame(self.tabs)

        self.tabs.add(self.page_home, text="Shop")
        self.tabs.add(self.page_cart, text="My Cart")
        self.tabs.add(self.page_checkout, text="Buy Now")

        # thsi will help to Load each tab
        self.setup_home()
        self.setup_cart()
        self.setup_checkout()

    def load_product_list(self):
        if os.path.exists("kids_products.json"):
            with open("kids_products.json", "r") as file:
                return json.load(file)
        return []

    def setup_home(self):
        # Big title that says welcome
        title = tk.Label(self.page_home, text="Welcome to TinyThreads!", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # this will be the container for the product cards
        self.product_frame = tk.Frame(self.page_home)
        self.product_frame.pack()

        # Loop for products and ui 
        for idx, item in enumerate(self.products):
            self.display_product(item, idx)

    def display_product(self, product, index):
        # product box for single product 
        card = tk.Frame(self.product_frame, bd=1, relief=tk.SOLID, padx=10, pady=10)
        card.grid(row=index // 2, column=index % 2, padx=10, pady=10)

        # this will load and display file 
        img_path = product.get("image")
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((120, 120))  # Resize image to fit card
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(card, image=photo)
                img_label.image = photo  # Must store reference to avoid garbage collection
                img_label.pack()
            except Exception as e:
                print(f"Image error: {e}")

        # this section is for the Product name
        name = tk.Label(card, text=product["name"], font=("Arial", 14, "bold"))
        name.pack(anchor="w")

        # Description
        desc = tk.Label(card, text=product["desc"], wraplength=180)
        desc.pack(anchor="w")

        # Price
        price = tk.Label(card, text=f"Price: €{product['price']:.2f}", fg="green")
        price.pack(anchor="w")

        # Add-to-cart button
        buy_btn = tk.Button(card, text="Add to Cart", command=lambda: self.add_to_cart(product))
        buy_btn.pack(pady=5)
