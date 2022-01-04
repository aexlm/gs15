# coding: utf-8
import multiprocessing.pool
import threading
import algos.generator
import os
from classes.ServerFactory import ServerFactory
from random import SystemRandom

from classes.Voter import Voter

generateur = SystemRandom()

NB_BITS = 512
NB_VOTANTS = 0
NB_DEPOUILLEURS = 0
sprime_512 = []
past_primes = []

_prime = 0
_generator = 0

def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
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
    # print("p de Zp = ", _prime, "\nGenerateur g =", _generator)
    admin = ServerFactory.get_admin_server_instance()
    admin.start_vote(ServerFactory.get_voting_server_instance(), ServerFactory.get_credentials_server_instance())
    vote_code = input("Entrez votre code de vote : ")
    while not admin.check_vote_code(vote_code):
        cls()
        vote_code = input("Mauvais code de vote, reessayez : ")
    cls()
    for question in admin.get_elec_questions():
        print(question, "\n")
        choix = input("Votre choix ? ")
        # Vote
        input("\nChoix pris ! N'oubliez pas de le valider !")
    input()


def register_voter():
    cls()
    n = input("Entrez votre nom : ")
    p = input("Entrez votre prenom : ")
    m = input("Entrez votre mail : ")

    huis_ind = generateur.randint(0, 9)
    huis = ServerFactory.get_admin_server_instance().huissiers[huis_ind]
    v = Voter(n,p,m)
    huis.add_voter(v)
    cls()
    print(f'Votant enregistre !\n{v}')
    input()


if __name__ == '__main__':
    search = threading.Thread(target=search, daemon=True).start()
    pool = multiprocessing.pool.ThreadPool(processes=1)  # https://tinyurl.com/y5syn7wb
    initialization = pool.apply_async(init)
    #os.system(python -m smtpd -c DebuggingServer -n localhost:1025)

    while 1:
        cls()
        menu = "->1<- Créer un vote\n->2<- Enregistrer un electeur\n->3<- Enregistrer un vote\n->4<_ Verifier un vote\n->5<- Proceder au depouillement\n"
        choix = int(input(menu))
        if choix == 1:
            #_prime, _generator = initialization.get()
            start_vote()
        elif choix == 2:
            register_voter()
