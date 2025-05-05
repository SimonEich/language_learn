from db import Database
from gui import Gui

from cards import Card

file_name = "cards/cards/txt/es_en.txt"


if __name__=="__main__":
    

    db = Database()
    gui = Gui(db)
    
    gui.root.mainloop()
    
