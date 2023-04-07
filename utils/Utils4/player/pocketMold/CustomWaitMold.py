class CustomWaitMold:

    def __init__(self, seconds: int):
        self.seconds = seconds

    def get_pocket_mold(self):
        return {"name": "custom_wait", "args": [self.seconds]}