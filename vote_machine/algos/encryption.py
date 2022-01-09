import hashlib, base64
import vote_machine.algos.sha256 as sha256
from vote_machine.algos.maths import exponentation_rapide
import vote_machine.values as values
from random import SystemRandom


def pbkdf1(password, salt, c=1000, dkLen = 16):
    h = hashlib.md5((password + salt).encode())
    for _ in range(c-1):
        h = hashlib.md5(h.hexdigest().encode())
    h = h.hexdigest()
    dk = ''
    for i in range(dkLen):
        dk += h[i]
    return dk


def private_2_pub(private_c, uuid):
    dk = pbkdf1(private_c, uuid)
    s = int(dk, 16) % values.q
    return exponentation_rapide(values.g, s, values.q)


def hjson(election):
    election_sha = sha256.hash256(str(election))
    election_b64 = base64.b64encode(election_sha)
    return election_b64.decode("utf-8")


if __name__ == '__main__':
    #print(bin(int(sha256.hash256("bonjour").hex(), 16)))
    passw = 'amoO3kF0kNCS9ml'
    salt = 'paRi917bQl0kQj'
    dk = pbkdf1(passw, salt)
    print(dk)
    print(int(dk, 16))
    print(len(bin(int(dk,16))) - 2)