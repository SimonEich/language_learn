from gui.gui_base import Gui
from data.data_handler import DataHandler  # adjust to match your actual implementation

if __name__ == "__main__":
    data = DataHandler()
    app = Gui(data)
    app.root.mainloop()

