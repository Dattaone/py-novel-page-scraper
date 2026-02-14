_current_ui = None

def set_ui(ui):
    global _current_ui
    _current_ui = ui

def ui():
    return _current_ui