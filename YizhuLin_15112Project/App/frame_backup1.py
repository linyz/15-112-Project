#!/usr/bin/env python
from Tkinter import *
from PIL import ImageTk, Image, ImageDraw


class DrawBoard(Frame):
    
    def __init__(self, master=None):
        self.word = 'HOUSE'
        self.time = 15
        self.image = Image.new('RGB',(500,500), '#FFFFFF')
        self.pixels = self.image.load()
        self.image_tk = ImageTk.PhotoImage(self.image)    
        
        self.colorList=['#000000', '#FFFFFF',
                        '#ED1C24', '#FFAEC9',
                        '#FF7F27', '#FFF200',
                        '#22B14C', '#00A2EB',
                        '#3F48CC', '#A349A4']
        self.Brushes=[PhotoImage(file="Brush_1.gif"), PhotoImage(file="Brush_2.gif"), PhotoImage(file="Brush_3.gif")]
        self.color = '#000000'
        self.brushSize = 5
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
        ColorPalette.grid(row=1, column=0)
        
        Brush = Frame(master,width=50, height=125)
        self.initBrush(Brush)
        Brush.grid(row=2, column=0)
        
        #draw board      
        ImageLabel = Label(master, image=self.image_tk)
        ImageLabel.grid(row=1, column=2, rowspan=10, columnspan=2)
        
        ImageLabel.bind("<Button-1>", lambda event: self.mousePressed(ImageLabel, event))
        self.timerFired(ImageLabel)
     
    def mousePressed(self, canvas, event):   
        r = self.brushSize
        print event.x, event.y
        for i in xrange(event.x - r, event.x+r):
            for j in xrange(event.y -r, event.y+r):
                self.pixels[i,j] = self.stringToRGB(self.color)
        self.redrawAll(canvas)
    
    def redrawAll(self, canvas):
        #canvas.delete(ALL)
        #canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk)
        self.image_tk = ImageTk.PhotoImage(self.image) 
        canvas.configure(image=self.image_tk)
        
    def timerFired(self, canvas):
        self.redrawAll(canvas)
        delay = 500 # milliseconds
        def f():
            self.timerFired(canvas) # DK: define local fn in closure
        canvas.after(delay, f) # pause, then call timerFired again
        
    def initColorPalette(self, master=None):
        for row in xrange(5):
            for col in xrange(2):
                Button(master,bg=self.colorList[row*2+col], text='',
                       width=3, height=1, command=self.changeColor(row*2+col)).grid(sticky='n', row=row, column=col)
                
    def initBrush(self, master=None):        
        for row in xrange(3):
            Button(master,bg='white', image=self.Brushes[row], command=self.changeBrushSize(row)).grid(sticky='n', row=row, column=0)
    
    def changeColor(self, color):
        self.color = self.colorList[color]
        
    def changeBrushSize(self, size):
        self.brushSize=(size+1)*5
    
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