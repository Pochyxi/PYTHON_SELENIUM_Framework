from utils.Utils4.player.PocketMold.StandarMold import StandardMold


class ClickMold(StandardMold):

    def __init__(self, selector: str, by='css'):
        self.selector = selector
        self.by = by

    def get_pocket_mold(self):
        return {"name": "click", "args": [self.selector, self.by]}
