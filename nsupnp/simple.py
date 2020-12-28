import nsupnp.main
import socket
import time


class SimpleNsupnp:
    """
    A class to simplify the usage of the nsupnp class. It
    registers a single service in the default channel and
    handles the unregistration at disposal.

    Also gives a method to discover other nsupnp services
    ...

    Attributes
    ----------
    name : str
        name of the service
    version : str
        version of the service
    protocol : int
        the protocol of the service
    timeout : int
        the max timeout the service responds to

    Methods
    -------
    services():
        returns all found services

    """

    def __init__(self, name: str, version: str, protocol: str, timeout: str = '3'):
        self.client = nsupnp.main.nonStandardUniversalPlugAndPlay()

        local_address = str(socket.gethostbyname(socket.gethostname()))
        self.Service = (name, version, protocol, local_address, timeout)

        self.client.register(*self.Service)

        self.client.discover()

    def services(self):
        self.client.discover()
        time.sleep(float(self.Service[4]))
        return self.client.registeredOtherServices

    def __del__(self):
        self.client.unregister(*self.Service)
