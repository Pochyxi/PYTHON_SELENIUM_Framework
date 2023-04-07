import json


class JSON_scribe:

    def __init__(self, json_file):
        self.json_file = json_file

    def obj_from_json(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    def set_json_obj(self, chiave_modifica, nuovo_valore):
        # legge il contenuto del file JSON
        with open(self.json_file, 'r') as file:
            dati = json.load(file)

        # modifica il valore della chiave specificata
        dati[chiave_modifica] = nuovo_valore

        # scrive le modifiche sul file JSON
        with open(self.json_file, 'w') as file:
            json.dump(dati, file, indent=4)

