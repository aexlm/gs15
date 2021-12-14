# coding: utf-8
import multiprocessing.pool
import threading
import algos.generator
import os
from classes.ServerFactory import ServerFactory
from random import SystemRandom

from vote_machine.classes.Voter import Voter

generateur = SystemRandom()

NB_BITS = 512
NB_VOTANTS = 0
NB_DEPOUILLEURS = 0
sprime_512 = []
past_primes = []

_prime = 0
_generator = 0

def cls():
    os.system('clear')


def search():
    while 1:
        while len(sprime_512) < 2:
            p = algos.generator.strong_prem_gen(NB_BITS)
            if p not in sprime_512 and p not in past_primes:
                sprime_512.append(p)


def init():
    loop = True
    while loop:
        if len(sprime_512) > 0:
            p = sprime_512.pop(0)
            past_primes.append(past_primes)
            g = algos.generator.find_gen(p, [2, p/2])
            loop = False

    return p,g


def start_vote():
    cls()
    print("p de Zp = ", _prime, "\nGenerateur g =", _generator)
    input()


def register_voter():
    cls()
    n = input("Entrez votre nom : ")
    p = input("Entrez votre prenom : ")
    m = input("Entrez votre mail : ")

    huis_ind = generateur.randint(0,9)
    huis = ServerFactory.get_admin_server_instance().huissiers[huis_ind]
    huis.add_voter(Voter(n,p,m))
    input()


if __name__ == '__main__':
    search = threading.Thread(target=search, daemon=True).start()
    pool = multiprocessing.pool.ThreadPool(processes=1)  # https://tinyurl.com/y5syn7wb
    initialization = pool.apply_async(init)


    while 1:
        cls()
        menu = "->1<- Créer un vote\n->2<- Enregistrer un electeur\n->3<- Enregistrer un vote\n->4<_ Verifier un vote\n->5<- Proceder au depouillement\n"
        choix = int(input(menu))
        if choix == 1:
            _prime, _generator = initialization.get()
            start_vote()
        elif choix == 2:
            register_voter()
