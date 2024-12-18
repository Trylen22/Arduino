import tkinter as tk
from therm_ui import ThermometerUI

def main():
    root = tk.Tk()
    app = ThermometerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 