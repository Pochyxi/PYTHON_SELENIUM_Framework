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

    def toast(self, message, bg_text="success"):
        text_header = "Messaggio di errore" if bg_text == "danger" else "Messaggio di successo"

        script = f"""
            let toast_container = document.createElement('div');
            toast_container.setAttribute('id', 'toast_container');
            
            toast_container.innerHTML = `
                <div class="toast-container position-fixed bottom-0 end-0 p-3">
                  <div id="liveToast" class="toast text-bg-{bg_text}" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header">
                      <strong class="me-auto">{text_header}</strong>
                      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                      {message}
                    </div>
                  </div>
                </div>
            `;
            
            document.body.appendChild(toast_container);
            
            const my_toast = document.getElementById('liveToast')
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(my_toast);
            toastBootstrap.show();
        """

        self.driver.execute_script(script)
