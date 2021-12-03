from vote_machine.classes.AdminServer import AdminServer


class ServerFactory:
    __adminServerInstance = None
    __registerServerInstance = None
    __votingServerInstance = None
    __certificateServerInstance = None

    @staticmethod
    def get_admin_server_instance() -> AdminServer:
        if ServerFactory.__adminServerInstance is None:
            ServerFactory.__adminServerInstance = AdminServer()
        return ServerFactory.__adminServerInstance
