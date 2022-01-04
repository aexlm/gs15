from classes.AdminServer import AdminServer
from classes.CredentialsServer import CredentialsServer
from classes.VotingServer import VotingServer


class ServerFactory:
    __adminServerInstance = None
    __credentialsServerInstance = None
    __votingServerInstance = None

    @staticmethod
    def get_admin_server_instance() -> AdminServer:
        if ServerFactory.__adminServerInstance is None:
            ServerFactory.__adminServerInstance = AdminServer()
        return ServerFactory.__adminServerInstance

    @staticmethod
    def get_credentials_server_instance() -> CredentialsServer:
        if ServerFactory.__credentialsServerInstance is None:
            ServerFactory.__credentialsServerInstance = CredentialsServer()
        return ServerFactory.__credentialsServerInstance

    @staticmethod
    def get_voting_server_instance() -> VotingServer:
        if ServerFactory.__votingServerInstance is None:
            ServerFactory.__votingServerInstance = VotingServer()
        return ServerFactory.__votingServerInstance
