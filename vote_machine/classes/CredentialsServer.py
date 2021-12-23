import random
from random import SystemRandom
import vote_machine.algos as algos
import vote_machine.values as values
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
        dk = algos.encryption.pbkdf1(private_c, uuid)
        s = int(dk, 16) % values.q
        return algos.maths.exponentation_rapide(values.g, s, values.p)

    def mail(self, voter, private_c):
        subject1 = "Vote - Votre code de vote"
        msg1 = f'{voter.prenom} {voter.nom}, voici votre code de vote : {voter.pubc}'
        email_sender.sendmail(voter.mail, subject1, msg1)
        subject2 = "Vote - Votre mot de passe"
        msg2 = f'{voter.prenom} {voter.nom}, voici votre mot de passe : {private_c}'
        email_sender.sendmail(voter.mail, subject2, msg2)


if __name__ == '__main__':
    cs = CredentialsServer()
    #cs.gen_private_c()
