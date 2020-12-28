import socket
import struct
import threading
import time

import random


class Service:
    def __init__(self, name, version, protocol, timeout, address):
        self.name = name
        self.version = version
        self.protocol = protocol
        self.timeout = timeout
        self.address = address
        self.registrationTime = time.time()


class udpClient:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: bytes):
        self.sock.sendto(message, (self.ip, self.port))


class udpServer:
    def __init__(self, ip: str, port: int, callback: object, autoStart: bool = True):
        self.port = port
        self.ip = ip
        self.callback = callback
        self.killed = False

        # "inspired" by https://github.com/MoshiBin/ssdpy/blob/master/ssdpy/server.py

        # What I think it does:
        # This defines a normal socket in ip4 space and defines that udp should be used.
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Magic Part xD
        # I think it defines register as a listener to 239.255.255.250
        mreq = socket.inet_aton(self.ip)
        mreq += struct.pack(b"@I", socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        # binds to 0.0.0.0
        self.sock.bind(('0.0.0.0', self.port))

        self.workThread = threading.Thread(target=self.recieveLoop, args=())
        self.workThread.daemon = True

        if autoStart:
            self.start()

    def recieveLoop(self):
        while not self.killed:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.callback(data, addr)

    def start(self):
        self.killed = False
        self.workThread.start()

    def stop(self):
        self.killed = True


class nonStandardUniversalPlugAndPlay:

    def __init__(self, ip: str = '239.255.255.250', port: int = 5005):
        self.ip = ip
        self.port = port
        self.client = udpClient(ip, port)
        self.server = udpServer(ip, port, self.autoCallBack)

        self.registeredSelfServices = []
        self.registeredOtherServices = []

    def __del__(self):
        for i in self.registeredSelfServices:
            self.unregister(i[0], i[1], i[2], i[3], i[4])

    def register(self, serviceName: str, serviceVersion: str, serviceProtocol: str, serviceAddress: str,
                 timeout: int = 3):
        msg = \
            'r-regit * nSUPnP 1.0' + \
            '\ninst: nSUPnP/alive' + \
            '\nmaxt: ' + str(timeout) + \
            '\nname: ' + serviceName + \
            '\nvers: ' + serviceVersion + \
            '\nprot: ' + serviceProtocol + \
            '\naddr: ' + serviceAddress + \
            '\n'
        self.client.send(msg.encode('ASCII'))
        self.registeredSelfServices.append((serviceName, serviceVersion, serviceProtocol, serviceAddress, timeout))

    def unregister(self, serviceName: str, serviceVersion: str, serviceProtocol: str, serviceAddress: str,
                   timeout: int = 3):
        cntr = 0
        indx = None
        for i in self.registeredSelfServices:
            if i[0] == serviceName and i[1] == serviceVersion and i[2] == serviceProtocol and i[4] == timeout and i[
                3] == serviceAddress:
                indx = cntr
            cntr += 1
        self.registeredSelfServices.remove(self.registeredSelfServices[indx])
        msg = \
            'r-regit * nSUPnP 1.0' + \
            '\ninst: nSUPnP/byebye' + \
            '\nmaxt: ' + str(timeout) + \
            '\nname: ' + serviceName + \
            '\nvers: ' + serviceVersion + \
            '\nprot: ' + serviceProtocol + \
            '\naddr: ' + serviceAddress + \
            '\n'
        self.client.send(msg.encode('ASCII'))

    def discover(self, timeout: int = 3):
        msg = \
            's-search * nSUPnP 1.0' + \
            '\ninst: nSUPnP/discover' + \
            '\nmaxt: ' + str(timeout) + \
            '\n'
        self.client.send(msg.encode('ASCII'))
        self.registeredOtherServices.clear()

    def autoCallBack(self, data, address):
        def parse(data):
            data = data.split('\n')
            head = data[0].split('*')
            method = head[0]
            protocolVersion = head[1]
            return data[1::], method, protocolVersion

        def getDataFromParsed(data: [str], name: str):
            for i in data:
                d = i.split(':')
                if d[0] == name:
                    return d[1][1::]

        # print(data.decode(), 136, "\n")
        senderAddress = address[0]
        senderProt = address[1]

        parsedData, parsedMethod, parsedProtocol = parse(data.decode())
        if parsedMethod == 's-search ':
            if getDataFromParsed(parsedData, 'inst') == 'nSUPnP/discover':
                for i in self.registeredSelfServices:
                    self.unregister(i[0], i[1], i[2], i[3], i[4])
                    self.register(i[0], i[1], i[2], i[3], i[4])

        if parsedMethod == 'r-regit ':
            if getDataFromParsed(parsedData, 'inst') == 'nSUPnP/alive':
                self.registeredOtherServices.append(
                    Service(
                        getDataFromParsed(parsedData, 'name'),
                        getDataFromParsed(parsedData, 'vers'),
                        getDataFromParsed(parsedData, 'prot'),
                        getDataFromParsed(parsedData, 'maxt'),
                        getDataFromParsed(parsedData, 'addr')

                    )
                )
            if getDataFromParsed(parsedData, 'inst') == 'nSUPnP/byebye':
                indx = None
                cntr = 0
                for i in self.registeredOtherServices:
                    if i.name == getDataFromParsed(parsedData, 'name') and \
                            i.version == getDataFromParsed(parsedData, 'vers') and \
                            i.protocol == getDataFromParsed(parsedData, 'prot') and \
                            i.timeout == getDataFromParsed(parsedData, 'maxt') and \
                            i.address == getDataFromParsed(parsedData, 'addr'):
                        indx = cntr
                    cntr += 1
                if indx is not None:
                    try:
                        self.registeredOtherServices.remove(self.registeredOtherServices[indx])
                    except:
                        print('FAIL !!!!!')
                        print(parsedData)
                        print('END FAIL !')
