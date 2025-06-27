#  TinyThreads - Kids Clothing Store GUI App

This is a basic Python GUI app I made using **Tkinter**. It's like a mini kids clothing store where you can:

- View cute clothes with images
- Add items to your cart
- Remove them if you change your mind
- Place a fake order at checkout (just for fun )

---

##  Why I Made This

I wanted to practice working with:
- Python GUIs (Tkinter)
- JSON file reading
- Basic image display using Pillow (PIL)
- Cart logic and button actions

---

##  How It Works

- It loads all product data from `image.json`
- Each product has a name, price, description, and image
- Images are shown in the app if they're saved in the same folder
- You can switch between three tabs: **Shop**, **My Cart**, and **Buy Now**

---

##  File Structure
Backendprojyct/
│
├── tinythreads_backend.py         # Main GUI code
├── image.json                     # Product data file
├── image1.jpg                     # Product images
├── image2.jpg
├── …

 ##Requirements
	•	Python 3.x
	•	Pillow library

 pip3 install pillow

 then type 

 python3 tinythreads_backend.py
