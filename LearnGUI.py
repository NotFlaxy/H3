import tkinter as tk

def createWindow():
    window = tk.Tk()
    window.title("This is my GUI")
    window.geometry("400x600")
    return window

def windowContent(window):
    # Frame creation
    frameA = tk.Frame(master=window, height=60, borderwidth=5, relief=tk.RIDGE)
    frameB = tk.Frame(master=window, borderwidth=3, relief=tk.RIDGE)
    
    # Disable content adjusting frame size
    frameA.pack_propagate(False)
    frameB.pack_propagate(False)

    # Labels, Text boxes, Inputs and Buttons.
    inputLabel = tk.Label(master=frameA, text="IP-Address:", foreground="black", font=("Comic Sans", 10))
    entry = tk.Entry(master=frameA, width=30)
    textBox = tk.Text(master=frameB, foreground="black", font=("Helvetica"))
    button = tk.Button(master=window, width=10, height=3, text="Submit", command=lambda: buttonClick(entry, textBox))
    textBox.config(state="disabled")

    # Initialize Content
    frameA.pack(fill=tk.X, pady=5, padx=5)
    frameB.pack(fill=tk.BOTH, expand=True, pady=(5, 5), padx=5)
    inputLabel.pack(fill=tk.BOTH, side=tk.TOP)
    textBox.pack(fill=tk.BOTH, expand=True)
    entry.pack(side=tk.BOTTOM, pady=2)
    button.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 5), padx=5)
    return entry

def buttonClick(entry, textBox):
    userInput = entry.get()
    textBox.config(state="normal")
    textBox.insert(1.0, "Hello There\n")
    print(userInput)

def main():
    window = createWindow()
    windowContent(window)
    window.mainloop()

if __name__ == "__main__":
    main()