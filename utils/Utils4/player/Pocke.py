from utils.Utils4.player.pocketMold.standard.StandarMold import StandardMold


class Pocke:

    def __init__(self, standard_mold: StandardMold):
        self.mold = standard_mold

    def get_pocke(self):
        return self.mold.get_pocket_mold()
