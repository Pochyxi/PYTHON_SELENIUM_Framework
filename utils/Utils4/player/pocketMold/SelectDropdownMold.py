class SelectDropdownMold:

    def __init__(self, selector: str, text=None, by='css', index=None, value=None):
        self.selector = selector
        self.text = None if text == 'None' else text
        self.by = by
        self.index = None if index == 'None' else index
        self.value = None if value == 'None' else value

    def get_pocket_mold(self):
        return {"name": "select_dropdown", "args": [self.selector, self.text, self.by, self.index, self.value]}
