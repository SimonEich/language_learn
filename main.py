from db import Database
from gui import Gui
from readfile_v2 import ReadFile

from cards import Card

file_name = "cards/cards/txt/es_en.txt"


if __name__=="__main__":
    
    data = ReadFile(file_name)

    db = Database(data.read_and_process_file())
    gui = Gui(db)
    
    gui.root.mainloop()
    
