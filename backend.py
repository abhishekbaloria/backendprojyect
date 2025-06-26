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
