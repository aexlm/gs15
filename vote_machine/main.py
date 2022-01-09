# coding: utf-8
import multiprocessing.pool
import threading
import vote_machine.algos as algos
import os
from classes.ServerFactory import ServerFactory
from random import SystemRandom

from vote_machine.classes.Vote import Vote
from vote_machine.classes.Voter import Voter

generateur = SystemRandom()

NB_BITS = 512
NB_DEPOUILLEURS = 0
sprime_512 = []
past_primes = []

_prime = 0
_generator = 0

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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
    admin = ServerFactory.get_admin_server_instance()
    if len(admin.get_voters()) == 0:
        input("Vous n'avez pas ajouté d'électeurs.")
        return

    voting = ServerFactory.get_voting_server_instance(admin)

    return voting


def register_voter():
    cls()
    n = input("Entrez votre nom : ")
    p = input("Entrez votre prenom : ")
    m = input("Entrez votre mail : ")

    huis_ind = generateur.randint(0, 9)
    huis = ServerFactory.get_admin_server_instance().huissiers[huis_ind]
    v = Voter(n, p, m)
    huis.add_voter(v)
    cls()
    print(f'Votant enregistré !\n{v}')
    input()


def register_vote(voting):
    cls()
    if voting.election is None:
        voting.create_election(ServerFactory.get_credentials_server_instance())

    vote_code = input("Entrez votre code de vote : ")
    invalid = True
    while invalid:
        pub_c = voting.check_vote_code(vote_code)
        if pub_c is not None:
            invalid = False
            break
        cls()
        vote_code = input("Mauvais code de vote, reessayez : ")

    ballot = Vote(pub_c)
    for question in voting.election.questions:
        cls()
        print(question.print_self(), "\n")
        choice = int(input("Votre choix ? "))
        while choice not in question.get_nbs():
            choice = int(input("\nCe choix n'est pas proposé. Votre choix ? "))
        ballot.reponse.append({"q_uuid": question.uuid, "choix": choice})

    ballot = voting.complete_ballot(ballot)
    input("\nChoix enregistré ! N'oubliez pas de le valider !")
    cls()

    valid = False
    for i in range(3):
        cls()
        c = input(f"Entrez votre mot de passe ({3-i} tentatives restantes) : ")
        valid = ballot.sign_vote(c)
        if valid:
            voting.add_vote(ballot)
            print("Vote déposé dans l'urne, merci !")
            break
    if not valid:
        print("Tentatives épuisées, votre vote a été rejeté.")
    input()


def check_vote(voting):
    cls()
    c = input("Entrez votre mot de passe : ")
    cls()
    infos = voting.find_votes(c)
    if infos is not None:
        print(f'Nom : {infos["nom"]}\nPrénom : {infos["prenom"]}')
        for q in infos["questions"]:
            print(f'   Q_Uuid : {q["uuid"]}\n   Choix : {q["choix"]}')
        print(f'Valide ? {infos["valide"]}')
        input()
    else:
        input("Aucune corresponsance.")


def count_votes(voting):
    cls()
    for question in voting.election.questions:
        res = voting.count_votes(question)
        print(question.enonce)
        for choix in question.choix:
            print(f'   {choix["nb"]}- {choix["c"]} : {res[choix["nb"]]} voix')
        input()


if __name__ == '__main__':
    """
    Afin de lancer le serveur smtp de debug de python (utilisé pour envoyer les identifiants), il suffit de renter une 
    commande dans le terminal : python -m smtpd -c DebuggingServer -n localhost:1025
    Ensuite, les mails s'afficheront sur ce terminal et donneront les codes de vote ainsi que les mots de passe
    """
    search = threading.Thread(target=search, daemon=True).start()
    pool = multiprocessing.pool.ThreadPool(processes=1)  # https://tinyurl.com/y5syn7wb
    initialization = pool.apply_async(init)
    voting = None

    while 1:
        cls()
        menu = "->1<- Créer un vote\n->2<- Enregistrer un electeur\n->3<- Enregistrer un vote\n->4<- Vérifier un vote\n->5<- Procéder au dépouillement\n"
        choix = int(input(menu))
        if choix == 1:
            #_prime, _generator = initialization.get()
            voting = start_vote()
        elif choix == 2:
            register_voter()
        elif choix == 3:
            if voting is not None:
                register_vote(voting)
        elif choix == 4:
            if voting is not None:
                check_vote(voting)
        elif choix == 5:
            if voting is not None:
                count_votes(voting)