# coding: utf-8

import os
import algos


def cls():
    os.system('clear')


def print_req(mode, a="a", b="b", c="c", m="m"):
    cls()
    if mode == 1:
        _str = "PGCD({},{}) = {}\n\n".format(a, b, c)
    elif mode == 2:
        _str = "{} * x ≡ 1 mod {}\n\n".format(a, m)
    elif mode == 3:
        _str = "{}x + {} ≡ {} mod {}\n\n".format(a, b, c, m)
    print(_str)


def print_th_equs(equs, x="none"):
    cls()
    if len(equs) > 0:
        i = 1
        for eq in equs:
            if x == "none":
                _str = "Eq {} : {} mod {}".format(i, eq.get("a"), eq.get("m"))
                print(_str)
                i += 1
            else:
                _str = "{} = {} mod {}".format(x, eq.get("a"), eq.get("m"))
                print(_str)
        print("")
        if x != "none":
            print("\nx = ", x)


def print_th_req(equs, a="a", m="m"):
    print_th_equs(equs)
    _str = "Equation {} : {} mod {}\n\n".format(len(equs) + 1, a, m)
    print(_str)


def ask_eq(equs):
    print_th_req(equs)
    a = int(input("a ? "))
    print_th_req(equs, a)
    m = int(input("m ? "))
    equs.append({"a": a, "m": m})
    print_th_equs(equs)


def disp_pgcd():
    print_req(1)
    a = int(input("a ? "))
    print_req(1, a)
    b = int(input("b ? "))
    print_req(1, a, b, algos.euclide(a, b))
    input()


def disp_inv():
    print_req(2)
    a = int(input("a ? "))
    print_req(2, a)
    m = int(input("m ? "))
    inv = algos.inverse_mod(a, m)
    cls()
    _str = "{} * {} ≡ 1 mod {}\n\nL'inverse de {} est {} dans Z{}\n".format(a, inv, m, a, inv, m)
    input(_str)


def disp_solv():
    print_req(3)
    a = int(input("a ? "))
    print_req(3, a)
    b = int(input("b ? "))
    print_req(3, a, b)
    c = int(input("c ? "))
    print_req(3, a, b, c)
    m = int(input("m ? "))
    print_req(3, a, b, c, m)

    x = algos.solve(a, b, c, m)
    _str = "{} * {} + {} ≡ {} mod {}\nx = {}".format(a, x, b, c, m, x)
    print(_str)

    input()


def disp_th_ch():
    cls()
    _continue = True
    equs = []

    while _continue:
        while len(equs) < 2:
            ask_eq(equs)
        ltr = input("Ajouter une équation ? (y/n) ")
        if ltr == "y":
            ask_eq(equs)
        else:
            x = algos.theoremeChi(equs)
            print_th_equs(equs, x)
            _continue = False
    input()


if __name__ == '__main__':
    while 1:
        cls()
        menu = "MENU \n=====================\n1. PGCD\n2. Inverse\n3. Résolution\n4. Théorème chinois\n"
        choix = input(menu)
        if choix == "1":
            disp_pgcd()
        elif choix == "2":
            disp_inv()
        elif choix == "3":
            disp_solv()
        elif choix == "4":
            disp_th_ch()
        else:
            break
