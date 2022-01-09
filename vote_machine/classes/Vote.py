import json

from vote_machine.algos.encryption import private_2_pub


class Vote:

    def __init__(self, credential):
        self.reponse = []
        self.credential = credential
        self.election_hash = None
        self.election_uuid = None
        self.valide = False
        # self.signature = {"hash": None, "proof": {"challenge": None, "response": None}}

    def serialize(self):
        return json.dumps({'reponse': self.reponse,
                           'credential': self.credential,
                           'election_hash': self.election_hash,
                           'election_uuid': self.election_uuid})

    def sign_vote(self, c):
        """
        gen = SystemRandom()

        self.signature["hash"] = sha256.hash256(self.serialize()).hex()

        s = int(pbkdf1(c, self.election_uuid), 16) % values.q
        w = gen.randint(1, values.q)
        A = exponentation_rapide(values.g, w, values.q)

        self.signature["proof"]["challenge"] = int(sha256.hash256(str(s) + self.signature["hash"] + str(A)).hex(),
                                                   16) % values.q
        self.signature["proof"]["response"] = (w - s * self.signature["proof"]["challenge"]) % values.q


        Après de nombreuses tentatives, je n'ai pas trouvé de solutions pour le Zero-knowledge proof
        J'ai bien compris le principe, mais je n'ai pas trouvé la solution techniques
        En effet, l'exponentation de g à la puissance resp ne donne pas un résultat convenable
        En testant avec de plus petites valeurs, j'ai trouvé que la formule fonctionnait si l'on n'appliquait pas le mod
        sur resp
        En revanche, ce n'est pas possible ici car la valeur de g est trop grande, donc tant pis, je me rends...
        
        
        term1 = exponentation_rapide(values.g, self.signature["proof"]["response"], values.q)
        #term1bis = (exponentation_rapide(values.g, w, values.q) * float(values.g**(-s * self.signature["proof"]["challenge"]))) % values.q
        term2 = exponentation_rapide(int(self.credential), self.signature["proof"]["challenge"], values.q)
        term2bis = exponentation_rapide(values.g, s * self.signature["proof"]["challenge"], values.q)
        Auno = term1 * term2 % values.q
        #Abis = (values.g**self.signature["proof"]["response"] * int(self.credential)**self.signature["proof"]["challenge"]) % values.q


        A = (exponentation_rapide(values.g, self.signature["proof"]["response"], values.q) *
             exponentation_rapide(int(self.credential), self.signature["proof"]["challenge"], values.q)) % values.q
        """

        if private_2_pub(c, self.election_uuid) == int(self.credential):
            self.valide = True
            return True
        else:
            return False


if __name__ == '__main__':
    vote = Vote(1243)
    print(vote.serialize())
