import logging
from time import sleep

class SSHTunnel(object):

    def __init__(self, username, password, gateway, gateway_port, remote_host, remote_port, local_host, local_port):
        self.username = username
        self.password = password
        self.gateway = gateway
        self.gateway_port = int(gateway_port)
        self.remote_host = remote_host
        self.remote_port = int(remote_port)
        self.local_host = local_host
        self.local_port = int(local_port)

    def __call__(self, function, *args, **kwargs):

        def inner(*args, **kwargs):

            self.__logger()

            server = self.__get_server()

            self.__connect(server)

            while True:

                server.check_tunnels()

                if not server.is_active:
                    logging.info('Connection unavailable')
                    server.stop()
                    self.__connect(server)

                function(*args, **kwargs)

        return inner

    def __get_server(self):
        from sshtunnel import SSHTunnelForwarder

        server = SSHTunnelForwarder(
            ssh_address_or_host=(
                self.gateway,
                self.gateway_port
            ),
            ssh_username=self.username,
            ssh_password=self.password,
            remote_bind_address=(
                self.remote_host,
                self.remote_port
            ),
            local_bind_address=(
                self.local_host,
                self.local_port
            ),
            threaded=False,
            compression=True
        )

        return server

    def __logger(self):

        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(
                    'sshtunnel.log',
                    encoding='utf-8'
                ),
                logging.StreamHandler()
            ]
        )

    def __connect(self, server):

        while not server.is_active:
            try:
                logging.info('Starting server . . .')
                server.start()
                logging.info('SSH connection started')
            except:
                logging.error('SSH connection error')
                sleep(5)
                continue

            server.check_tunnels()
