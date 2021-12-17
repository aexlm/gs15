class Question:

    def __init__(self, enonce):
        self.enonce = enonce
        self.choix = []

    def set_choix(self, choix):
        i = 1
        for c in choix:
            self.choix.append({"nb": i, "c": c})
            i += 1

    def prtn(self):
        print(self)

    def __str__(self):
        str = self.enonce
        for c in self.choix:
            str += f'\n   - {c["nb"]} : {c["c"]}'
        return str

if __name__ == '__main__':
    q = Question("Qui est le plus beau ?")
    choix = ["Axel", "Michael", "Gregoire"]
    q.set_choix(choix)
    print(q)