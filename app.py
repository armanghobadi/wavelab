import tkinter as tk
from controllers.main_controller import MainController
from views.main_view import MainView

def main():
    root = tk.Tk()
    view = MainView(root)
    controller = MainController(view)
    root.mainloop()

if __name__ == "__main__":
    main()