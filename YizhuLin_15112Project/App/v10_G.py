#!/usr/bin/env python
from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
import time
import math
from twisted.internet import reactor, protocol, task, tksupport
from twisted.protocols.basic import LineReceiver

class DrawBoard(Frame):
    
    def __init__(self, master=None):
        #iniate game info
        self.status = 'GUESS' #draw or guess
        self.count = 0 # current round
        self.word = 'HOUSE' #word to draw
        self.time = 15 #timer
        # tkinter window
        self.image = Image.new('RGB',(500,500), '#FFFFFF')
        self.pixels = self.image.load()
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
        self.brushSize = 2
        
        self.msg = 'Say sth and Guess here...'
        self.chatMsg = 'Hello'
        #mouse status
        self.b1Pressed = False
        self.oldx = None
        self.oldy = None
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
        
        Clear = Button(master, text='REDRAW', command=self.redrawPressed).grid(sticky='n', row=3, column=0)
        
        #draw board
        ImageLabel = Label(master, image=self.image_tk)
        ImageLabel.grid(row=1, column=2, rowspan=4, columnspan=2,sticky='n')
        self.board = ImageLabel
        ImageLabel.bind("<ButtonPress-1>", self.mousePressed)
        ImageLabel.bind("<ButtonRelease-1>", self.mouseReleased)
        ImageLabel.bind("<Motion>", self.mouseMoved)
        
        self.Hint = Label(master, bg='#FAD2C2', text=self.hint, anchor=N, width=20, height=10)
        self.Hint.grid(sticky='n', row = 1, column=4)
        self.Msg = Label(master, bg='#FAD2C2', textvariable=self.chat, anchor=NW,
                         width=20, height=10,wraplength=200, justify=LEFT)
        self.Msg.grid(sticky='n', row = 2, column=4)
        
        self.r = StringVar() 
        self.r.set(self.msg)    
        self.r_entry = Entry(width=20, textvariable=self.r)
        self.r_entry.grid(sticky='n', row = 3, column=4)     
        self.r_entry.bind('<Return>', self.chatEntry)
        self.timerFired()
    
    def chatEntry(self, event):
        self.chatMsg = self.r.get()
        self.r_entry.delete(0, END)
        self.newChat = 1
        MyFactory.sendChat(f)
    
    def mouseMoved(self, event):
        if (self.status == 'DRAW' and self.b1Pressed and
            self.oldx != None and self.oldy != None):
            r = self.brushSize            
            for i in xrange(min(event.x, self.oldx)-r,max(event.x,self.oldx)+r):
                for j in xrange(min(event.y, self.oldy)-r,max(event.y,self.oldy)+r):
                    distance = self.dPointToLine(event.x, event.y, self.oldx, self.oldy, i, j)
                    if distance < r and self.inImage(i, j):
                        self.pixels[i,j] = self.stringToRGB(self.color)
                        f.sendPixel(i, j, self.color)

            self.redrawAll()
        self.oldx = event.x
        self.oldy = event.y
    
    def dPointToLine(self, x0, y0, x1, y1, i, j):
        a = y1-y0
        b = x0-x1
        c = y0*x1-y1*x0
        if math.sqrt(float(a**2+b**2)) == 0: return 100
        return abs(a*i+b*j+c)/math.sqrt(float(a**2+b**2))
    
    def inImage(self, x, y):
        return 0<x<500 and 0<y<500
     
    def mousePressed(self,event):
        self.b1Pressed = True
        
    def mouseReleased(self,event):
        self.b1Pressed = False
        self.oldx = None
        self.oldy = None
        
    def redrawAll(self):
        #canvas.delete(ALL)
        #canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk)
        self.image_tk = ImageTk.PhotoImage(self.image) 
        self.board.configure(image=self.image_tk)
        
    def timerFired(self):
        self.redrawAll()
        delay = 250 # milliseconds
        def f():
            self.timerFired() # DK: define local fn in closure
        self.board.after(delay, f) # pause, then call timerFired again
    
    def redrawPressed(self):
        if self.status == 'DRAW':
            self.clearBoard()
            f.sendClear()
        
    def clearBoard(self):
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
        if self.status == 'DRAW':self.brushSize=2
    def changeBrushSize1(self):
        if self.status == 'DRAW':self.brushSize=5
    def changeBrushSize2(self):
        if self.status == 'DRAW':self.brushSize=10
        
    def stringToRGB(self, s):
        s = s.lstrip('#')
        lv = len(s)
        return tuple(int(s[i:i+lv/3], 16) for i in range(0, lv, lv/3))

class MyClient(LineReceiver):
    """Once connected, send a message, then print the result."""
    
    def connectionMade(self):
        self.sendLine("hello, world!")
        self.factory.clientReady(self)
        
    def lineReceived(self, data):
        if data.startswith('#CHAT_'):
            currMsg = board.chat.get()
            recMsg=data.split('_', 1)[1]
            board.chat.set(currMsg+recMsg+'\n')
        elif data=='#CLEAR_' and board.status == 'GUESS':
            board.clearBoard()
        elif data.startswith('#PIXEL_'):
            if board.status == 'GUESS':
                (i,j,color)=tuple(data.split('_')[1:4])
                board.pixels[int(i),int(j)]=board.stringToRGB(color)
        #print self.data
        #self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "connection lost"

class MyFactory(protocol.ClientFactory):
    protocol = MyClient
    
    def __init__(self, game):
        self.clientInstance = 'None'
        if game != None:
            self.game = game
        """self.lc = task.LoopingCall(self.sendData)
        self.lc.start(1)"""
    
    def sendPixel(self, i,j, color):
        if self.clientInstance != 'None':
            pixelStr = '#PIXEL_'+str(i)+'_'+str(j)+'_'+color
            self.clientInstance.sendLine(pixelStr)
       
    def sendChat(self):
        if self.clientInstance != 'None':
            #if self.game.newChat:
            self.clientInstance.sendLine('#CHAT_'+self.game.chatMsg)
            #protocol.sendLine('#CHAT_'+self.game.chatMsg+'_END;')
                #self.game.newChat = 0
        #reactor.callLater(0,self.sendData,reactor)
    
    def sendClear(self):
        if self.clientInstance != 'None':
            self.clientInstance.sendLine('#CLEAR_')            
        
    """def startedConnecting(self, connector):
        print 'connected'
        self.server = connector"""
    def clientReady(self, instance):
        self.clientInstance = instance    
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
root.protocol("WM_DELETE_WINDOW", reactor.stop)
tksupport.install(root)
board = DrawBoard(root)
f = MyFactory(board)
reactor.connectTCP("localhost", 8000, f)
reactor.run()
