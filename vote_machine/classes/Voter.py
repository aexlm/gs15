class Voter:

    def __init__(self, nom, prenom, mail, weight=1):
        self.nom = nom.upper()
        self.prenom = prenom.title()
        self.mail = mail.lower()
        self.weight = weight
        self.uuid = None
        self.pubc = None
        self.__cred = None

    def __str__(self):
        str = f'   Uuid : {self.uuid}\n   Nom : {self.nom}\n   Prenom : {self.prenom}\n   Mail : {self.mail}'
        return str

    def set_cred(self, pub, c):
        # Check certif
        self.pubc = pub
        self.__cred = c
