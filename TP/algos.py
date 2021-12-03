# coding: utf-8
import math
import random
from random import SystemRandom


def euclide(a, b):
    pgcd = 0
    while a % b != 0:
        pgcd = a % b
        a = b
        b = pgcd
    return pgcd


def euclide_et(a, b):
    _a = a
    _b = b

    _x = 1
    x = 0
    x_ = math.floor(_a/_b) * x + _x

    _y = 0
    y = 1
    y_ = math.floor(_a/_b) * y + _y

    i = 1
    pgcd = 0

    while _a % _b != 0:
        pgcd = _a % _b
        _a = _b
        _b = pgcd

        _x = x
        x = x_
        x_ = math.floor(_a/_b) * x + _x

        _y = y
        y = y_
        y_ = math.floor(_a/_b) * y + _y

        i += 1

    coef_a = math.pow(-1, i) * x * a
    coef_b = math.pow(-1, i + 1) * y * b
    if (coef_a + coef_b) != pgcd:
        print("Euclide etendu a eu un probleme")
        return
    return {"x": coef_a / a, "y": coef_b / b}


def inverse_mod(a, mod):
    return int(euclide_et(a, mod).get("x") % mod)


def expo(a, exp, mod):
    _a = a
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * _a) % mod
        exp = math.floor(exp/2)
        _a = (_a * _a) % mod
    return result


def euler(nb):
    p = 0
    d = 2
    phi = 1

    while nb % d == 0:
        p += 1
        quot = math.floor(nb/d)
        nb = quot
    if p != 0:
        phi = int(phi * math.pow(d, p-1) * (d - 1))
        p = 0

    d = 3
    while (d <= nb):
        while nb % d == 0:
            p += 1
            quot = math.floor(nb/d)
            nb = quot
        if p != 0:
            phi = int(phi * math.pow(d, p-1) * (d - 1))
            p = 0
        d += 2

    phi -= 1
    return phi


def solve(a, c, y, mod):
    _y = (y - c) % mod
    phi = euler(mod)
    x = expo(a, phi, mod)
    x = (x * _y) % mod
    return x


def theoremeChi(equs):
    ms = []
    as_ = []
    i = 0
    resultat = 0
    for eq in equs:
        ms.append(eq.get("m"))
        as_.append(eq.get("a"))

    while i+1 < len(ms):
        if ms[i] <= 2 | ms[i+1] <= 2 | euclide(ms[i], ms[i+1]) != 1:
            print("Les valeurs rentrees ne sont pas valides pour le theoreme")
            return
        i += 1

    M = 1
    for m in ms:
        M = M * m

    for eq in equs:
        Mk = int(M / eq.get("m"))
        yk = inverse_mod(Mk, eq.get("m"))
        resultat += eq.get("a") * Mk * yk

    return int(resultat % M)


def crible_erathostene(lim):
    pre = [p for p in range(2, lim+1) if (p % 2 != 0)]
    pre.append(2)
    try:
        for p in pre:
            for n in pre:
                if (n % p == 0) & (n != p):
                    pre.remove(n)
    finally:
        pre.sort()
        return pre


def prim_fermat(n):
    a = random.randint(0, n-1)
    print("Pour a = ", a)
    if expo(a, n-1, n) == 1:
        return True
    else:
        return False


def coefs_s_d(n):
    s, d = 0, n-1
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d


def miller_temoin(n, a, d, s):
    x = expo(a, d, n)
    if (x == 1) | (x == n-1):
        return False
    for _ in range(s-1):
        x = expo(x, 2, n)
        if x == n-1:
            return False
    return True


def miller_rabin(n, k=5):
    if (n == 2) | (n == 3):
        return True
    if n % 2 == 0:
        return False
    s, d = coefs_s_d(n)
    for _ in range(k):
        a = random.randint(2, n-2)
        if miller_temoin(n, a, d, s):
            return False
    return True


def bigint_gen(n):
    cryptogen = SystemRandom()
    x = 2
    while x % 2 == 0:
        x = cryptogen.randint(pow(2, n-1), pow(2, n) - 1)
    return x


def big_prem_gen(n, k=5):
    x = bigint_gen(n)
    while not miller_rabin(x, k):
        x = bigint_gen(n)
    return x


# Fonction de génération d'un nombre premier fort
def strong_prem_gen(n, lim=5):
    """
    :param n: le nombre de bits du nombre à générer
    :param lim: la limite du nombre q premier tel que n-1/q est premier
    :return: un nombre fortement premier sur n bits et ses diviseurs pour nb-1
    """

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


def find_gen(p, divs):
    """
    :param p: l'ordre du corps Zp dans lequel on travaille (p est fortement premier)
    :param divs: les diviseurs de p-1
    :return: un élément générateur du corps Zp
    """

    cryptogen = SystemRandom()

    _continue = True
    a = cryptogen.randint(2, p-1)

    while _continue:
        for d in divs:
            if expo(a, d, p) != 1:
                _continue = False
            else:
                a = cryptogen.randint(2, p-1)

    return a


def init_gen(n = 64):
    """
    Fonction qui génère un nombre premier fort p de n bits ainsi et un élément générateur de Zp a
    :param n: le nombre de bits de p
    :return: p, a
    """

    p, divs = strong_prem_gen(n)
    a = find_gen(p, divs)
    return p, a


if __name__ == '__main__':
    # print(crible_erathostene(23983))
    # print(prim_fermat(23981))

    # print(miller_rabin(23981, 5))
    #a = bigint_gen(64)
    #print("int :", a, " ; bin :", bin(a), " ; taille :", len(bin(a)) - 2)

    #p, divs = strong_prem_gen(16, 2)
    #print(p, divs)
    #print(find_gen(p, divs))

    print(init_gen(16))