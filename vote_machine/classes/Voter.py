class Voter:

    def __init__(self, nom, prenom, mail):
        self.nom = nom
        self.prenom = prenom
        self.mail = mail

    def __str__(self):
        str = f'Nom : {self.nom}\nPrenom : {self.prenom}\nMail : {self.mail}'
        return str