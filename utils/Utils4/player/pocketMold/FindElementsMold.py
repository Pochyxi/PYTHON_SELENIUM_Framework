class FindElementsMold:

    def __init__(self, selector: str, by='css', index=None, text=None):
        self.selector = selector
        self.by = by
        self.index = None if index == 'None' else index
        self.text = None if text == 'None' else text

    def get_pocket_mold(self):
        return {"name": "find_elements", "args": [self.selector, self.by, self.index, self.text]}
