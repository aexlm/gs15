import random
import os, sys
import algos.generator

from classes import email_sender


p = os.path.abspath('..')
sys.path.insert(1, p)


class CredentialsServer:

    def __init__(self):
        self.l_pub = []

    def gen_cred(self, uuid, admin_server):
        for v in admin_server.get_voters():
            if v.pubc is None:
                private_c = self.gen_private_c()
                public_c = self.gen_pub_c(private_c, uuid)
                v.set_cred(public_c, private_c)
                self.mail(v, private_c)
                self.l_pub.append(public_c)
                # gen pub with kdf
        random.shuffle(self.l_pub)
        return self.l_pub

    def gen_private_c(self):
        c = ''
        base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        checksum = 0
        for i in range(14):
            c += random.choice(base58)
            checksum += base58.index(c[i])
        c += base58[(53 - checksum) % 53]
        return c

    def gen_pub_c(self, private_c, uuid):
        return algos.generator.pbkdf1(private_c, uuid) 
        # N'est-ce pas plutot s=algos.generator.pbkdf1(private_c, uuid)  
        # Et Pub_c = g**s % p ????????

    def mail(self, voter, private_c):
        subject1 = "Vote - Votre code de vote"
        msg1 = f'{voter.prenom} {voter.nom}, voici votre code de vote : {voter.pubc}'
        email_sender.sendmail(voter.mail, subject1, msg1)
        subject2 = "Vote - Votre mot de passe"
        msg2 = f'{voter.prenom} {voter.nom}, voici votre mot de passe : {private_c}'
        email_sender.sendmail(voter.mail, subject2, msg2)


if __name__ == '__main__':
    cs = CredentialsServer()
    print(cs.gen_private_c())
