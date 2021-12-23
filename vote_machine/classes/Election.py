import json

from vote_machine.classes.Question import Question
from vote_machine.json_encoder import JsonEncoder


class Election:

    def __init__(self, qs):
        self.questions = qs
        self.uuid = None
        self.public_key = None

    def __iter__(self):
        yield from {
            "uuid": self.uuid,
            "public_key": self.public_key,
            "questions": self.questions
        }.items()

    def __str__(self):
        return json.dumps(dict(self), cls=JsonEncoder)

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        return json.dumps(self.__dict__, cls=JsonEncoder)

if __name__ == '__main__':
    q = Question("Quel est le meilleur duo ?")
    choix = ["Remi Cogranne et Nicolas Burger", "Jordan et Pippen", "Superman et Batman", "Asterix et Obelix"]
    q.set_choix(choix)
    questions = [q]
    e = Election(questions)
    print(e.serialize())
