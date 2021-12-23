import json


class Question:

    def __init__(self, enonce):
        self.enonce = enonce
        self.choix = []

    def __iter__(self):
        yield from {
            "enonce": self.enonce,
            "choix": self.choix
        }.items()

    def __str__(self):
        return json.dumps(dict(self))

    def __repr__(self):
        return self.__str__()

    def set_choix(self, choix):
        i = 1
        for c in choix:
            self.choix.append({"nb": i, "c": c})
            i += 1

    def get_nbs(self):
        nbs = []
        for c in self.choix:
            nbs.append(c['nb'])
        return nbs

    def print_self(self):
        str = self.enonce
        for c in self.choix:
            str += f'\n   - {c["nb"]} : {c["c"]}'
        return str


if __name__ == '__main__':
    q = Question("Qui est le plus beau ?")
    choix = ["Axel", "Michael", "Gregoire"]
    q.set_choix(choix)
    print(q.get_nbs())