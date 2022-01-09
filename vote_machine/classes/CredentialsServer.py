import random
from random import SystemRandom
import vote_machine.algos as algos
import vote_machine.values as values
import vote_machine.algos.sha256 as sha256
from vote_machine.algos.encryption import private_2_pub
from vote_machine import email_sender


class CredentialsServer:

    gen = random.SystemRandom()

    def __init__(self):
        self.l_pub = []

    def gen_cred(self, uuid, voters):
        for v in voters:
            if v.pubc is None:
                private_c = self.gen_private_c()
                public_c = self.gen_pub_c(private_c, uuid)
                v.set_cred(public_c, private_c)
                self.mail(v, private_c)
                self.l_pub.append({"pub_k": public_c, "weight": v.weight})
        random.shuffle(self.l_pub)
        return self.l_pub

    def gen_private_c(self):
        c = ''
        base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        checksum = 0
        for i in range(14):
            c += CredentialsServer.gen.choice(base58)
            checksum += base58.index(c[i])
        c += base58[(53 - checksum) % 53]
        return c

    def gen_pub_c(self, private_c, uuid):
        return private_2_pub(private_c, uuid)          # La valeur numérique en tant que big_int est stocké pour Pub(cn)

    def mail(self, voter, private_c):
        subject1 = "Vote - Votre code de vote"
        sha_pubc = sha256.hash256(str(voter.pubc)).hex()
        msg1 = f'{voter.prenom} {voter.nom}, voici votre code de vote : {sha_pubc}' # Mais cette valeur est hashée pour l'envoyer au votant
        email_sender.sendmail(voter.mail, subject1, msg1)
        subject2 = "Vote - Votre mot de passe"
        msg2 = f'{voter.prenom} {voter.nom}, voici votre mot de passe : {private_c}'
        email_sender.sendmail(voter.mail, subject2, msg2)


if __name__ == '__main__':
    cs = CredentialsServer()
    pub_c = str(cs.gen_pub_c("pyvdwxNrGhm8mPh", "oiokjnj09"))
    print(pub_c)
    h_pubc = sha256.hash256(pub_c).hex()
    print(h_pubc)
