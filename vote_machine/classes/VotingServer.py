import random

from vote_machine.classes.Election import Election
import os, sys

p = os.path.abspath('..')
sys.path.insert(1, p)

from email_sender import sendmail


class VotingServer:

    def __init__(self):
        self.voters = []
        self.questions = []
        self.election = None

    def create_election(self, admin_server, credentials_server):
        self.election = Election(self.questions)
        uuid = ''
        for _ in range(14):
            uuid += random.choice('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
        self.election.uuid = uuid
        self.send_mails(admin_server, uuid)
        credentials_server.gen_cred(uuid, admin_server)
        self.send_election_data(admin_server)

    def send_mails(self, admin_server, uuid):
        for voter in admin_server.get_voters():
            subject = "Vote - Identifiant de l'election"
            msg = f'{voter.prenom} {voter.nom}, voici l\'identifiant de l\'election : {uuid}'
            sendmail(voter.mail, subject, msg)

    def send_election_data(self, admin_server):
        if admin_server.election is None:
            admin_server.election = self.election
