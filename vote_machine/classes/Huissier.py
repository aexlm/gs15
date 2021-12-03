from vote_machine.classes.Voter import Voter


class Huissier:

    def __init__(self, id):
        self.id = id
        self.voters = []

    def add_voter(self, voter):
        self.voters.append(voter)

    def print_voters(self):
        print(f'Huissier : {self.id}')
        for v in self.voters:
            print("   ", v)

    def __str__(self):
        str = f'Huissier {self.id}'
        return str