from vote_machine.algos.generator import generate_uuid
from vote_machine.classes.Huissier import Huissier
from vote_machine.classes.Question import Question


class AdminServer:

    def __init__(self):
        self.nb_huissier = 10
        self.huissiers = []
        self.questions = []
        for i in range(self.nb_huissier):
            h = Huissier(i)
            self.huissiers.append(h)
        self.init_questions()

    def init_questions(self):
        q = Question("Quel est le meilleur duo ?")
        choix = ["Remi Cogranne et Nicolas Burger", "Jordan et Pippen", "Superman et Batman", "Asterix et Obelix"]
        q.set_choix(choix)
        self.questions.append(q)

    def get_voters(self):
        self.give_uuid()
        voters = []
        for h in self.huissiers:
            voters += h.voters
        return voters

    def give_uuid(self):
        for h in self.huissiers:
            for v in h.voters:
                if v.uuid is None:
                    v.uuid = generate_uuid()
