# WebDriver
from selenium import webdriver

# Util per leggere i processi
import psutil

# Keys, per emulare la pressione di un tasto
from selenium.webdriver import Keys

# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService

# Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService

# Edge
from selenium.webdriver.edge.service import Service as EdgeService

# Util per il wait
import time

# Eccezioni per il wait
from selenium.common import ElementNotVisibleException, ElementNotSelectableException, TimeoutException, \
    NoSuchElementException, ElementNotInteractableException

# Utile per specificare il tipo di selettore
from selenium.webdriver.common.by import By
# Il WebElement
from selenium.webdriver.remote.webelement import WebElement
# Expected conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
# WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait


class Utils4:

    def __init__(self, browser):

        for proc in psutil.process_iter():
            if proc.name() == "chrome.exe" and browser == "chrome":
                proc.kill()
                continue
            elif proc.name() == "firefox.exe" and browser == "firefox":
                proc.kill()
                continue
            elif proc.name() == "msedge.exe" and browser == "edge":
                proc.kill()

        if browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--incognito')
            self.service_obj = ChromeService("/Users/a.lopez/Documents/chromedriver")
            self.driver = webdriver.Chrome(service=self.service_obj, options=chrome_options)
            self.driver.maximize_window()
        elif browser == 'firefox':
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--private')
            self.service_obj = FirefoxService("/Users/a.lopez/Documents/geckodriver")
            self.driver = webdriver.Firefox(service=self.service_obj, options=firefox_options)
            self.driver.maximize_window()
        elif browser == 'edge':
            edge_options = webdriver.EdgeOptions()
            edge_options.add_argument('--inprivate')
            self.service_obj = EdgeService("/Users/a.lopez/Documents/msedgedriver")
            self.driver = webdriver.Edge(service=self.service_obj, options=edge_options)
            self.driver.maximize_window()

        self.wait_t1_pf1 = WebDriverWait(self.driver, timeout=1, poll_frequency=1,
                                         ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                             ElementNotInteractableException])

    # # # RITORNA IL DRIVER
    def get_driver(self):
        return self.driver

    # # #

    # # # CHIUDE IL DRIVER
    def close_driver(self):
        self.driver.close()

    # # # APRE LA PAGINA DESIDERATA, INGRANDISCE LA FINESTRA DEL BROWSER
    # |page| = stringa che rappresenta l'url della pagina
    def get_page(self, page: str):
        self.driver.get(page)

    # # # Wait personalizzato in selenium
    def custom_wait(self, timeout=2, condition=EC.title_contains("__falsa_condizione__")):
        try:
            WebDriverWait(self.driver, timeout).until(condition)
        except TimeoutException:
            pass

    @staticmethod
    # # # ATTESA IMPLICITA
    def sleepping_wait(seconds=5):
        time.sleep(seconds)

    # # # EVIDENZIA UN WEB ELEMENT
    # # # |webelement| = WebElement da evidenziare
    def highlight_element(self, webelement: WebElement):

        css = self.generate_css_selector(webelement) + ' {\
        outline: 5px solid #5CFFCB !important; \
        border: 5px solid transparent !important; \
        border-bottom: 5px solid #BCB6FF !important; \
        box-shadow: 0 0 5px 10px #8F85FF !important; \
        border-radius: 5px !important; \
        }'

        self.driver.execute_script(
            'var style = document.createElement("style"); style.innerHTML = "{}";\
             document.head.appendChild(style);\
             style.setAttribute("data-highlight-style", "");'
            .format(css))

    # # # EVIDENZIA UN WEB ELEMENT CON BORDO ROSSO
    # # # |webelement| = WebElement da evidenziare
    def highlight_error(self, webelement: WebElement):
        css = self.generate_css_selector(webelement) + ' {border: 5px solid red !important;}'

        self.driver.execute_script(
            'var style = document.createElement("style"); style.innerHTML = "{}";\
             document.head.appendChild(style);\
             style.setAttribute("data-highlight-style", "");'
            .format(css))

    # # # EVIDENZIA IL BODY CON BORDO ROSSO
    def highlight_body_error(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.highlight_error(body)

    # # # RIMUOVE GLI HIGHLIGHTS
    # # # |timeout| = tempo di attesa prima di rimuovere gli highlights
    def remove_highlights(self, timeout=None):
        if timeout is not None:
            self.custom_wait(timeout)
        else:
            self.custom_wait(2)
        self.driver.execute_script('var styleElements = document.querySelectorAll("style[data-highlight-style]"); \
                                    styleElements.forEach(function(e){e.parentNode.removeChild(e)});')

    @staticmethod
    # # # ACCETTA UN WEBELEMENT E RITORNA IL SUO SELETTORE CSS PIU' SPECIFICO POSSIBILE
    def generate_css_selector(webelement: WebElement) -> str:
        if not isinstance(webelement, WebElement):
            raise TypeError("L'input dovrebbe essere un WebElement.")

        # Estrae gli attributi dell'elemento web
        def get_attributes(el: WebElement) -> str:
            attributes = []
            element_properties = ["id", "class", "name"]
            for prop in element_properties:
                attribute_value = el.get_attribute(prop)
                if attribute_value and prop == "class":
                    attribute_value = attribute_value.replace(" ", ".")
                    attributes.append(f".{attribute_value}")
                elif attribute_value:
                    attributes.append(f"[{prop}='{attribute_value}']")
            return "".join(attributes)

        # Cerca il selettore css più specifico possibile
        def find_css_selector_recursively(element: WebElement, selector: str = "") -> str:
            parent_element = element.find_element(By.XPATH, '..')
            tag_name = element.tag_name
            siblings = parent_element.find_elements(By.XPATH, f'*[local-name()="{tag_name}"]')
            current_selector = f"{tag_name}{get_attributes(element)}"
            if len(siblings) > 1:
                index = siblings.index(element) + 1
                current_selector = f"{current_selector}:nth-of-type({index})"

            if parent_element.tag_name.lower() != "html":
                return find_css_selector_recursively(parent_element, f"{current_selector} > {selector}")
            else:
                return f"{current_selector} > {selector}"

        try:
            css_selector = find_css_selector_recursively(webelement).strip(" >")
        except Exception as e:
            print(f"Errore durante la generazione del CSS selector: {str(e)}")
            css_selector = "Impossibile generare un CSS selector per questo elemento."

        return css_selector

    def center_element(self, webelement):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", webelement
        )

    # # # CERCA UN ELEMENTO NELLA PAGINA PER 30 SECONDI E NE CONTROLLA LA PRESENZA OGNI SECONDO
    # # # Trovato l'elemento sfrutta la funzione highlight_element per evidenziarlo
    def find_element(self, selector, by='css'):
        found = False
        count = 0
        while not found:
            try:
                if by == "css":
                    element = self.wait_t1_pf1.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                elif by == "id":
                    element = self.wait_t1_pf1.until(EC.presence_of_element_located((By.ID, selector)))
                elif by == "xpath":
                    element = self.wait_t1_pf1.until(EC.presence_of_element_located((By.XPATH, selector)))
                elif by == "link-text":
                    element = self.wait_t1_pf1.until(EC.presence_of_element_located((By.LINK_TEXT, selector)))
                else:
                    raise ValueError("Tipo di selettore non supportato: {}".format(by))
                found = True
                print("Elemento trovato")
                self.center_element(element)
                self.highlight_element(element)
                return element
            except TimeoutException:
                count += 1
                if count >= 31:
                    print("Timeout raggiunto, interrompo la ricerca")
                    raise NoSuchElementException("Elemento non trovato: {}".format(selector))
                else:
                    print("Elemento non trovato, tentativo " + str(count) + "/30")
                    self.highlight_body_error()
                    self.remove_highlights(timeout=1)
                    continue

    # # # CERCA PIU' ELEMENTI NELLA PAGINA PER 30 SECONDI E NE CONTROLLA LA PRESENZA OGNI SECONDO
    # # # index se specificato tramite stringa numerica, ritorna l'elemento che si trova in quella specifica posizione
    def find_elements(self, selector, by='css', index=None, text=None):
        found = False
        count = 0
        while not found:
            try:
                if by == "css":
                    elements = self.wait_t1_pf1.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                elif by == "id":
                    elements = self.wait_t1_pf1.until(EC.presence_of_all_elements_located((By.ID, selector)))
                elif by == "xpath":
                    elements = self.wait_t1_pf1.until(EC.presence_of_all_elements_located((By.XPATH, selector)))
                elif by == "link-text":
                    elements = self.wait_t1_pf1.until(EC.presence_of_all_elements_located((By.LINK_TEXT, selector)))
                else:
                    raise ValueError("Tipo di selettore non supportato: {}".format(by))
                found = True
                print("Elementi trovati")
                if text is not None:
                    for element in elements:
                        if text in element.text:
                            self.center_element(element)
                            self.highlight_element(element)
                            return element
                    raise NoSuchElementException("Nessun elemento trovato con il testo: {}".format(text))
                elif index is not None:
                    element = elements[int(index)]
                    self.center_element(element)
                    self.highlight_element(element)
                    return element
                else:
                    for element in elements:
                        try:
                            self.highlight_element(element)
                        except Exception:
                            print("Errore durante l'highlight dell'elemento: {}".format(element))
                    return elements
            except TimeoutException:
                count += 1
                if count >= 31:
                    print("Timeout raggiunto, interrompo la ricerca")
                    raise NoSuchElementException("Elementi non trovati: {}".format(selector))
                else:
                    print("Elementi non trovati, tentativo " + str(count) + "/30")
                    self.highlight_body_error()
                    self.remove_highlights(timeout=1)
                    continue

    # # # UTILIZZA IL FIND_ELEMENT PER CLICCARE UN ELEMENTO
    # # # Rimuove gli highlights se esistono
    def click(self, selector, by='css'):
        webelement = self.find_element(selector, by=by)
        found = False
        count = 0
        while not found:
            try:
                found = True
                self.remove_highlights()
                webelement.click()
            except Exception as e:
                count += 1
                if count >= 11:
                    print("Timeout raggiunto, lancio eccezione")
                    raise Exception(str(e))
                else:
                    print("Errore durante il click, tentativo " + str(count) + "/10")
                    self.highlight_body_error()
                    self.remove_highlights(timeout=1)
                    continue

    # # # PRENDE UN WEBELEMENT ED EFFETTUA IL CLICK SU DI ESSO
    # # # Rimuove gli highlights se esistono
    def click_webelement(self, webelement):
        found = False
        count = 0
        while not found:
            try:
                found = True
                self.remove_highlights()
                webelement.click()
            except Exception as e:
                count += 1
                if count >= 11:
                    print("Timeout raggiunto, lancio eccezione")
                    raise Exception(str(e))
                else:
                    print("Errore durante il click, tentativo " + str(count) + "/10")
                    self.highlight_body_error()
                    self.remove_highlights(timeout=1)
                    continue

    def write(self, selector, text, by='css', press_enter=False):
        webelement = self.find_element(selector, by=by)

        try:
            self.remove_highlights()
            webelement.send_keys(text)
            if press_enter:
                webelement.send_keys(Keys.ENTER)
        except Exception:
            print("Errore durante la scrittura")

    # # # GESTISCE LA SELEZIONE DI UN ELEMENTO DALLA DROPDOWN
    # # # |text|: testo visibile dell'elemento da selezionare
    # # # |index|: indice dell'elemento da selezionare
    # # # |value|: valore dell'elemento da selezionare
    def select_dropdown(self, selector, text=None, by='css', index=None, value=None):
        webelement = self.find_element(selector, by=by)

        if webelement.tag_name != "select":
            raise ValueError(f"L'elemento non è una select dropdown -> {webelement.tag_name}")

        dropdown = Select(webelement)
        if text is not None:
            self.remove_highlights()
            dropdown.select_by_visible_text(text)
        elif index is not None:
            self.remove_highlights()
            dropdown.select_by_index(index)
        elif value is not None:
            self.remove_highlights()
            dropdown.select_by_value(value)


