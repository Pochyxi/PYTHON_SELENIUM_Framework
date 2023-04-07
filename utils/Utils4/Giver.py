def get_practice1_elements(case_string):
    def switch_case(case_value):
        switch_dict = {
            "button_cookies": button_cookies,
            "input_writing": input_writing,
            "practice_page_1": practice_page_1,
            "country_select": country_select,
        }
        return switch_dict.get(case_value, case_default)()

    def practice_page_1():
        return "https://www.tutorialspoint.com/selenium/selenium_automation_practice.htm"

    def button_cookies():
        return "button[class='fc-button fc-cta-consent fc-primary-button']"

    def country_select():
        return "#mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(9) > td:nth-child(2) > select"

    def input_writing():
        return "#mainContent > div:nth-child(6) > div > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]"

    def case_default():
        return "Nessuno switch corrispondente trovato"

    input_case_value = case_string

    result = switch_case(input_case_value)

    return result


def get_practice2_elements(case_string):
    def switch_case(case_value):
        switch_dict = {
            "practice_page_2": practice_page_2,
            "input_hide_show": input_hide_show,
        }
        return switch_dict.get(case_value, case_default)()

    def practice_page_2():
        return "https://rahulshettyacademy.com/AutomationPractice/"

    def input_hide_show():
        return "#name"

    def case_default():
        return "Nessuno switch corrispondente trovato"

    input_case_value = case_string

    result = switch_case(input_case_value)

    return result
