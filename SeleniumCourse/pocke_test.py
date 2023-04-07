from utils.Utils4 import Giver
from utils.Utils4.Utils4 import Utils4
from utils.Utils4.player.Pocke import Pocke
from utils.Utils4.player.Player import Player
from utils.Utils4.player.pocketMold.ClickMold import ClickMold
from utils.Utils4.player.pocketMold.FindElementsMold import FindElementsMold
from utils.Utils4.player.pocketMold.GetPageMold import GetPageMold

get_page_pocke = Pocke(GetPageMold(Giver.get_practice1_elements("practice_page_1"))).get_pocke()

click_pocke = Pocke(ClickMold(Giver.get_practice1_elements("input_writing"))).get_pocke()

find_elements_pocke = Pocke(FindElementsMold("strong")).get_pocke()

executor = Player(Utils4('edge'), [get_page_pocke, click_pocke, find_elements_pocke])

executor.throw_pockes()


