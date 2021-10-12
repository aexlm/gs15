# coding: utf-8
import atexit
import math


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
    last = 0
    try:
        for p in pre:
            last = p
            for n in pre:
                if (n % p == 0) & (n != p):
                    pre.remove(n)
    finally:
        return last


if __name__ == '__main__':
    print(crible_erathostene(12324))
