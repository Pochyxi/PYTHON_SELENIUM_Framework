import json

from ibridHUB.scribers.html_scribe import HTML_scribe
from ibridHUB.scribers.json_scribe import JSON_scribe
from utils.Utils4.Utils4 import Utils4
from utils.Utils4.player.Player import Player
from utils.Utils4.player.PockeCompiler import PockeCompiler


class AppHandler:

    def __init__(self, browser):
        self.utils = Utils4(browser)

        self.driver = self.utils.get_driver()

        self.ConfigJsonObj = JSON_scribe("./ibridHUB/json_data/data.json")

        self.TestSuiteJsonObj = JSON_scribe("./ibridHUB/json_data/test_suite.json")

        self.HTML_scribe = HTML_scribe(self.driver)

        self.HTML_scribe.add_html_global(self.standard_obj())

        self.stale()

    def standard_obj(self):
        print("INIZIALIZZAZIONE OGGETTO JSON...")
        config = self.ConfigJsonObj.obj_from_json()["config"]
        config["router"] = "home"
        config["home_flag"] = True
        config["flag"] = True
        config["test_running"] = False
        config["test_running_flag"] = False
        config["test_coordinate"] = ""
        self.ConfigJsonObj.set_json_obj("config", config)

        print("OGGETTO JSON INIZIALIZZATO")

        return self.ConfigJsonObj.obj_from_json()

    def stale(self):

        while True:

            # OGGETTO JSON
            json_obj = self.ConfigJsonObj.obj_from_json()
            print("JSON OBJ: ", json_obj)

            # HTML OBJ
            html_obj_braces = self.HTML_scribe.obj_from_html()
            print("HTML OBJ: ", html_obj_braces)

            self.utils.sleepping_wait(0.5)
            print("Watching...")

            # ROUTER
            self.router(json_obj, html_obj_braces)

            # LACIO DEI TEST CASES
            self.arbitrum(json_obj, html_obj_braces, self.TestSuiteJsonObj.obj_from_json())

            self.test_compiler(self.TestSuiteJsonObj.obj_from_json(), html_obj_braces, json_obj)

            # CONTROLLO CHIUSURA
            if not self.close_control():
                break

    def router(self, config_obj, html_obj):

        # Aggiorno l'html obj in base al json obj
        self.HTML_scribe.set_html_obj(config_obj, "config", "braces")

        print("JSON_ROUTER: ", config_obj["config"]["router"])

        print("HTML_ROUTER: ", html_obj["router"])

        # Se la flag è True, allora il router deve cambiare pagina
        # aggiorna il json obj e setta la pagina html
        if html_obj["home_flag"]:
            self.router_redirect(config_obj)

        elif html_obj["test_flag"]:
            self.router_redirect(config_obj, redirect="test")

    def router_redirect(self, config_obj, redirect="home"):
        if redirect == "test":
            self.HTML_scribe.add_html_global(self.standard_obj())

            self.update_router_info(config_obj, page_name='test')

            self.HTML_scribe.set_test_page_and_update_html_obj(config_obj, self.TestSuiteJsonObj.obj_from_json())

        elif redirect == "home":
            self.HTML_scribe.add_html_global(self.standard_obj())

            self.update_router_info(config_obj)

            # Aggiorno l'html e provvedo ad aggiornare l'oggetto html
            self.HTML_scribe.set_home_page_and_update_html_obj(config_obj)

    def update_router_info(self, config_obj, page_name="home"):
        if page_name == 'home':
            config_obj["config"]["router"] = "home"
            config_obj["config"]["home_flag"] = False
            self.ConfigJsonObj.set_json_obj("config", config_obj["config"])
        elif page_name == 'test':
            config_obj["config"]["router"] = "test"
            config_obj["config"]["test_flag"] = False
            self.ConfigJsonObj.set_json_obj("config", config_obj["config"])

    def close_control(self):
        return self.HTML_scribe.obj_from_html('braces')["flag"]

    def test_compiler(self, test_suite_obj, html_obj, json_obj):

        if html_obj["save_test_case_flag"] and html_obj["test_case_coordinates"] != "":
            self.HTML_scribe.delete_container("toast_container")

            cliente = html_obj["test_case_coordinates"].split(" || ")[0]
            application = html_obj["test_case_coordinates"].split(" || ")[1]
            test_case = html_obj["test_case_coordinates"].split(" || ")[2]

            if cliente in test_suite_obj["test_suite"]["clienti"].keys():
                print("CLIENTE PRESENTE")

                if application in test_suite_obj["test_suite"]["clienti"][cliente]["applications"].keys():
                    print("APP PRESENTE")

                    if test_case not in test_suite_obj["test_suite"]["clienti"][cliente]["applications"][application][
                        "test_cases"].keys():
                        print("TEST CASE NON PRESENTE")
                        test_suite_obj["test_suite"]["clienti"][cliente]["applications"][application]["test_cases"][
                            test_case] = json.loads(html_obj["test_case_list"])

                        self.TestSuiteJsonObj.set_json_obj("test_suite", test_suite_obj["test_suite"])

                        print("TEST CASE AGGIUNTO")
                        self.HTML_scribe.clear_container("braces")
                        self.HTML_scribe.set_html_obj(json_obj, "config", "braces")
                        self.HTML_scribe.global_scripts.toast("Test Case Aggiunto")
                    else:
                        print("TEST CASE PRESENTE NELLA LISTA")
                        self.HTML_scribe.clear_container("braces")
                        self.HTML_scribe.set_html_obj(json_obj, "config", "braces")
                        self.HTML_scribe.global_scripts.toast("Il test case " + test_case + " è già presente nella lista", "danger")
                else:
                    print("APP NON PRESENTE")
                    self.HTML_scribe.clear_container("braces")
                    self.HTML_scribe.set_html_obj(json_obj, "config", "braces")
                    self.HTML_scribe.global_scripts.toast("App " + application + " non presente in " + cliente, "danger")
            else:
                print("CLIENTE NON PRESENTE")
                self.HTML_scribe.clear_container("braces")
                self.HTML_scribe.set_html_obj(json_obj, "config", "braces")
                self.HTML_scribe.global_scripts.toast("Cliente " + cliente + " non presente nella lista clienti", "danger")

    def arbitrum(self, config_obj, html_obj, test_suite_obj):
        result = False
        if html_obj["run_test_flag"]:
            config_obj['config']['test_running'] = True
            self.ConfigJsonObj.set_json_obj("config", config_obj['config'])
            try:
                # # # # LOGICA DI TEST RUNNING
                self.compile_and_run_test(test_suite_obj, html_obj)
                # # # # FINE ______
                result = True
            except Exception as e:
                print(e)
                self.reset_page_after_test(config_obj, result)

            config_obj['config']['run_test_flag'] = False
            self.ConfigJsonObj.set_json_obj("config", config_obj['config'])

        if config_obj['config']['test_running'] and result:
            config_obj['config']['test_running'] = False
            self.ConfigJsonObj.set_json_obj("config", config_obj['config'])
            self.reset_page_after_test(config_obj, result)

    def compile_and_run_test(self, config_obj, html_obj):
        coordinate_list = html_obj["test_coordinate"].split(" || ")

        cliente = coordinate_list[0]
        application = coordinate_list[1]
        test_case = coordinate_list[2]

        script = config_obj["test_suite"]['clienti'][cliente]['applications'][application]['test_cases'][test_case]

        Player(self.utils, PockeCompiler(script).compile_pockes()).throw_pockes()

    def reset_page_after_test(self, config_obj, result):
        self.reset_app(config_obj)
        if result:
            self.HTML_scribe.push_success_modal()
            self.utils.sleepping_wait(3)
            self.HTML_scribe.delete_container("dvlpz-modal-success")
        else:
            self.HTML_scribe.push_error_modal()
            self.utils.sleepping_wait(3)
            self.HTML_scribe.delete_container("dvlpz-modal-error")

    def reset_app(self, config_obj):
        self.utils.get_page("data:,")
        self.HTML_scribe.add_html_global(self.standard_obj())
        self.router_redirect(config_obj)
