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
            
            let action_counter = 0;
            
            // Imposta la select al suo valore di default
            const reset_select = () => {
                mySelect.selectedIndex = 0;
            };

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
            
                // GET PAGE
                if (selectedValue == "get_page") {
                    const select_container = document.getElementById('select_container');
                    
                    const get_page_container = document.createElement('div');
                    get_page_container.setAttribute('id', 'get_page_container');
                    get_page_container.classList.add('mb-3');
                    get_page_container.innerHTML = `
                        <label for="get_page_label" class="form-label">URL</label>
                        <input type="text" class="form-control" id="get_page_label"
                                       placeholder="inserisci l'URL della pagina">
                        <button id="get_page_button" type="button" class="btn btn-success dvlpz_blue_button mt-2">Aggiungi</button>
                    `;
                    
                    select_container.appendChild(get_page_container);
                    
                    // GET PAGE ADD BUTTON
                    const get_page_button = document.getElementById('get_page_button');
                    
                    // GET PAGE AGGIUNGI FUNCTION
                    get_page_button.addEventListener('click', function() {
                        const get_page_input = document.getElementById('get_page_label');
                        const get_page_input_value = get_page_input.value;
                        
                        new_div = document.createElement('div');
                        new_div.id = "action_" + action_counter;
                        action_counter += 1;
                        new_div.textContent = "ID:" + "'" + new_div.id + "' " + "Vai alla pagina con URL " + "'" + get_page_input_value + "'";
                        
                        new_div.setAttribute('data_action', "get_page" + " || " + get_page_input_value);
                        
                        const action_div = document.getElementById('action_container');
                        action_div.appendChild(new_div);
                        
                        get_page_input.value = "";
                    });
                    
                // CLICK
                } else if (selectedValue == "click") {
                    const select_container = document.getElementById('select_container');
                    
                    const click_container = document.createElement('div');
                    click_container.setAttribute('id', 'click_container');
                    click_container.classList.add('mb-3');
                    click_container.innerHTML = `
                        <label for="click_label" class="form-label">Selettore</label>
                        <input type="text" class="form-control" id="click_label"
                                        placeholder="inserisci il selettore">
                        <button id="click_button" type="button" class="btn btn-success dvlpz_blue_button mt-2">Aggiungi</button>                
                    `;
                    
                    select_container.appendChild(click_container);
                    
                    // CLICK ADD BUTTON
                    const click_button = document.getElementById('click_button');
                    
                    // CLICK AGGIUNGI FUNCTION
                    click_button.addEventListener('click', function() {
                        const click_input = document.getElementById('click_label');
                        const click_input_value = click_input.value;
                        
                        new_div = document.createElement('div');
                        new_div.id = "action_" + action_counter;
                        action_counter += 1;
                        new_div.textContent =  "ID:" + "'" + new_div.id + "' " + "Clicca elemento con selettore " + "'" + click_input_value + "'";
                        
                        new_div.setAttribute('data_action', "click" + " || " + click_input_value);
                        
                        const action_div = document.getElementById('action_container');
                        action_div.appendChild(new_div);
                        
                        click_input.value = "";
                    });
                    
                // FIND_ELEMENT
                } else if (selectedValue == "find_element") {
                    const select_container = document.getElementById('select_container');
                    
                    const find_element_container = document.createElement('div');
                    find_element_container.setAttribute('id', 'find_element_container');
                    find_element_container.classList.add('mb-3');
                    find_element_container.innerHTML = `
                    <label for="find_element_label" class="form-label">Selettore find element</label>
                    <input type="text" class="form-control" id="find_element_label" placeholder="inserisci il selettore">
                    <button id="find_element_button" type="button" class="btn btn-success dvlpz_blue_button mt-2">Aggiungi</button>  
                    `;
                    
                    select_container.appendChild(find_element_container);
                    
                    // FIND_ELEMENT ADD BUTTON
                    const find_element_button = document.getElementById('find_element_button');
                    
                    // FIND_ELEMENT AGGIUNGI FUNCTION
                    find_element_button.addEventListener('click', function() {
                        const find_element_input = document.getElementById('find_element_label');
                        const find_element_input_value = find_element_input.value;
                        
                        new_div = document.createElement('div');
                        new_div.id = "action_" + action_counter;
                        action_counter += 1;
                        new_div.textContent = "ID:" + "'" + new_div.id + "' " + "Cerca elemento con selettore " + "'" +  find_element_input_value + "'";
                        
                        new_div.setAttribute('data_action', "find_element" + " || " + find_element_input_value);
                        
                        const action_div = document.getElementById('action_container');
                        action_div.appendChild(new_div);
                        
                        find_element_input.value = "";
                    });
                    
                // FIND_ELEMENTS
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
                        <button id="find_elements_button" type="button" class="btn btn-success dvlpz_blue_button mt-2">Aggiungi</button>
                    `;
                    
                    select_container.appendChild(find_elements_container);
                    
                    // FIND_ELEMENTS ADD BUTTON
                    const find_elements_button = document.getElementById('find_elements_button');
                    
                    // FIND_ELEMENTS AGGIUNGI FUNCTION
                    find_elements_button.addEventListener('click', function() {
                        const find_elements_input = document.getElementById('find_elements_label');
                        const find_elements_input_value = find_elements_input.value;
                        
                        const find_elements_index = document.getElementById('find_elements_index');
                        const find_elements_index_value = find_elements_index.value.lenght > 0 ? find_elements_index.value : "None";
                        
                        const find_elements_text = document.getElementById('find_elements_text');
                        const find_elements_text_value = find_elements_text.value.length > 0 ? find_elements_text.value : "None";
                        
                        new_div = document.createElement('div');
                        new_div.id = "action_" + action_counter;
                        action_counter += 1;
                        new_div.textContent = "ID:" + "'" + new_div.id + "' " + "Cerca elementi con selettore " + "'" +  find_elements_input_value + "', " + "con index  " + "'" + find_elements_index_value + "', " + "con testo " +  "'" + find_elements_text_value + "'";
                        
                        new_div.setAttribute('data_action', "find_elements" + " || " + find_elements_input_value + " || " + "css" + " || " + find_elements_index_value + " || " + find_elements_text_value);
                        
                        const action_div = document.getElementById('action_container');
                        action_div.appendChild(new_div);
                        
                        find_elements_input.value = "";
                        find_elements_index.value = "";
                        find_elements_text.value = "";
                    });
                    
                // WRITE
                } else if ( selectedValue == "write") {
                    const select_container = document.getElementById('select_container');
                    
                    const write_container = document.createElement('div');
                    write_container.setAttribute('id', 'write_container');
                    write_container.classList.add('mb-3');
                    write_container.innerHTML = `
                        <label for="write_label" class="form-label">Selettore</label>
                        <input type="text" class="form-control" id="write_label" placeholder="inserisci il selettore">
                        
                        <label for="write_text" class="form-label">Testo</label>
                        <input type="text" class="form-control" id="write_text" placeholder="Testo da inserire">
                        
                        <div class="mt-2 d-flex justify-content-start">
                            <label class="form-check-label text-start me-2" for="send_enter_write">Premi invio</label>
                            <input class="form-check-input" type="checkbox" value="True" id="send_enter_write">
                        </div>
                        
                        <div>
                            <button id="write_button" type="button" class="btn btn-success dvlpz_blue_button mt-2">Aggiungi</button>
                        </div>
                    `;
                    
                    select_container.appendChild(write_container);
                    
                    // WRITE ADD BUTTON
                    const write_button = document.getElementById('write_button');
                    
                    // WRITE AGGIUNGI FUNCTION
                    write_button.addEventListener('click', function() {
                        const write_input = document.getElementById('write_label');
                        const write_input_value = write_input.value;
                        
                        const write_text = document.getElementById('write_text');
                        const write_text_value = write_text.value;
                         
                        const send_enter_write = document.getElementById('send_enter_write').checked ? "True" : "False";
                        
                        new_div = document.createElement('div');
                        new_div.id = "action_" + action_counter;
                        action_counter += 1;
                        new_div.textContent = "ID:" + "'" + new_div.id + "' " + "Scrivi su elemento con selettore " + "'" +  write_input_value + "', " + "e clicca invio " + "'" + send_enter_write + "'";
                        
                        new_div.setAttribute('data_action', "write" + " || " + write_input_value + " || " + write_text_value + " || " + "css" + " || " + send_enter_write);
                        
                        const action_div = document.getElementById('action_container');
                        action_div.appendChild(new_div);
                        
                        write_input.value = "";
                        write_text.value = "";
                    });
                }
            }
            
            // SELECT
            mySelect.addEventListener('change', handleSelectChange);
            
            // DEFAULT
            if (mySelect.value == "get_page") {
                const select_container = document.getElementById('select_container');
                const get_page_container = document.createElement('div');
                get_page_container.setAttribute('id', 'get_page_container');
                get_page_container.classList.add('mb-3');
                get_page_container.innerHTML = `
                    <label for="get_page_label" class="form-label">URL</label>
                    <input type="text" class="form-control" id="get_page_label"
                                   placeholder="inserisci l'URL della pagina">
                    <button id="get_page_button" type="button" class="btn btn-success dvlpz_blue_button mt-2">Aggiungi</button>
                `;
                
                select_container.appendChild(get_page_container);
                
                // ADD BUTTON
                const get_page_button = document.getElementById('get_page_button');
                
                // AGGIUNGI FUNCTION
                get_page_button.addEventListener('click', function() {
                    const get_page_input = document.getElementById('get_page_label');
                    const get_page_input_value = get_page_input.value;
                    
                    new_div = document.createElement('div');
                    new_div.id = "action_" + action_counter;
                    action_counter += 1;
                    new_div.textContent = "ID:" + "'" + new_div.id + "' " + "Vai alla pagina con URL " + "'" + get_page_input_value + "'";
                    
                    new_div.setAttribute('data_action', "get_page" + " || " + get_page_input_value);
                    
                    const action_div = document.getElementById('action_container');
                    action_div.appendChild(new_div);
                    
                    get_page_input.value = "";
                });
            }
        """
        self.driver.execute_script(script)

    def add_test_case_button(self):
        script = """
            // IL PULSANTE PER AGGIUNGERE IL TEST CASE
            const save_test_case_button = document.getElementById('save_test_case_button');
            
            const save_test = () => {
                // IL CONTAINER DELLE ACTION
                const test_case_container = document.getElementById('action_container');
            
                // LA FLAG CHE DETERMINA L'AGGIUNTA DI UN NUOVO TEST CASE
                const save_test_case_flag = document.getElementById('save_test_case_flag');
                
                // IL CONTENUTO DEL TEST CASE
                const test_case_list = document.getElementById('test_case_list');
                
                // COORDINATE DEL NUOVO TEST CASE
                const test_case_coordinates = document.getElementById('test_case_coordinates');
                
                // NOME CLIENTE
                const nome_cliente = document.getElementById('nome_cliente');
                
                // NOME APPLICAZIONE 
                const nome_applicazione = document.getElementById('nome_applicazione');
                
                // NOME TEST
                const nome_test = document.getElementById('nome_test');
                
                // LISTA DA POPOLARE E POI INSERIRE NELLA LISTA DEL TEST CASE
                let list = [];
                
                
                for (let i = 0; i < test_case_container.children.length; i++) {
                    list.push(test_case_container.children[i].getAttribute('data_action'));
                }
                
                // AGGIUNGO IL TEST CASE ALLA LISTA
                test_case_list.textContent = JSON.stringify(list);
                
                // AGGIUNGO LE COORDINATE DEL TEST CASE
                test_case_coordinates.textContent = nome_cliente.value + " || " + nome_applicazione.value + " || " + nome_test.value;
                
                // SETTO LA FLAG A TRUE
                save_test_case_flag.textContent = "True";
            
            }; 
            
            save_test_case_button.addEventListener('click', save_test);
        """

        self.driver.execute_script(script)
