class GetPageMold:
    def __init__(self, page: str):
        self.page = page

    def get_pocket_mold(self):
        return {"name": "get_page", "args": [self.page]}
