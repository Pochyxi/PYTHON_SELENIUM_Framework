class HomeScripts:

    def __init__(self, driver):
        self.driver = driver

        # Implementa un bottone nella pagina per lo spegnimento dell'applicazione
    def add_exit_button(self):
        self.driver.execute_script("""
            let button = document.getElementById('click_me');
            button.addEventListener('click', function() { 
                const flag_traductor = (flag_value) => {
                    if (flag_value == "True") {
                        return "False";
                    };
                    return "True";
                };
                let flag_value = document.getElementById('flag').innerHTML = flag_traductor(document.getElementById('flag').innerHTML)
                button.innerHTML = "ESEGUO CHIUSURA";
            });
        """)

    # Implementa un bottone nella pagina per il ricaricamento della pagina
    def add_reload_button(self):
        self.driver.execute_script("""
                let button = document.getElementById('reload_button');
                button.addEventListener('click', function() { 
                    const flag_traductor = (flag_value) => {
                        if (flag_value == "True") {
                            return "False";
                        };
                        return "True";
                    };
                    let flag_value = document.getElementById('home_flag').innerHTML = flag_traductor(document.getElementById('home_flag').innerHTML)
                    button.innerHTML = "RICARICO";
                    document.querySelector('div.progress').removeAttribute('style');
                });
            """)

    def add_test_link(self):
        self.driver.execute_script("""
            let button = document.getElementById('test_link');
            button.addEventListener('click', function() {
                const flag_traductor = (flag_value) => {
                        if (flag_value == "True") {
                            return "False";
                        };
                        return "True";
                    };
                    document.getElementById('test_flag').innerHTML = flag_traductor(document.getElementById('test_flag').innerHTML)
                    document.getElementById('router').innerHTML = "test"
                    document.querySelector('div.progress').removeAttribute('style');
            });
        """)

    def add_home_link(self):
        self.driver.execute_script("""
            let button = document.getElementById('home_link');
            button.addEventListener('click', function() {
                const flag_traductor = (flag_value) => {
                        if (flag_value == "True") {
                            return "False";
                        };
                        return "True";
                    };
                    document.getElementById('home_flag').innerHTML = flag_traductor(document.getElementById('home_flag').innerHTML)
                    document.getElementById('router').innerHTML = "home"
                    document.querySelector('div.progress').removeAttribute('style');
            });
        """)


