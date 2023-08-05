from tkinter import *
from graphics import *
from tkinter import Image
import tkinter.font as tkFont


class window:
    
    def Createwindow(nameWindow = str,widthWindow = int, heightWindow = int ):     

        global cubeCount
        cubeCount = 0


        global windowWidth
        windowWidth = widthWindow

        global windowHeight
        windowHeight = widthWindow

        global win 
        win = tk.Tk()
        win.title(nameWindow)
        win.iconbitmap("assets/images/window/icon.ico")
        win.geometry("{}x{}".format(widthWindow, heightWindow))
        
        global c

        c = Canvas(win, width=windowWidth*120, height=windowHeight*120, bg='white')

    def waitWindow():
        win.wait_window()
    
    def close():
        win.quit()
        

    def setIcon(nameIcon = str):
        win.iconbitmap("assets/images/window/" + nameIcon)
    
    

class CanvasDraw:

    
    
    
    

    def CreateText(xPos = float, yPos = float, textWord = str, widthFont = float, heightFont = float):
        label = Label(win, text=textWord)
        label.place(x=xPos, y=yPos, height=heightFont, width=widthFont)

    def CreateCube(xPos1 = float, yPos1 = float, xPos2 = float, yPos2 = float, widthCube = float):      
        c.create_rectangle(xPos1, yPos1, xPos2, yPos2, width=widthCube)
        c.pack()

    def CreateLine(xPos1 = float, yPos1 = float, xPos2 = float, yPos2 = float, widthLine = float):      
        c.create_line(xPos1, yPos1, xPos2, yPos2, width=widthLine)
        c.pack()

    def CreateCircle(xPos1 = float, yPos1 = float, xPos2 = float, yPos2 = float, widthCircle = float):
        global circle
        circle = c.create_oval(xPos1, yPos1, xPos2, yPos2, width=widthCircle)
        c.pack()

    def ImageLoad(ImageName = str):
        img = PhotoImage(file="C:/Users/fokus/Documents/BytexPy/scripts/assets/images/" + ImageName, master=win)
        label = Label(win, image=img)
        label.image_ref = img
        label.pack()

     
    
        
        

    
        







