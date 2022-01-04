#import vote_machine.algos.maths as maths
import hashlib
from random import SystemRandom
from algos import maths as maths

generateur = SystemRandom() # Génere de manière plus sécurisée


# Fonction du Crible d'Erathostene
def crible_erathostene(limite):
    """
    :param limite: La limite jusqu'à laquelle il faut trouver les nombres premiers
    :return: la liste des nombres premiers de 2 à limite
    """

    pre = [p for p in range(2, limite+1) if (p % 2 != 0)]
    pre.append(2)
    try:
        for p in pre:
            for n in pre:
                if (n % p == 0) & (n != p):
                    pre.remove(n)
    finally:
        pre.sort()
        return pre


def coefs_s_d(n):
    s, d = 0, n-1
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d


def miller_temoin(n, a, d, s):
    x = pow(a, d, n)
    if (x == 1) | (x == n-1):
        return False
    for _ in range(s-1):
        x = pow(x, 2, n)
        if x == n-1:
            return False
    return True


def miller_rabin(n, k=20):
    """
    :param n: le nombre dont on veut savoir s'il est premier
    :param k: le nombre d'itérations à réaliser, donne le niveau de précision (20 par défault)
    :return: True si le nombre est premier, False autrement
    """
    # Tests basiques pour éviter les échecs dans le cas d'un n trop petit
    if (n == 2) | (n == 3):
        return True
    if n % 2 == 0:  # n-1 sera forcément pair, utile pour les coefficients
        return False

    # Génération des coefficients statiques utilisés pour le témoin
    s, d = coefs_s_d(n)

    # Répétition du test pour k itérations
    for _ in range(k):
        a = generateur.randint(2, n-2)
        if miller_temoin(n, a, d, s):
            return False
    return True


def bigint_gen(n):
    x = 2
    while x % 2 == 0:
        x = generateur.randint(pow(2, n-1), pow(2, n) - 1)
    return x


def big_prem_gen(n):
    x = bigint_gen(n)
    while not miller_rabin(x):
        x = bigint_gen(n)
    return x


def strong_prem_gen(n):
    """
    :param n: le nombre de bits du nombre à générer
    :return: un nombre fortement premier sur n bits et ses diviseurs pour nb-1
    """

    _continue = True
    while _continue:
        nb = big_prem_gen(n)
        if miller_rabin((nb - 1) // 2):
            _continue = False

    return nb


"""
# Fonction de génération d'un nombre premier fort en utilisant le crible
# Par simplicité et pour des raisons de performance, il est plus judicieux de faire simplement le test avec n-1/2
def strong_prem_gen(n, lim=3):
    :param n: le nombre de bits du nombre à générer
    :param lim: la limite du nombre q premier tel que n-1/q est premier
    :return: un nombre fortement premier sur n bits et ses diviseurs pour nb-1

    liste = crible_erathostene(lim)

    _continue = True
    while _continue:
        nb = big_prem_gen(n)
        for p in liste:
            if (nb - 1) % p == 0 and miller_rabin((nb - 1) // p):
                divs = [p, (nb - 1) // p]
                _continue = False
                break

    return nb, divs
"""


def find_gen(p, divs):
    """
    :param p: l'ordre du corps Zp dans lequel on travaille (p est fortement premier)
    :param divs: les diviseurs de p-1
    :return: un élément générateur du corps Zp
    """

    _continue = True
    a = generateur.randint(2, p-1)

    while _continue:
        for d in divs:
            if maths.exponentation_rapide(a, d, p) != 1:
                _continue = False
            else:
                a = generateur.randint(2, p-1)

    return a


def el_gamal_key_generation(sprime, generator):
    """
    Fonction qui va génerer notre couple de clé public/privé sécurisée par le problème du logarithme discret

    :param sprime: Nombre fortement premier de 512 bits par défaut
    :param generator: élément générateur de l'ensemble Zp*
    :return: Ephemeral public key, private key
    """

    a = generateur.randint(2, sprime-2)
    epk = maths.exponentation_rapide(generator, a, sprime) # Ephemeral Public Key, change pour chaque signature

    return epk, a

def init_gen(n = 256):
    """
    Fonction qui génère un nombre premier fort p de n bits ainsi et un élément générateur de Zp a
    :param n: le nombre de bits de p
    :return: p, a
    """

    p = strong_prem_gen(n)
    divs = [2, p/2]
    a = find_gen(p, divs)
    return p, a


def pbkdf1(password, salt, c=1000, dkLen = 15):
    h = hashlib.md5((password + salt).encode())
    for _ in range(c-1):
        h = hashlib.md5(h.hexdigest().encode())
    h = h.hexdigest()
    dk = ''
    for i in range(dkLen):
        dk += h[i]
    return dk


if __name__ == '__main__':
    passw = 'amoO3kF0kNCS9ml'
    salt = 'paRi917bQl0kQj'
    dk = pbkdf1(passw, salt)
    print(dk)