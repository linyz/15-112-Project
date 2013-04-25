#!/usr/bin/env python
#technology demonstration - PIL
#Use PIL to handle image edit, and display/update the image in tkinter
#When click mouse left button, draw a small white square on black backgroud

from Tkinter import *
from PIL import ImageTk, Image, ImageDraw

def mousePressed(canvas, event):
    image = canvas.data.image

    r = 5
    pixels = image.load()
    print event.x, event.y
    for i in xrange(event.x - r, event.x+r):
        for j in xrange(event.y -r, event.y+r):
            pixels[i,j] = (255, 255, 255)
    redrawAll(canvas)
    
def redrawAll(canvas):
    #canvas.delete(ALL)
    image = canvas.data.image
    image_tk = ImageTk.PhotoImage(image) 
    #canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk)
    canvas.configure(image = image_tk)
    canvas.image = image_tk

    
def timerFired(canvas):
    redrawAll(canvas)
    delay = 500 # milliseconds
    def f():
        timerFired(canvas) # DK: define local fn in closure
    canvas.after(delay, f) # pause, then call timerFired again
    
def run():
    print """When click mouse left button, draw a small white square on black backgroud"""
    root = Tk()
    
    image = Image.new('RGB',(500,500))

    image_tk = ImageTk.PhotoImage(image)
    
    canvas = Label(root, image = image_tk)
    canvas.pack()
    #canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk)
    class Struct: pass
    canvas.data = Struct()
    canvas.data.image = image

    canvas.bind("<Button-1>", lambda event: mousePressed(canvas, event))
    timerFired(canvas)
    
    root.mainloop()
         

run()
