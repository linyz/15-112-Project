#!/usr/bin/env python
from Tkinter import *
from PIL import ImageTk, Image, ImageDraw


class DrawBoard(Frame):
    
    def __init__(self, master=None):
        self.count = 0
        self.word = 'HOUSE'
        self.time = 15
        self.image = Image.new('RGB',(500,500), '#FFFFFF')
        self.pixels = self.image.load()
        self.image_tk = ImageTk.PhotoImage(self.image)    
        self.hint = 'HINTS'
        self.chat = StringVar()
        #self.chat = 'Player_1: Hi!'
        self.colorList=['#000000', '#FFFFFF',
                        '#ED1C24', '#FFAEC9',
                        '#FF7F27', '#FFF200',
                        '#22B14C', '#00A2EB',
                        '#3F48CC', '#A349A4']
        self.Brushes=[PhotoImage(file="Brush_1.gif"), PhotoImage(file="Brush_2.gif"), PhotoImage(file="Brush_3.gif")]
        self.color = '#000000'
        self.brushSize = 5
        
        self.msg = 'Say sth and Guess here...'
        self.chatMsg = ''
        
        self.initUI(master)
    
    def initUI(self, master=None):
        frame = Frame(master)
        frame.grid()
        WordLabel = Label(master,text='Your Word: %s' % self.word)
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
        self.chat.set(self.chat.get()+self.chatMsg+'\n')
    
    def leftMouseMoved(self, event):
        r = self.brushSize
        for i in xrange(event.x - r, event.x+r):
            for j in xrange(event.y -r, event.y+r):
                if self.inImage(i, j) and (i-event.x)**2+(j-event.y)**2<r**2:
                    self.pixels[i,j] = self.stringToRGB(self.color)
        self.redrawAll()        
    
    def inImage(self, x, y):
        return 0<x<500 and 0<y<500
     
    def mousePressed(self,event):   
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
        
    def timerFired(self):
        self.redrawAll()
        delay = 500 # milliseconds
        def f():
            self.timerFired() # DK: define local fn in closure
        self.board.after(delay, f) # pause, then call timerFired again
        
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
        self.color=self.colorList[0]
    def changeColor1(self):
        self.color=self.colorList[1]
    def changeColor2(self):
        self.color=self.colorList[2]
    def changeColor3(self):
        self.color=self.colorList[3]
    def changeColor4(self):
        self.color=self.colorList[4]
    def changeColor5(self):
        self.color=self.colorList[5]
    def changeColor6(self):
        self.color=self.colorList[6]
    def changeColor7(self):
        self.color=self.colorList[7]
    def changeColor8(self):
        self.color=self.colorList[8]
    def changeColor9(self):
        self.color=self.colorList[9]
        
    def changeBrushSize0(self):
        self.brushSize=5
    def changeBrushSize1(self):
        self.brushSize=10
    def changeBrushSize2(self):
        self.brushSize=20
        
    def stringToRGB(self, s):
        s = s.lstrip('#')
        lv = len(s)
        return tuple(int(s[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    
class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("App")
        DrawBoard(master=master)
        #self.pack()
        
def main():  
    root = Tk()
    app = App(root)
    #root.geometry("400x100+300+300")
    root.mainloop()

main()