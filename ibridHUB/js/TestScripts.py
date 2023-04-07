import json


class TestScripts:
    def __init__(self, driver):
        self.driver = driver

    def push_tests_cards(self, json_obj, div_id):
        # Itera attraverso "test_suite" per trovare tutti i test
        test_cases = []
        for cliente in json_obj["test_suite"]["clienti"]:
            for applicazione in json_obj["test_suite"]["clienti"][cliente]["applications"]:
                for test_case, test_value in json_obj["test_suite"]["clienti"][cliente]["applications"][applicazione]["test_cases"].items():
                    test_cases.append(
                        {
                            "cliente": cliente,
                            "applicazione": applicazione,
                            "nome_test": test_value['name'],
                            "valore_test":
                                json_obj["test_suite"]["clienti"][cliente]["applications"][applicazione]["test_cases"][
                                    test_case]['script']
                        })

        # Inserisci tutti i test all'interno del div specificato utilizzando execute_script di Selenium
        for test in test_cases:
            script = f"""
                let new_element = document.createElement('div');
                new_element.className = "card";
                new_element.id = "{test['nome_test']}";
                new_element.setAttribute("data-script", {test['valore_test']});
                new_element.innerHTML = `
                    <div class='card-header' style='background-color: #18254E; color: #A9CCE3;'>
                        <h5 class='card-title'>Cliente: {test['cliente']}</h5>
                        <h6 class='card-subtitle mb-2'>Applicazione: {test['applicazione']}</h6>
                    </div>
                    <div class='card-body' style='background-color: #C0D8ED; color: #18254E;'>
                        <p class='card-text'><span class='h6' style='color: #18254E;'>Nome del test</span>: {test['nome_test']}</p>
                    </div>
                `;
                document.getElementById('{div_id}').appendChild(new_element);
            """
            self.driver.execute_script(script)
