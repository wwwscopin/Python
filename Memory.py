# implementation of card game - Memory

import simplegui
import random

width=800



# helper function to initialize globals
def new_game():
    global state, deck, exposed, turn
    state=0
    deck=[i for i in range(8)]*2
    random.shuffle(deck)
    exposed=[False]*16
    turn=0
    label.set_text("Turns = " + str(turn))


     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global A, B, state, turn
    idx=int(pos[0]/50)
    if exposed[idx]==False:
        exposed[idx]=True
        if state == 0: 
            state =1
            A=idx
        elif state == 1: 
            state =2
            B=A
            A=idx
            turn += 1
            label.set_text("Turns = " + str(turn))
        else:      
            if deck[A]!=deck[B]:
                exposed[A]=exposed[B]=False
            A=idx
            state = 1
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    canvas.draw_line([0,0],[width,0], 1, "Yellow")
    canvas.draw_line([0,100],[width,100], 1, "Yellow")
    for i in range(18):
        canvas.draw_line([50*i,0],[50*i,100], 1, "Yellow")
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(deck[i]),[50*i+10,60], 40, "White")
        else:
            canvas.draw_polygon([[50*i,0],[50*(i+1),0],[50*(i+1),100],[50*i,100]], 1, "Yellow", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0 ")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
