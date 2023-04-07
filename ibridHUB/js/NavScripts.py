class NavScripts:

    def __init__(self, driver):
        self.driver = driver

    def hide_progress_bar(self):
        self.driver.execute_script("""
            document.querySelector('div.progress').setAttribute('style', 'display: none');
        """)