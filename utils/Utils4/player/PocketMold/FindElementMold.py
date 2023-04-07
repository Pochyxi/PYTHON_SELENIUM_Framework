class FindElementMold:

    def __init__(self, selector: str, by='css'):
        self.selector = selector
        self.by = by

    def get_pocket_mold(self):
        return {"name": "find_element", "args": [self.selector, self.by]}
