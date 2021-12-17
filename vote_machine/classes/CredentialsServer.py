import random
import os, sys

p = os.path.abspath('..')
sys.path.insert(1, p)

from email_sender import sendmail


class CredentialsServer:

    def __init__(self):
        pass

    def gen_cred(self, uuid, admin_server):
        for v in admin_server.get_voters():
            if v.cred is None:
                v.cred = self.gen_private_c()
                self.mail(v)
                # gen pub with kdf

    def gen_private_c(self):
        c = ''
        base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        checksum = 0
        for i in range(14):
            c += random.choice(base58)
            checksum += base58.index(c[i])
        c += base58[(53 - checksum) % 53]
        return c

    def mail(self, voter):
        subject = "Vote - Votre mot de passe"
        msg = f'{voter.prenom} {voter.nom}, voici votre mot de passe : {voter.cred}'
        sendmail(voter.mail, subject, msg)


if __name__ == '__main__':
    cs = CredentialsServer()
    #cs.gen_private_c()
