class Voter:

    def __init__(self, nom, prenom, mail):
        self.nom = nom.upper()
        self.prenom = prenom.title()
        self.mail = mail.lower()
        self.weight = 1
        self.uuid = None
        self.cred = None

    def __str__(self):
        str = f'   Uuid : {self.uuid}\n   Nom : {self.nom}\n   Prenom : {self.prenom}\n   Mail : {self.mail}'
        return str