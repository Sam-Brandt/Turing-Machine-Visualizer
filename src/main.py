#Sam Brandt
#Visualizer for binary turing machines
#'graphics.py' must be either loaded by your IDE or downloaded manually and placed in the same folder

try:
    from graphics import *
except:
    print("graphics.py not installed properly.")
    print("\nPress return to exit.")
    input()
import random
import math

#config
window_width = 1200
window_height = 400
frame_duration = 3 #lower for faster, 1 for fastest

#Function that makes the process of drafting turing programs easier
def encode(word):
   if word == "red" or word == "right":
       return True
   else:
       return False


cards = {}
#Create your desired set of turing machine cards here. Keys in the 'card' dictionary represent card numbers,
#the first three entries in the tuple are the actions taken if the current tape cell is white,
#and the second three entries are the actions taken if the currnet tape cell is red. Generates a set of 90
#random cards by default.
#code starts
maxcards = 90
for i in range(1, maxcards + 1):
    bools = {}
    for j in range(0, 4):
        if random.randrange(0, 2) == 1:
            bools[j] = True
        else:
            bools[j] = False
    cards[i] = (bools[0], bools[1], random.randrange(0,91),
                bools[2], bools[3], random.randrange(0,91))

#Example hardcoded program.
"""cards[1] = (encode("red"), encode("right"), 2,
            encode("red"), encode("left"), 2)

cards[2] = (encode("red"), encode("left"), 1,
            encode("white"), encode("left"), 3)

cards[3] = (encode("red"), encode("right"), 0,
            encode("red"), encode("left"),  4)

cards[4] = (encode("red"), encode("right"), 4,
            encode("white"), encode("right"),  1)"""
#code ends

pgc = 1
tape = {} #Stores the states of tape cells
tape[0] = False
start = 0 #Where to start reading instructions from a card tuple
if tape[0]:
   start = 3
else:
   start = 0
ptr = 0 #Location of the head on the tape
line = 1 #State of card execution procedure
card = cards[1] #Reference to the current card
running = True
t = 0 #counter to keep track of how many program cycles have passed
camera_x = window_width / 2 #Where the screen window is located on the tape
follow_pointer = False #Whether the screen window is following the head or not
def update_state():
    global t, running, ptr, card, start, pgc, line, camera_x
    t += 1
    if t % frame_duration == 0 and running: #Handles the rate of updates
        if line == 1:
            #Modifies the current tape cell
            tape[ptr] = card[start]
        elif line == 2:
            #Updates the head location
            if card[start + 1]: #
                ptr += 1
            else:
                ptr -= 1
        elif line == 3:
            #Moves to the next card
            pgc = card[start + 2]
            if pgc == 0:
                running = False
            else:
                card = cards[pgc]
                if pgc not in cards.keys():
                    print("Card " + pgc + " does not exist!")
                    exit(1)
            if ptr in tape.keys() and tape[ptr]:
                start = 3
            else:
                start = 0
        #Updates state of card execution
        line += 1
        if line == 4:
            line = 1
    #Updates camera to the new head location if necessary
    if follow_pointer:
        camera_x = - ptr * 20 + window_width / 2

last_x = 0 #Previous x coordinate of mouse
#Prepare all variables if a mouse click begins
def begin(event):
    global follow_pointer, last_x
    follow_pointer = False
    last_x = event.x

#Updates the camera based on the movement of the clicked mouse
def during(event):
    global camera_x, last_x
    camera_x += (event.x - last_x)
    last_x = event.x

def done(event):
    unused = 0

#Switches the camera focus if the 'f' button is pressed
def press_f(event):
    global follow_pointer
    follow_pointer = not follow_pointer

win = GraphWin("Random Turing Machine", window_width, window_height, False)
win.focus_set()
win.bind('<Button-1>', begin)
win.bind('<B1-Motion>', during)
win.bind('<ButtonRelease-1>', done)
win.bind('f', press_f)
center = window_height / 2
fonts = {
    10 : ("Roboto", 10, "normal"),
    12 : ("Roboto", 12, "normal"),
    16 : ("Roboto", 16, "normal")
}

def render():
    cx = camera_x
    tdisp = math.floor(cx / 20)
    #Loop for drawing the tape
    for i in range(0, math.ceil((window_width + 1) / 20)):
        if i - tdisp in tape.keys() and tape[i - tdisp]:
            win.create_rectangle((i - 1) * 20 + cx % 20, center - 10, i * 20 + cx % 20, center + 10, fill="red")
        else:
            win.create_rectangle((i - 1) * 20 + cx % 20, center - 10, i * 20 + cx % 20, center + 10, fill="white")
        #Draws the numeric indicators every 10 cells
        if (i - tdisp) % 10 == 0:
            win.create_text(i * 20 - 10 + cx % 20, center + 20, text=str(i - tdisp), fill="black", font=fonts[10])
    #Draws the head
    win.create_polygon((ptr-1)*20+cx, center - 30, ptr*20+cx,center - 30, (ptr-0.5)*20+cx,center - 10, fill="lightgreen", outline="black")
    win.create_text(window_width / 2, 1.4 * center, text="Tape Location: " + str(ptr), fill="black", font=fonts[16])
    #The below code draws the current card
    #--------------------------------------
    win.create_rectangle(0, 0, 180, 100, outline="black", fill="white")
    #Card number
    win.create_text(30, 15, text="Card: " + str(pgc), fill="black", font=fonts[10])
    if pgc > 0:
        for i in range(0, 2):
            s = ""
            color = "black"
            loc = 50
            if i == 0:
                s = "white:"
                if start == 0:
                    color = "red"
            else:
                s = "red:"
                loc = 80
                if start == 3:
                    color = "red"
            #Conditional branching indicators
            win.create_text(30, loc, text=s, fill=color, font=fonts[10])
            #Card execution state indicator
            win.create_rectangle(40+line*30,40+start*10,40+line*30+20,40+start*10+20,outline="red")
            #What color to change the cell to
            if card[i * 3]:
                win.create_oval(80-5,50+i*30-5,80+5,50+i*30+5,fill="red")
            else:
                win.create_oval(80-5,50+i*30-5,80+5,50+i*30+5,outline="black")
            inv = 1
            if card[i * 3 + 1]:
                inv=-1
            #Which direction to move the head in
            win.create_line(110 - inv * 5, 50 + i * 30, 110 + inv * 5, 50 + i * 30 - 5, fill="black")
            win.create_line(110 - inv * 5, 50 + i * 30, 110 + inv * 5, 50 + i * 30 + 5, fill="black")
            #Next card number
            win.create_text(140, 50 + i * 30, text=str(card[(i + 1) * 3 - 1]), fill="black", font=fonts[10])
    else:
        win.create_text(90, 60, text="<terminated>", fill="black", font=fonts[10])
    #--------------------------------------
    long_string = "Click and drag to move camera, or press 'F' to lock camera on machine head."
    win.create_text(window_width / 2, 1.75 * center, text=long_string, fill="black", font=fonts[12])
    #Show everything on the screen
    win.update()
    #Collect garbage
    win.delete("all")

#Main loop
while True:
    update_state()
    render()