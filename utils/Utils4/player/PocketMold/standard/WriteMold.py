class WriteMold:

    def __init__(self, selector, text, by='css', press_enter=False):
        self.selector = selector
        self.text = text
        self.by = by
        self.press_enter = None if press_enter == 'None' else press_enter

        if self.press_enter == 'True':
            self.press_enter = True

    def get_pocket_mold(self):
        return {"name": "write", "args": [self.selector, self.text, self.by, self.press_enter]}
