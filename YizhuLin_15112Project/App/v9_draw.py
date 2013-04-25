#!/usr/bin/env python
from Tkinter import *
from PIL import ImageTk, Image, ImageDraw
import socket
import time
import threading
from twisted.internet import reactor, protocol, task, tksupport


class DrawBoard(Frame):
    
    def __init__(self, master=None):
        #iniate game info
        self.status = 'DRAW' #draw or guess
        self.count = 0 # current round
        self.word = 'HOUSE' #word to draw
        self.time = 15 #timer
        # tkinter window
        self.image = Image.new('RGB',(500,500), '#FFFFFF')
        self.pixels = self.image.load()
        self.imageStr = self.image.tostring()
        self.image_tk = ImageTk.PhotoImage(self.image)    
        self.hint = 'HINTS'
        #msg in chat box
        self.chat = StringVar()
        self.newChat = 0 #if sending a new msg
        self.colorList=['#000000', '#FFFFFF',
                        '#ED1C24', '#FFAEC9',
                        '#FF7F27', '#FFF200',
                        '#22B14C', '#00A2EB',
                        '#3F48CC', '#A349A4']
        self.Brushes=[PhotoImage(file="Brush_1.gif"), PhotoImage(file="Brush_2.gif"), PhotoImage(file="Brush_3.gif")]
        self.color = '#000000'
        self.brushSize = 5
        
        self.msg = 'Say sth and Guess here...'
        self.chatMsg = 'Hello'
        self.initUI(master)
        
    def initUI(self, master=None):
        self.frame = Frame(master)
        self.frame.grid()
        if self.status == 'DRAW':
            WordLabel = Label(master,text='Your Word: %s' % self.word)
        else:
            WordLabel = Label(master,text='What is it?')
        WordLabel.grid(row=0, column=2)
        
        TimeLabel = Label(master,text='Time: %d' % self.time)
        TimeLabel.grid(row=0, column=3)

        ColorPalette = Frame(master,width=50, height=125)
        self.initColorPalette(ColorPalette)
        ColorPalette.grid(sticky='n', row=1, column=0)
        
        Brush = Frame(master,width=50, height=125)
        self.initBrush(Brush)
        Brush.grid(sticky='n', row=2, column=0)
        
        Clear = Button(master, text='REDRAW', command=self.clearBoard).grid(sticky='n', row=3, column=0)
        
        #draw board
        ImageLabel = Label(master, image=self.image_tk)
        ImageLabel.grid(row=1, column=2, rowspan=4, columnspan=2,sticky='n')
        self.board = ImageLabel
        #ImageLabel.bind("<Button-1>", self.mousePressed)
        ImageLabel.bind("<B1-Motion>", self.leftMouseMoved)
        
        self.Hint = Label(master, bg='#FAD2C2', text=self.hint, anchor=N, width=20, height=10)
        self.Hint.grid(sticky='n', row = 1, column=4)
        self.Msg = Label(master, bg='#FAD2C2', textvariable=self.chat, anchor=NW,
                         width=20, height=10,wraplength=200, justify=LEFT)
        self.Msg.grid(sticky='n', row = 2, column=4)
        
        self.r = StringVar() 
        self.r.set(self.msg)    
        self.r_entry = Entry(width=20, textvariable=self.r)
        self.r_entry.grid(sticky='n', row = 3, column=4)     
        self.r_entry.bind('<Return>', self.settext)
        self.timerFired()
    
    def settext(self, event):
        self.chatMsg = self.r.get()
        self.r_entry.delete(0, END)
        self.newChat = 1
        #self.chat.set(self.chat.get()+self.chatMsg+'\n')
    
    def leftMouseMoved(self, event):
        if self.status == 'DRAW':
            r = self.brushSize
            for i in xrange(event.x - r, event.x+r):
                for j in xrange(event.y -r, event.y+r):
                    if self.inImage(i, j) and (i-event.x)**2+(j-event.y)**2<r**2:
                        self.pixels[i,j] = self.stringToRGB(self.color)
            self.redrawAll()        
    
    def inImage(self, x, y):
        return 0<x<500 and 0<y<500
     
    def mousePressed(self,event):
        if self.status == 'DRAW':
            r = self.brushSize
            print event.x, event.y
            print self.color
            print self.brushSize
            for i in xrange(event.x - r, event.x+r):
                for j in xrange(event.y -r, event.y+r):
                    self.pixels[i,j] = self.stringToRGB(self.color)
            self.redrawAll()
    
    def redrawAll(self):
        #canvas.delete(ALL)
        #canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk)
        self.image_tk = ImageTk.PhotoImage(self.image) 
        self.board.configure(image=self.image_tk)
        self.imageStr = self.image.tostring()
        
    def timerFired(self):
        self.redrawAll()
        delay = 250 # milliseconds
        def f():
            self.timerFired() # DK: define local fn in closure
        self.board.after(delay, f) # pause, then call timerFired again
        
    def clearBoard(self):
        if self.status == 'DRAW':
            self.image = Image.new('RGB',(500,500), '#FFFFFF')
            self.pixels = self.image.load()
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.redrawAll()
        
    def initColorPalette(self, master=None):
        
        Button(master,bg=self.colorList[0], text='',
                width=3, height=1, command=self.changeColor0).grid(sticky='n', row=0, column=0)
        Button(master,bg=self.colorList[1], text='',
                width=3, height=1, command=self.changeColor1).grid(sticky='n', row=0, column=1)
        Button(master,bg=self.colorList[2], text='',
                width=3, height=1, command=self.changeColor2).grid(sticky='n', row=1, column=0)
        Button(master,bg=self.colorList[3], text='',
                width=3, height=1, command=self.changeColor3).grid(sticky='n', row=1, column=1)
        Button(master,bg=self.colorList[4], text='',
                width=3, height=1, command=self.changeColor4).grid(sticky='n', row=2, column=0)
        Button(master,bg=self.colorList[5], text='',
                width=3, height=1, command=self.changeColor5).grid(sticky='n', row=2, column=1)
        Button(master,bg=self.colorList[6], text='',
                width=3, height=1, command=self.changeColor6).grid(sticky='n', row=3, column=0)
        Button(master,bg=self.colorList[7], text='',
                width=3, height=1, command=self.changeColor7).grid(sticky='n', row=3, column=1)
        Button(master,bg=self.colorList[8], text='',
                width=3, height=1, command=self.changeColor8).grid(sticky='n', row=4, column=0)
        Button(master,bg=self.colorList[9], text='',
                width=3, height=1, command=self.changeColor9).grid(sticky='n', row=4, column=1)
        
    def initBrush(self, master=None):        
        Button(master,bg='white', image=self.Brushes[0],
               command=self.changeBrushSize0).grid(sticky='n', row=0, column=0)   
        Button(master,bg='white', image=self.Brushes[1],
               command=self.changeBrushSize1).grid(sticky='n', row=1, column=0)
        Button(master,bg='white', image=self.Brushes[2],
               command=self.changeBrushSize2).grid(sticky='n', row=2, column=0)
        
    def changeColor0(self):
        if self.status == 'DRAW':self.color=self.colorList[0]
    def changeColor1(self):
        if self.status == 'DRAW':self.color=self.colorList[1]
    def changeColor2(self):
        if self.status == 'DRAW':self.color=self.colorList[2]
    def changeColor3(self):
        if self.status == 'DRAW':self.color=self.colorList[3]
    def changeColor4(self):
        if self.status == 'DRAW':self.color=self.colorList[4]
    def changeColor5(self):
        if self.status == 'DRAW':self.color=self.colorList[5]
    def changeColor6(self):
        if self.status == 'DRAW':self.color=self.colorList[6]
    def changeColor7(self):
        if self.status == 'DRAW':self.color=self.colorList[7]
    def changeColor8(self):
        if self.status == 'DRAW':self.color=self.colorList[8]
    def changeColor9(self):
        if self.status == 'DRAW':self.color=self.colorList[9]
        
    def changeBrushSize0(self):
        if self.status == 'DRAW':self.brushSize=5
    def changeBrushSize1(self):
        if self.status == 'DRAW':self.brushSize=10
    def changeBrushSize2(self):
        if self.status == 'DRAW':self.brushSize=20
        
    def stringToRGB(self, s):
        s = s.lstrip('#')
        lv = len(s)
        return tuple(int(s[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    
class App(Frame):
    def __init__(self, master=None):
        #Frame.__init__(self, master)
        #self.master.title("App")
        global board
        board = DrawBoard(master=master)
        
"""class Client(object):
    def __init__(self, board):
        print 'client working'
        self.data=board
        self.connect()
        self.callBack()
        
    def connect(self):
        print 'connecting'
        host = socket.gethostbyname(socket.gethostname())
        HOST = host
        PORT = 8000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print 'connected'

    def callBack(self):
        #print self.data.chatMsg
        if self.data.newChat == 1:
            #print 'sending data'
            self.s.sendall('#CHAT_'+self.data.chatMsg)
            self.data.newChat=0
        else:
            self.s.sendall('#0')
        #currMsg = self.data.chat.get()
        recMsg = self.s.recv(1024)
        if recMsg.startswith('#CHAT_'):
            currMsg = self.data.chat.get()
            recMsg=recMsg.split('_', 1)[1]
            self.data.chat.set(currMsg+recMsg+'\n')
            
        time.sleep(1)
        
        self.callBack()"""

class MyClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    
    def connectionMade(self):
        self.transport.write("hello, world!")
        
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        #print "Server said:", data
        if data.startswith('#CHAT_'):
            currMsg = board.chat.get()
            recMsg=data.split('_', 1)[1]
            board.chat.set(currMsg+recMsg+'\n')
        if data.startswith('#IMAGE_'):
            if board.status == 'GUESS':
                board.imageStr = data.split('_', 1)[1]
                board.image.fromstring(board.imageStr)
                board.redrawAll()
        #print self.data
        #self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "connection lost"

class MyFactory(protocol.ClientFactory):
    protocol = MyClient
    
    def __init__(self, game):
        self.server = None
        if game != None:
            self.game = game
        self.lc = task.LoopingCall(self.sendData)
        self.lc.start(1)
       
    def sendData(self):
        if self.server != None:
            if self.game.newChat:
                self.server.transport.write('#CHAT_'+self.game.chatMsg)
                self.game.newChat = 0
            if self.game.status == 'DRAW':
                self.server.transport.write('#IMAGE_'+self.game.imageStr)
        #reactor.callLater(0,self.sendData,reactor)
        
    def startedConnecting(self, connector):
        print 'connected'
        self.server = connector
        
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()
        
"""def main():  
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    tksupport.install(root)
    board = DrawBoard(root)
    f = MyFactory(board)
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()

if __name__ == '__main__':
    main()"""
root = Tk()
root.resizable(width=FALSE, height=FALSE)
tksupport.install(root)
board = DrawBoard(root)
f = MyFactory(board)
reactor.connectTCP("localhost", 8000, f)
reactor.run()