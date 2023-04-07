from utils.Utils4.Utils4 import Utils4
from utils.Utils4.player.Player import Player
from utils.Utils4.player.Pocke import Pocke
from utils.Utils4.player.PocketMold.ClickMold import ClickMold
from utils.Utils4.player.PocketMold.CustomWaitMold import CustomWaitMold
from utils.Utils4.player.PocketMold.FindElementMold import FindElementMold
from utils.Utils4.player.PocketMold.FindElementsMold import FindElementsMold
from utils.Utils4.player.PocketMold.GetPageMold import GetPageMold
from utils.Utils4.player.PocketMold.SelectDropdownMold import SelectDropdownMold
from utils.Utils4.player.PocketMold.standard.WriteMold import WriteMold


class PockeCompiler:

    def __init__(self, string_list):
        self.string_list = string_list


    def compile_pockes(self):
        pocke_list = []

        for string in self.string_list:
            list_of_string_commands = string.split(" || ")
            info_object = {
                'comando': '',
                'params': []
            }

            for pocke in list_of_string_commands:

                index = list_of_string_commands.index(pocke)

                if index == 0:
                    info_object['comando'] = list_of_string_commands[index]
                elif index > 0:
                    info_object['params'].append(list_of_string_commands[index])

            if info_object['comando'] == 'get_page':
                pocke_list.append(Pocke(GetPageMold(*info_object['params'])).get_pocke())
            elif info_object['comando'] == 'click':
                pocke_list.append(Pocke(ClickMold(*info_object['params'])).get_pocke())
            elif info_object['comando'] == 'custom_wait':
                pocke_list.append(Pocke(CustomWaitMold(*info_object['params'])).get_pocke())
            elif info_object['comando'] == 'find_element':
                pocke_list.append(Pocke(FindElementMold(*info_object['params'])).get_pocke())
            elif info_object['comando'] == 'find_elements':
                pocke_list.append(Pocke(FindElementsMold(*info_object['params'])).get_pocke())
            elif info_object['comando'] == 'select_dropdown':
                pocke_list.append(Pocke(SelectDropdownMold(*info_object['params'])).get_pocke())
            elif info_object['comando'] == 'write':
                pocke_list.append(Pocke(WriteMold(*info_object['params'])).get_pocke())


        return pocke_list



string_list = [
    "get_page || https://www.tutorialspoint.com/selenium/selenium_automation_practice.htm",
    "click || #mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]",
    "custom_wait || 5",
    "find_element || #mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(9) > td:nth-child(2) > select",
    "custom_wait || 2",
    "find_elements || p",
    "find_elements || strong || css || None || Years of Experience",
    "select_dropdown || #mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(9) > td:nth-child(2) > select || Antartica || css || None || None",
    "write || #mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text] || budkaYo",
    "custom_wait || 5",
]

pocke_compiler = PockeCompiler(string_list)

print(pocke_compiler.compile_pockes())

player = Player(Utils4('edge'), pocke_compiler.compile_pockes())
player.throw_pockes()
