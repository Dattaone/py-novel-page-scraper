import datetime
from ui.ui_inteface import UIInterface

class CLIUI(UIInterface):
    def __init__(self):
        pass
    
    def info(self, msg:str):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
    
    def error(self, msg:str):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌ {msg}")
    
    def progress(self, msg:str):
        print(f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ⚠️ {msg}")