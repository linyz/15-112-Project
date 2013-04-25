#!/usr/bin/env python
#client test
from v5 import *
import socket
import threading
import time
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
        
class Client(object):
    def __init__(self, board):
        self.msg = board.msg
        self.chatMsg = board.chatMsg
        self.connect()
        self.callBack()
        
    def connect(self):
        host = socket.gethostbyname(socket.gethostname())
        HOST = host
        PORT = 8000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def callBack(self):
        self.s.sendall(self.chatMsg)
        print self.s.recv(1024)
        time.sleep(1)
        self.callBack()

class App(Frame):
    def __init__(self, master=None):
        #board = DrawBoard(master=master)

        #Frame.__init__(self, master)
        #self.master.title("App")
        board = threading.Thread(target=DrawBoard, args=(master,))
        board.start()
        #threading.Thread(target=Client, args=(board,)).start()
        #board = DrawBoard(master=master)
        
def main():  
    root = Tk()
    app = App(root)

    #root.geometry("400x100+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()
