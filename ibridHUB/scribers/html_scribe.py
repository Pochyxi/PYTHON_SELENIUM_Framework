import os
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from ibridHUB.js.GlobalScripts import GlobalScripts
from ibridHUB.js.HomeScripts import HomeScripts
from ibridHUB.js.NavScripts import NavScripts
from ibridHUB.js.TestScripts import TestScripts


class HTML_scribe:

    def __init__(self, driver):
        self.driver = driver

        # JS GLOBAL
        self.global_scripts = GlobalScripts(self.driver)

        # JS HOME
        self.home_scripts = HomeScripts(self.driver)

        # JS NAVBAR
        self.nav_scripts = NavScripts(self.driver)

        # JS TEST
        self.test_scripts = TestScripts(self.driver)

    # # # # HTML BASIC CONFIGURATIONS # # # #

    # Aggiunge tutto il contenuto del tag body in un file specificato
    # Svuota il body della pagina corrente e ci aggiunge il contenuto del file
    def add_html_global(self, json_obj):
        try:
            navbar = self.driver.find_element(By.ID, 'dvlpz-nav-container')

            if navbar:
                print("Navbar presente, non aggiungo il contenuto del file html")
                return
        except Exception:
            print("Navbar non presente, aggiungo il contenuto del file html")

            # Svuota il body nel caso sia popolato
            self.clear_body()

            # Aggiunta delle configurazioni di base per l'html
            self.global_scripts.insert_DOCTYPE()
            self.global_scripts.insert_language()
            self.global_scripts.insert_meta_charset()
            self.global_scripts.insert_title()

            # Aggiunta di BOOTSTRAP CSS
            self.global_scripts.add_bootstrap_css()

            # Aggiunta di bootstrap JS
            self.global_scripts.add_bootstrap_js()

            # Attendi che il browser abbia caricato sia il CSS che il JS
            time.sleep(1)

            # Inserisci il contenuto del body nella pagina corrente
            script_app = f"""
                let body_contenuto = document.createElement('div');
                body_contenuto.setAttribute('id', 'app');
                view_container = document.createElement('div');
                view_container.setAttribute('id', 'view_container');
                document.body.appendChild(body_contenuto);
                document.body.appendChild(view_container);
            """

            self.driver.execute_script(script_app)

            self.add_css_file("./ibridHUB/css/global.css", 'global')

            self.add_html_fragment("./ibridHUB/html/nav.html", 'dvlpz-nav-container', 'app')

            # JS GLOBAL
            self.home_scripts.add_home_link()
            self.home_scripts.add_test_link()
            self.home_scripts.add_exit_button()
            self.home_scripts.add_reload_button()

            # self.add_css_file("./ibridHUB/css/home.css", 'home')
            # self.home_scripts.add_test_exemple_launch()

            self.set_html_obj(json_obj, "config", "braces")

    # Estrae il contenuto di un file html, nello specifico il contenuto del div con id specificato
    # e lo inserisce nella pagina corrente, all'interno del div con id specificato
    def add_html_fragment(self, file_html, source_div_id, target_div_id, clear=False):

        if clear:
            # Pulisce il div prima di riempirlo
            self.clear_container(target_div_id)

        # Leggi il contenuto del file HTML
        with open(file_html, 'r', encoding='utf-8') as file:
            contenuto = file.read()

        # Estrai il contenuto del div con l'ID specifico
        soup = BeautifulSoup(contenuto, 'html.parser')
        source_div = soup.find(id=source_div_id)

        if source_div is not None:
            source_div_content = str(source_div)

            # Inserisci il contenuto del div nella pagina corrente, all'interno del div con l'ID target
            script = f"""
                let target_div = document.getElementById('{target_div_id}');
                if (target_div) {{
                    target_div.innerHTML += {repr(source_div_content)};
                }} else {{
                    console.error('Target div with ID "{target_div_id}" not found.');
                }}
            """
            self.driver.execute_script(script)

        else:
            print(f"Div with ID '{source_div_id}' not found in the provided HTML file.")

    # Inserisce un modale di successo nella pagina corrente
    def push_success_modal(self):
        self.add_html_fragment("./ibridHUB/html/modal.html",
                               'dvlpz-modal-success', 'view_container')

    # Inserisce un modale di errore nella pagina corrente
    def push_error_modal(self):
        self.add_html_fragment("./ibridHUB/html/modal_error.html",
                               'dvlpz-modal-error', 'view_container')

    def set_home_page_and_update_html_obj(self, json_obj):
        # Aggiorno l'html e provvedo ad aggiornare l'oggetto html
        self.add_css_file("./ibridHUB/css/home.css", 'home', clear=True, exclude=['global'])
        self.add_html_fragment("./ibridHUB/html/home.html", 'container_app', 'view_container',
                                           clear=True)

        self.home_scripts.add_test_exemple_launch()
        self.nav_scripts.hide_progress_bar()

        self.clear_container("braces")
        self.set_html_obj(json_obj, "config", "braces")

    def set_test_page_and_update_html_obj(self, json_obj):
        # Inserisco il css appartenente alla pagina test
        self.add_css_file("./ibridHUB/css/test.css", 'test', clear=True, exclude=['global'])
        # Inserisco il l'html appartenente alla pagina test
        self.add_html_fragment("./ibridHUB/html/test.html", "test_view", 'view_container', clear=True)

        # Nascondo la barra di caricamento
        self.nav_scripts.hide_progress_bar()

        # Aggiungo le card dei test
        self.test_scripts.push_tests_cards(json_obj, 'test_view')

        # Elimino l'oggetto html di nome braces
        self.clear_container("braces")
        # Aggiorno l'html obj in base al json obj
        self.set_html_obj(json_obj, "config", "braces")

    # # # # FINE # # # #

    # # # # METODI # # # #
    # Aggiunge un file css specificato tramite tag style, data_name serve per inserire un attributo data-name
    # all'elemento appena inserito, clear serve per eliminare tutti gli elementi <style> che non corrispondono al
    # data-name specificato, exclude è una lista di data-name che non devono essere eliminati
    def add_css_file(self, file_path, data_name, clear=False, exclude=None):
        # Verifica che il file abbia estensione ".css"
        _, ext = os.path.splitext(file_path)
        if ext != '.css':
            raise ValueError(f"File '{file_path}' non è un file CSS.")

        with open(file_path, 'r') as f:
            css_styles = f.read().replace('\n', '')

        if clear:
            # Elimina tutti gli elementi <style> che non corrispondono ai criteri
            if exclude is None:
                exclude = []

            exclude_condition = " || ".join([f"style.getAttribute('data-name') == '{name}'" for name in exclude])
            exclude_condition = f"({exclude_condition})" if exclude_condition else "false"

            script = f"""(function() {{
                let styles = document.getElementsByTagName('style');
                for (let i = styles.length - 1; i >= 0; i--) {{
                    let style = styles[i];
                    if (style.getAttribute('data-name') !== '{data_name}' && !{exclude_condition}) {{
                        style.parentNode.removeChild(style);
                    }}
                }}
            }})();"""
            self.driver.execute_script(script)

        # Crea un nuovo elemento <style> e aggiunge le proprietà CSS
        script = f"""(function() {{
            let style = document.createElement('style');
            style.innerHTML = "{css_styles}";
            if ("{data_name}") {{
                style.setAttribute('data-name', '{data_name}');
            }}
            let head = document.getElementsByTagName('head')[0];
            head.appendChild(style);
        }})();"""
        self.driver.execute_script(script)

    # Svuota un div che ha un id specifico
    def clear_container(self, container_id):
        self.driver.execute_script(f"""
            let div = document.getElementById("{container_id}");
            if (div) {{
                div.innerHTML = '';
            }}
        """)

    # Elimina un elemento dal DOM con l'id specificato
    def delete_container(self, container_id):
        script = f"""(function() {{
                let div = document.getElementById('{container_id}');
                if (div) {{
                    div.parentNode.removeChild(div);
                }}
            }})();"""
        self.driver.execute_script(script)

    # Pulisce il body della pagina corrente
    def clear_body(self):
        self.driver.execute_script("""
            document.body.innerHTML = '';
        """)

    # Ritorna un oggetto contenente i valori dell'html, per ora solo del div 'braces'
    # L'oggetto è la rappresentazione della gerarchia del div con id 'braces', dove l'id di ogni elemento
    # rappresenta la chiave dell'oggetto ed il testo all'interno dell'elemento è il suo valore
    def obj_from_html(self, brace_name="braces"):
        obj_mockup = {}

        brace_element = self.driver.find_element(By.ID, brace_name)

        brace_siblings = brace_element.find_elements(By.XPATH, "./*")

        for sibling in brace_siblings:
            sibling_name = sibling.get_attribute("id")
            sibling_value = sibling.text

            obj_mockup[sibling_name] = self.html_obj_filter_values(sibling_value)

        return obj_mockup

    # Inserisce all'interno del div con id specificato(brace_name) gli elementi dell'oggetto JSON
    def set_html_obj(self, obj_from_json, section_of_json, brace_name):

        obj_JSON_keys = obj_from_json[section_of_json].keys()
        obj_JSON_items = obj_from_json[section_of_json].items()

        print("OGGETTO JSON: ", obj_from_json[section_of_json])

        one_shot_flag = True

        # Iterazione sull'oggetto JSON
        for key, value in obj_JSON_items:
            # alla prima iterazione crea il div braces
            try:

                braces = self.driver.find_element(By.ID, brace_name)
                brace_siblings = braces.find_elements(By.XPATH, "./*")
                sibling_ids = [sibling.get_attribute('id') for sibling in brace_siblings]

                # HTML OBJ
                obj_from_HTML = self.obj_from_html(brace_name=brace_name)
                # Chiavi dell'oggetto html
                obj_HTML_keys = obj_from_HTML.keys()

                # CONTROLLO LUNGHEZZA OGGETTI
                print(f"Controllo lunghezza oggetti: json: {len(obj_JSON_keys)} html: {len(obj_HTML_keys)}")
                if len(obj_JSON_keys) != len(obj_HTML_keys):
                    print("Lunghezza diversa, aggiorno...")

                    # Se è stato giù creato l'elemento nell'html, semplicemente salto l'iterazione
                    if key in sibling_ids:

                        # Controllo se l'elemento che esiste nel DOM esiste anche nel JSON, nel caso lo elimino
                        for id_element in obj_HTML_keys:
                            if id_element not in obj_JSON_keys:
                                print(f"chiave '{id_element}' non presente in '{obj_HTML_keys}', lo elimino dal DOM...")
                                self.driver.execute_script(f"""
                                    document.getElementById('{id_element}').remove();
                                """)
                                continue
                        print(f"chiave '{key}' presente in '{sibling_ids}', salto iterazione...")
                        continue

                    print(f"Inserisco div con id '{key}' e valore '{value}'")
                    self.driver.execute_script(f"""
                        let {key} = document.createElement("div");
                        {key}.setAttribute("id", "{key}");
                        {key}.innerHTML = "{value}";
                        document.getElementById("{brace_name}").appendChild({key});
                    """)
                else:
                    return

            except Exception as e:
                # Controllo che l'eccezione non sia causata volutamente
                braces = None
                try:
                    braces = self.driver.find_element(By.ID, brace_name)
                    one_shot_flag = False
                except Exception:
                    print(f"{brace_name} non trovato lo creo...")
                    self.driver.execute_script(f"""
                        let braces = document.createElement('div');
                        braces.setAttribute('id', "{brace_name}");
                        braces.setAttribute('style', 'color: #B5D5ED;');
                        document.body.appendChild(braces);
                    """)
                # Se braces esiste e quindi l'eccezione non è stata causata volutamente, rilancio l'eccezione
                if braces and not one_shot_flag:
                    raise Exception("Errore inaspettato", str(e))

                # Al primo giro deve per forza inserire il primo elemento
                try:
                    self.driver.find_element(By.ID, key)
                except Exception:
                    print("sibling non trovato lo creo...")
                    print(f"Inserisco div con id '{key}' e valore '{value}'")
                    if one_shot_flag:
                        self.driver.execute_script(f"""
                            let {key} = document.createElement('div');
                            {key}.setAttribute('id', '{key}');
                            {key}.innerHTML = '{value}';
                            document.getElementById("{brace_name}").appendChild({key});
                        """)

    # Serve a parsare la stringa bolleana in un valore booleano
    @staticmethod
    def html_obj_filter_values(value):
        if value == "True":
            return True
        elif value == "False":
            return False

        return value

    # # # # FINE # # # #
