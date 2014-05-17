# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui 
import random
import math


# initialize global variables used in your code
num_range=100
num_guess=7
secret_num=random.randrange(0, num_range)
ran=1

# helper function to start and restart the game
def new_game():
    f.start()
    if ran==1:  range100()
    elif ran==2: range1000()
    
    
# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global secret_num, num_guess,ran
    ran=1
    num_guess=7
    secret_num=random.randrange(0, 100)
    print "New game. Range is from 0 to 100"
    print "Number of remaining guess is", num_guess

def range1000():
    # button that changes range to range [0,1000) and restarts
    global secret_num, num_guess, ran
    ran=2
    num_guess=10
    secret_num=random.randrange(0, 1000)
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guess is", num_guess

    
def input_guess(guess):
    # main game logic goes here	
    print "Guess was ", guess
    global in_num, num_guess
    in_num=int(guess)
    num_guess=num_guess-1
    print "Number of remaining guess is", num_guess
    if num_guess>0: 
        if in_num>secret_num: print "Higher!"
        elif in_num<secret_num: print "Lower!"
        else: print "Your guess is right!, The number was",secret_num
    else: print "You run out of guess. The number was", secret_num
    if num_guess==0: new_game()
        

    
# create frame
f=simplegui.create_frame("Guess the number",200,200)


# register event handlers for control elements
f.add_button("Range is [0,100)",range100,200)
f.add_button("Range is [0,1000)",range1000,200)
f.add_input("Enter a guess", input_guess,200)



# call new_game and start frame
new_game




# always remember to check your completed program against the grading rubric
