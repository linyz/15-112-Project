#!/usr/bin/env python
from Tkinter import *
from PIL import ImageTk, Image, ImageDraw


class DrawBoard(Frame):
    def __init__(self, master=None):
        self.word = 'HOUSE'
        self.time = 15
        self.initUI()
        
    
    def initUI(self, master=None):
        frame = Frame.__init__(self, master)
        
        WordLabel = Label(master,text='Your Word: %s' % self.word)
        WordLabel.grid(row=0, column=0)
        WordLabel.pack()
        
        TimeLabel = Label(master,text='Time: %d' % self.time)
        TimeLabel.grid(row=0, column=1)
        TimeLabel.pack()
        
        #draw board    
        image = Image.new('RGB',(500,500))
        image_tk = ImageTk.PhotoImage(image)    
        ImageLabel = Label(master, image=image_tk)
        ImageLabel.pack()
        class Struct: pass
        ImageLabel.data = Struct()
        ImageLabel.data.image = image
        ImageLabel.bind("<Button-1>", lambda event: self.mousePressed(ImageLabel, event))
        self.timerFired(ImageLabel)
        #self.pack()
 
    def mousePressed(self, canvas, event):
        image = canvas.data.image    
        r = 5
        pixels = image.load()
        print event.x, event.y
        for i in xrange(event.x - r, event.x+r):
            for j in xrange(event.y -r, event.y+r):
                pixels[i,j] = (255, 255, 255)
        self.redrawAll(canvas)
    
    def redrawAll(self, canvas):
        #canvas.delete(ALL)
        image = canvas.data.image
        image_tk = ImageTk.PhotoImage(image) 
        #canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk)
        canvas.configure(image = image_tk)
        canvas.image = image_tk
    
        
    def timerFired(self, canvas):
        self.redrawAll(canvas)
        delay = 500 # milliseconds
        def f():
            self.timerFired(canvas) # DK: define local fn in closure
        canvas.after(delay, f) # pause, then call timerFired again
        
class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, width=100, height=100)
        self.master.title("App")
        DrawBoard(master=master)
        #self.pack()
        
def main():  
    root = Tk()
    app = App(root)
    #root.geometry("400x100+300+300")
    root.mainloop()

main()