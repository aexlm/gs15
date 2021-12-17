import random

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
        self.election = None

    def init_questions(self):
        q = Question("Quel est le meilleur duo ?")
        choix = ["Remi Cogranne et Nicolas Burger", "Jordan et Pippen", "Superman et Batman", "Asterix et Obelix"]
        q.set_choix(choix)
        self.questions.append(q)

    def get_election_uuid(self):
        return self.election.uuid

    def get_elec_questions(self):
        return self.election.questions

    def print_huissiers(self):
        for h in self.huissiers:
            print(h)

    def print_voters(self):
        for h in self.huissiers:
            h.print_voters()

    def get_voters(self):
        voters = []
        for h in self.huissiers:
            voters += h.voters
        return voters

    def generate_uuid(self):
        uuid = ''
        for _ in range(14):
            uuid += random.choice('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
        return uuid

    def give_uuid(self):
        for h in self.huissiers:
            for v in h.voters:
                if v.uuid is None:
                    v.uuid = self.generate_uuid()

    def send_to_voting(self, voting_server, credentials_server):
        # if certif ok :
        voting_server.voters.append(self.get_voters())
        voting_server.questions += self.questions
        voting_server.create_election(self, credentials_server)

    def start_vote(self, voting_server, credentials_server):
        if self.election is None:
            self.init_questions()
            self.give_uuid()
            self.send_to_voting(voting_server, credentials_server)
