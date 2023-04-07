class TestScripts:
    def __init__(self, driver):
        self.driver = driver

    def push_tests_cards(self, json_obj, div_id):
        # Itera attraverso "test_suite" per trovare tutti i test
        test_cases = []
        for cliente in json_obj["test_suite"]["clienti"]:
            for applicazione in json_obj["test_suite"]["clienti"][cliente]["applications"]:
                for test_case in json_obj["test_suite"]["clienti"][cliente]["applications"][applicazione]["test_cases"]:
                    test_cases.append(
                        {
                            "cliente": cliente,
                            "applicazione": applicazione,
                            "nome_test": test_case
                        })

        # Inserisci tutti i test all'interno del div specificato utilizzando execute_script di Selenium
        for test in test_cases:
            script = f"""
                let new_element = document.createElement('div');
                new_element.className = "card";
                new_element.id = "{test['nome_test']}";
                new_element.setAttribute("data-script", "{test['cliente']}" + " || " + "{test['applicazione']}" + " || " + "{test['nome_test']}");
                new_element.innerHTML = `
                    <div class='card-header' style='background-color: #18254E; color: #A9CCE3;'>
                        <h5 class='card-title'>Cliente: {test['cliente']}</h5>
                        <h6 class='card-subtitle mb-2'>Applicazione: {test['applicazione']}</h6>
                    </div>
                    <div class='card-body' style='background-color: #C0D8ED; color: #18254E;'>
                        <p class='card-text'><span class='h6' style='color: #18254E;'>Nome del test</span>: {test['nome_test']}</p>
                        <button id="execute_test_button" type="button" class="btn btn-success dvlpz_blue_button">Esegui</button>
                    </div>
                `;
                
                    new_element.querySelector("#execute_test_button").addEventListener("click", function() {{
                    document.getElementById('test_coordinate').textContent = new_element.getAttribute('data-script');
                    this.textContent = "ESEGUO...";
                    document.getElementById('run_test_flag').textContent = "True";
                }});
                
                document.getElementById('{div_id}').appendChild(new_element);
                
            """
            self.driver.execute_script(script)

    def handle_action_choice(self):
        script = """
            const mySelect = document.getElementById('action_select');

            function handleSelectChange(event) {
                const selectedValue = event.target.value;
                console.log('Valore selezionato:', selectedValue);
                const select_container = document.getElementById('select_container');
            
                // Rimuovi tutti i contenitori se esistono
                const get_page_container = document.getElementById('get_page_container');
                const click_container = document.getElementById('click_container');
                const find_element_container = document.getElementById('find_element_container');
                const find_elements_container = document.getElementById('find_elements_container');
                const write_container = document.getElementById('write_container');
                
                if (get_page_container) select_container.removeChild(get_page_container);
                if (click_container) select_container.removeChild(click_container);
                if (find_element_container) select_container.removeChild(find_element_container);
                if (find_elements_container) select_container.removeChild(find_elements_container);
                if (write_container) select_container.removeChild(write_container);
            
                // Se l'utente ha selezionato "get_page" aggiungi un input per l'URL
                if (selectedValue == "get_page") {
                    const select_container = document.getElementById('select_container');
                    const get_page_container = document.createElement('div');
                    get_page_container.setAttribute('id', 'get_page_container');
                    get_page_container.classList.add('mb-3');
                    get_page_container.innerHTML = `
                        <label for="get_page_label" class="form-label">URL</label>
                        <input type="text" class="form-control" id="get_page_label"
                                       placeholder="inserisci l'URL della pagina">
                    `;
                    select_container.appendChild(get_page_container);
                } else if (selectedValue == "click") {
                    const select_container = document.getElementById('select_container');
                    const click_container = document.createElement('div');
                    click_container.setAttribute('id', 'click_container');
                    click_container.classList.add('mb-3');
                    click_container.innerHTML = `
                        <label for="click_label" class="form-label">Selettore</label>
                        <input type="text" class="form-control" id="click_label"
                                        placeholder="inserisci il selettore">
                    `;
                    select_container.appendChild(click_container);
                } else if (selectedValue == "find_element") {
                    const select_container = document.getElementById('select_container');
                    const find_element_container = document.createElement('div');
                    find_element_container.setAttribute('id', 'find_element_container');
                    find_element_container.classList.add('mb-3');
                    find_element_container.innerHTML = `
                    <label for="find_element_label" class="form-label">Selettore find element</label>
                    <input type="text" class="form-control" id="find_element_label" placeholder="inserisci il selettore">
                    `;
                    select_container.appendChild(find_element_container);
                }else if (selectedValue == "find_elements") {
                    const select_container = document.getElementById('select_container');
                    const find_elements_container = document.createElement('div');
                    find_elements_container.setAttribute('id', 'find_elements_container');
                    find_elements_container.classList.add('mb-3');
                    find_elements_container.innerHTML = `
                        <label for="find_elements_label" class="form-label">Selettore</label>
                        <input type="text" class="form-control" id="find_elements_label" placeholder="inserisci il selettore">
                        <label for="find_elements_index" class="form-label">Index</label>
                        <input type="number" class="form-control" id="find_elements_index" placeholder="inserisci l'index">
                        <label for="find_elements_text" class="form-label">Testo</label>
                        <input type="text" class="form-control" id="find_elements_text" placeholder="inserisci il testo">
                    `;
                    select_container.appendChild(find_elements_container);
                } else if ( selectedValue == "write") {
                    const select_container = document.getElementById('select_container');
                    const write_container = document.createElement('div');
                    write_container.setAttribute('id', 'write_container');
                    write_container.classList.add('mb-3');
                    write_container.innerHTML = `
                        <label for="write_label" class="form-label">Selettore</label>
                        <input type="text" class="form-control" id="write_label" placeholder="inserisci il selettore">
                        <input class="form-check-input" type="checkbox" value="True" id="send_enter_write">
                        <label class="form-check-label" for="send_enter_write">Premi invio</label>
                    `;
                    select_container.appendChild(write_container);
                }
            }
            
            mySelect.addEventListener('change', handleSelectChange);
            
            if (mySelect.value == "get_page") {
                const select_container = document.getElementById('select_container');
                const get_page_container = document.createElement('div');
                get_page_container.setAttribute('id', 'get_page_container');
                get_page_container.classList.add('mb-3');
                get_page_container.innerHTML = `
                    <label for="get_page_label" class="form-label">URL</label>
                    <input type="text" class="form-control" id="get_page_label"
                                   placeholder="inserisci l'URL della pagina">
                `;
                select_container.appendChild(get_page_container);
            }
        """
        self.driver.execute_script(script)
