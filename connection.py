#!/usr/bin/python

import socket
import ssl
import time
import helper

# This is a simple TCP/TLS client which just wraps socket's methods
# It assumes that a connection is closed if any I/O error occured
class Client:

    def __init__(self, host, port, is_tls = False):
        self.host = host
        self.port = port
        self.is_tls = is_tls
        self.connected = False

    def connect(self):
        self.connected = False
        self.verbose('connect to {0}:{1:d}'.format(self.host, self.port))
        if self.is_tls:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            self.context.set_alpn_protocols(['h2'])
            self.socket = self.context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.connected = True

    def send(self, data):
        try:
            if self.connected is False:
                self.connect()
            self.socket.sendall(data)
        except socket.error as msg:
            self.connected = False
            self.verbose('could not send data: {0}'.format(msg))
            raise

    def receive(self, length = 1024):
        try:
            if self.connected is False:
                self.connect()
            return self.socket.recv(length)
        except socket.error as msg:
            self.connected = False
            self.verbose('could not receive data: {0}'.format(msg))
            raise

    def isconnected(self):
        return self.connected

    def close(self):
        self.connected = False
        self.socket.close()

    def verbose(self, message):
        helper.verbose('[{0}] {1}'.format(Client.__name__, message))
