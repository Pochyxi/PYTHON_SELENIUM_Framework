from ibridHUB.scribers.html_scribe import HTML_scribe
from ibridHUB.scribers.json_scribe import JSON_scribe
from utils.Utils4 import Giver
from utils.Utils4.Utils4 import Utils4
from utils.Utils4.player.Pocke import Pocke
from utils.Utils4.player.Player import Player
from utils.Utils4.player.PocketMold.ClickMold import ClickMold
from utils.Utils4.player.PocketMold.FindElementsMold import FindElementsMold
from utils.Utils4.player.PocketMold.GetPageMold import GetPageMold
from utils.Utils4.player.PocketMold.SelectDropdownMold import SelectDropdownMold
from utils.Utils4.player.PocketMold.standard.WriteMold import WriteMold


class AppHandler:

    def __init__(self, browser):
        self.utils = Utils4(browser)

        self.driver = self.utils.get_driver()

        self.JSON_scribe = JSON_scribe("./ibridHUB/json_data/data.json")

        self.HTML_scribe = HTML_scribe(self.driver)

        self.HTML_scribe.add_html_global(self.standard_obj())

        self.stale()

    def standard_obj(self):
        print("INIZIALIZZAZIONE OGGETTO JSON...")
        config = self.JSON_scribe.obj_from_json()["config"]
        config["router"] = "home"
        config["home_flag"] = True
        config["flag"] = True
        self.JSON_scribe.set_json_obj("config", config)

        print("OGGETTO JSON INIZIALIZZATO")

        return self.JSON_scribe.obj_from_json()

    def stale(self):

        while True:
            # OGGETTO JSON
            json_obj = self.JSON_scribe.obj_from_json()
            print("JSON OBJ: ", json_obj)

            # HTML OBJ
            html_obj_braces = self.HTML_scribe.obj_from_html()
            print("HTML OBJ: ", html_obj_braces)

            self.utils.sleepping_wait(0.5)
            print("Watching...")

            # ROUTER
            self.router(json_obj, html_obj_braces)

            # Momentaneo solo a scopo di test
            self.arbitrum(json_obj, html_obj_braces, self.utils)

            # CONTROLLO CHIUSURA
            if not self.close_control():
                break

    def router(self, json_obj, html_obj):

        # Aggiorno l'html obj in base al json obj
        self.HTML_scribe.set_html_obj(json_obj, "config", "braces")

        print("JSON_ROUTER: ", json_obj["config"]["router"])

        print("HTML_ROUTER: ", html_obj["router"])

        # Se la flag è True, allora il router deve cambiare pagina
        # aggiorna il json obj e setta la pagina html
        if html_obj["home_flag"]:
            self.router_redirect(json_obj)

        elif html_obj["test_flag"]:
            self.router_redirect(json_obj, redirect="test")

    def router_redirect(self, json_obj, redirect="home"):
        if redirect == "test":
            self.HTML_scribe.add_html_global(self.standard_obj())

            self.update_router_info(json_obj, page_name='test')

            self.HTML_scribe.set_test_page_and_update_html_obj(json_obj)

        elif redirect == "home":
            self.HTML_scribe.add_html_global(self.standard_obj())

            self.update_router_info(json_obj)

            # Aggiorno l'html e provvedo ad aggiornare l'oggetto html
            self.HTML_scribe.set_home_page_and_update_html_obj(json_obj)

    def update_router_info(self, json_obj, page_name="home"):
        if page_name == 'home':
            json_obj["config"]["router"] = "home"
            json_obj["config"]["home_flag"] = False
            self.JSON_scribe.set_json_obj("config", json_obj["config"])
        elif page_name == 'test':
            json_obj["config"]["router"] = "test"
            json_obj["config"]["test_flag"] = False
            self.JSON_scribe.set_json_obj("config", json_obj["config"])

    def close_control(self):
        return self.HTML_scribe.obj_from_html('braces')["flag"]

    def arbitrum(self, json_obj, html_obj, utils):
        result = False
        if html_obj["run_test_flag"]:
            json_obj['config']['test_running'] = True
            self.JSON_scribe.set_json_obj("config", json_obj['config'])
            try:
                self.example_test(utils)
                result = True
            except Exception as e:
                print(e)
                self.reset_page_after_test(json_obj, result)

            json_obj['config']['run_test_flag'] = False
            self.JSON_scribe.set_json_obj("config", json_obj['config'])

        if json_obj['config']['test_running'] and result:
            json_obj['config']['test_running'] = False
            self.JSON_scribe.set_json_obj("config", json_obj['config'])
            self.reset_page_after_test(json_obj, result)

    def reset_page_after_test(self, json_obj, result):
        self.reset_app(json_obj)
        if result:
            self.HTML_scribe.push_success_modal()
            self.utils.sleepping_wait(3)
            self.HTML_scribe.delete_container("dvlpz-modal-success")
        else:
            self.HTML_scribe.push_error_modal()
            self.utils.sleepping_wait(3)
            self.HTML_scribe.delete_container("dvlpz-modal-error")

    def reset_app(self, json_obj):
        self.utils.get_page("data:,")
        self.HTML_scribe.add_html_global(self.standard_obj())
        self.router_redirect(json_obj)

    @staticmethod
    def example_test(utils):
        get_page_pocke = Pocke(GetPageMold(Giver.get_practice1_elements("practice_page_1"))).get_pocke()

        click_pocke = Pocke(ClickMold(Giver.get_practice1_elements("input_writing"))).get_pocke()

        find_elements_pocke = Pocke(FindElementsMold("strong")).get_pocke()

        write_pocke = Pocke(
            WriteMold(Giver.get_practice1_elements("input_writing"), "Questo è un esempio di scrittura")).get_pocke()

        select_pocke = Pocke(SelectDropdownMold(Giver.get_practice1_elements("country_select"), index=3)).get_pocke()

        player = Player(utils, [get_page_pocke, click_pocke, find_elements_pocke, write_pocke, select_pocke])

        player.throw_pockes()
