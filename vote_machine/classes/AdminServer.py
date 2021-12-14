from vote_machine.classes.Huissier import Huissier


class AdminServer:

    NB_HUISSIER = 10

    def __init__(self):
        self.huissiers = []
        for i in range(10):
            h = Huissier(i)
            self.huissiers.append(h)

    def print_huissiers(self):
        for h in self.huissiers:
            print(h)

    def print_voters(self):
        for h in self.huissiers:
            h.print_voters()