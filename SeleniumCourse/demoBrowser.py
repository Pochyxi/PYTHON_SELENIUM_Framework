from ibridHUB.appHandler import AppHandler
from utils.Utils4.Utils4 import Utils4

action = Utils4('edge')

# aggiungi_elementi_mancanti(action.driver)
app = AppHandler(action)


action.find_elements("button")

action.custom_wait(300000)

# action.get_page(get_practice1_elements("practice_page_1"))

# action.find_elements("td", index="0")

# # Testiamo il click nel caso in cui l'elemento non sia cliccabile, proverà a farlo 15 volte e poi lancerà un'eccezione
# action.click("#mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(11) > td:nth-child(2) > button")

# cookies = action.find_element(get_practice1_elements("button_cookies"))

# elements = action.find_elements("button", text="Consent")

# action.click_webelement(cookies)

# utils = action.find_elements("strong")

# action.remove_highlights()

# action.write(get_practice1_elements("input_writing"), "Developez")

# non_lo_trova = action.find_element("button[class='fc-button fc-cta-consent fc-primary-buttonzzzz']")

# action.select_dropdown(get_practice1_elements("country_select"), index="2")

# action.get_page(get_practice2_elements("practice_page_2"))

# action.find_elements("input")

# action.close_driver()

