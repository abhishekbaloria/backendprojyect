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