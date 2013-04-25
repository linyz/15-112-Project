#!/usr/bin/env python
#Server for Draw
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from time import time

class User(object):
    def __init__(self, connect, seat, name):
        self.connect = connect
        self.seat = seat
        self.name = name
        self.state = 'IDLE'
        self.isReady = False
        
all_connections = {1:'None', 2:'None', 3:'None'}
isFull = False

def send_all(line, me=None):
    #print 'sending'
    for key in all_connections:
        if all_connections[key] != 'None':
            all_connections[key].sendLine(line)


class ChatProtocol(LineReceiver):
    def lineReceived(self, line):
        send_all(line, self)
            

    def connectionMade(self):
        print 'new user'
        if not isFull:
            for key in all_connections:
                if all_connections[key] == 'None':
                    all_connections[key] = self
                    self.seat = key
                    break
        self.name = 'player' + str(int(time()))
        self.sendLine('%s,welcome!' % self.name)

        
    def connectionLost(self, reason):
        print self.seat, self.name, 'lost'
        all_connections[self.seat] = 'None'

    def set_name(self, name):
        for key in all_connections:
            if all_connections[key].name == name:
                self.sendLine('name taken! Pls choose another one:')
                return
        send_all('Info: %s changed name to %s' % (self.name,name))
        self.name = name


class ChatFactory(protocol.ServerFactory):
    protocol = ChatProtocol


if __name__ == '__main__':
    reactor.listenTCP(8000, ChatFactory())
    reactor.run()

