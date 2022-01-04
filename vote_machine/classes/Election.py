class Election:

    def __init__(self, questions):
        self.questions = questions
        self.uuid = None
        self.public_key = None
        self.public_keys = [] #Revoir les données publiques de l'élection pour d'eventuelles questions
