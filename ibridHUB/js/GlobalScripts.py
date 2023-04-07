class GlobalScripts:

    def __init__(self, driver):
        self.driver = driver

    # Aggiungi il CSS di Bootstrap
    def add_bootstrap_css(self):
        self.driver.execute_script("""
                    let link = document.createElement('link');
                    link.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css';
                    link.rel = 'stylesheet';
                    link.integrity = 'sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp';
                    link.crossOrigin = 'anonymous';
                    document.head.appendChild(link);
                """)

    # Aggiungi il JS di Bootstrap
    def add_bootstrap_js(self):
        self.driver.execute_script("""
                        let script = document.createElement('script');
                        script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js';
                        script.integrity = 'sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N';
                        script.crossOrigin = 'anonymous';
                        document.body.appendChild(script);
                    """)

    # Aggiungi il DOCTYPE
    def insert_DOCTYPE(self):
        self.driver.execute_script(
            "document.doctype || document.insertBefore(document.implementation.createDocumentType('html', '', ''), document.documentElement);")

    # Aggiungi l'attributo 'lang' al tag <html>
    def insert_language(self):
        self.driver.execute_script("document.documentElement.setAttribute('lang', 'it');")

    # Aggiungi il tag <meta charset="UTF-8"> nel tag <head>
    def insert_meta_charset(self):
        self.driver.execute_script("""
                    let meta = document.createElement('meta');
                    meta.setAttribute('charset', 'UTF-8');
                    document.head.appendChild(meta);
                """)

    # Aggiungi il tag <title> nel tag <head>
    def insert_title(self):
        self.driver.execute_script("""
                    let title = document.createElement('title');
                    title.innerHTML = 'TESTING HUB';
                    document.head.appendChild(title);
                """)