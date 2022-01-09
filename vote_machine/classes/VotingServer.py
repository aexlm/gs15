import random
from vote_machine.algos.generator import generate_uuid
from vote_machine.classes.Election import Election
from vote_machine import email_sender
import vote_machine.algos.sha256 as sha256
from vote_machine.classes.Vote import Vote
from vote_machine.algos.encryption import hjson
from vote_machine.algos.encryption import private_2_pub


class VotingServer:

    def __init__(self, admin_server):
        self.admin_server = self.check_admin_serv(admin_server)
        self.voters = self.admin_server.get_voters()
        self.questions = self.admin_server.questions
        self.votes = []
        self.election = None
        self.l_pub = []

    def check_admin_serv(self, admin_serv):
        # if admin trusted
        return admin_serv

    def create_election(self, credentials_server):
        self.election = Election(self.questions)
        self.election.uuid = generate_uuid()
        # self.send_mails(admin_server, uuid)
        self.l_pub += credentials_server.gen_cred(self.election.uuid, self.voters)

    def send_mails(self, admin_server, uuid):
        for voter in admin_server.get_voters():
            subject = "Vote - Identifiant de l'election"
            msg = f'{voter.prenom} {voter.nom}, voici l\'identifiant de l\'election : {uuid}'
            email_sender.sendmail(voter.mail, subject, msg)

    def send_election_data(self, admin_server):
        if admin_server.election is None:
            admin_server.election = self.election

    def check_vote_code(self, vote_code):
        pub_ks = []
        for el in self.l_pub:
            pub_ks.append(str(el['pub_k']))
        for k in pub_ks:
            if sha256.hash256(k).hex() == vote_code:
                return k
        return None

    def complete_ballot(self, vote):
        vote.election_uuid = self.election.uuid
        vote.election_hash = hjson(self.election)
        return vote

    def add_vote(self, vote):
        self.votes.append(vote)

    def find_votes(self, c):
        pub_c = private_2_pub(c, self.election.uuid)
        res = {"nom": None, "prenom": None, "questions": [], "valide": None}
        for vote in self.votes:
            if vote.credential == str(pub_c):
                for a in vote.reponse:
                    res["questions"].append({"uuid": a["q_uuid"], "choix": a['choix']})
                res["valide"] = vote.valide
        for el in self.voters:
            if el.pubc == pub_c:
                res["nom"] = el.nom
                res["prenom"] = el.prenom
        if res["nom"] is None or res["prenom"] is None or res["valide"] is None:
            return None
        else:
            return res

    def count_votes(self, question):
        resultats = {}
        for n in question.get_nbs():
            resultats.update({n: 0})

        for v in self.votes:
            if v.valide and v.election_uuid == self.election.uuid:
                for ans in v.reponse:
                    if ans["q_uuid"] == question.uuid:
                        resultats[ans["choix"]] += 1

        return resultats

