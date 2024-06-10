import tkinter as tk

root = tk.Tk()

root.geometry("400x400")
root.title("My GUI")

label = tk.Label(root, text="Hello World")
label.pack(padx=10, pady=10)

textbox = tk.Text(root, font=("Helvetica", 16))
textbox.pack(padx=10, pady=10)

tk.mainloop()
