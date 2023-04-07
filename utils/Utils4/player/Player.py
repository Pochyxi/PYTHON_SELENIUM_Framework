from utils.Utils4.Utils4 import Utils4


class Player:
    def __init__(self, utils4: Utils4, pocke_list):
        self.pocke_list = pocke_list
        self.utils4 = utils4

    def throw_pockes(self):
        for pocke in self.pocke_list:
            action_name = pocke['name']
            action_args = pocke['args']

            # Esegue l'azione corrispondente
            if action_name == 'get_page':
                self.utils4.get_page(*action_args)
            elif action_name == 'custom_wait':
                self.utils4.custom_wait(*action_args)
            elif action_name == 'click':
                self.utils4.click(*action_args)
            elif action_name == 'find_element':
                self.utils4.find_element(*action_args)
            elif action_name == 'find_elements':
                self.utils4.find_elements(*action_args)
            elif action_name == 'write':
                self.utils4.write(*action_args)
            elif action_name == 'select_dropdown':
                self.utils4.select_dropdown(*action_args)

            # Se nessun comando corrisponde, solleva un'eccezione
            else:
                raise ValueError(f"Comando '{action_name}' non riconosciuto.")