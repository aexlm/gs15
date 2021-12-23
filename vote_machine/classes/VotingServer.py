import random
from vote_machine.algos.generator import generate_uuid
from vote_machine.classes.Election import Election
from vote_machine import email_sender


class VotingServer:

    def __init__(self, admin_server):
        self.admin_server = self.check_admin_serv(admin_server)
        self.voters = self.admin_server.get_voters()
        self.questions = self.admin_server.questions
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
            pub_ks.append(el['pub_k'])
        return vote_code in pub_ks
