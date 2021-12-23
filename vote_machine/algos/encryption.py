import hashlib


def pbkdf1(password, salt, c=1000, dkLen = 16):
    h = hashlib.md5((password + salt).encode())
    for _ in range(c-1):
        h = hashlib.md5(h.hexdigest().encode())
    h = h.hexdigest()
    dk = ''
    for i in range(dkLen):
        dk += h[i]
    return dk

"""
def pbkdf2(password, salt, c=1000, dkLen = 16):
    hLen = 32
    if dkLen > (2**32 - 1) * hLen:
        return
    l = dkLen // hLen
    r = dkLen - (l - 1) * hLen
    dk = ''
    #for t in l:


def prf(password, salt, c, i):
    t = ''
    #for _ in c:"""



def hjson(data):
    pass


if __name__ == '__main__':
    #print(bin(int(sha256.hash256("bonjour").hex(), 16)))
    passw = 'amoO3kF0kNCS9ml'
    salt = 'paRi917bQl0kQj'
    dk = pbkdf1(passw, salt)
    print(dk)
    print(int(dk, 16))
    print(len(bin(int(dk,16))) - 2)