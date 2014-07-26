# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message=""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        s = ""
        for card in self.hand:
            s = s + str(card) + " "
        return  s      

    def add_card(self, card):
        return self.hand.append(card)# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        point  = 0
        countA = 0
        for card in self.hand: 
            point = point + VALUES[card.get_rank()]
            if card.get_rank()=="A": countA += 1
        if countA >=1:
            if point <=11 :
                point += 10
        return point # compute the value of the hand, see Blackjack video
  
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += 90
        if in_play:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100,200], CARD_BACK_SIZE)# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]	# create Hand object
        
    def __str__(self):
        s=""
        for card in self.deck:
            s = s + str(card) + " "           
        return  "Deck contains " + s

    def deal_card(self):
        return self.deck.pop(0)# add a card object to a hand

    def shuffle(self):   
        return random.shuffle(self.deck)# add a card object to a hand
 


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, score, deck, message
    
    if in_play == True:
        # if player clicks Deal button during a hand, player loses hand in progress
        message = "Hand starts ..."
        deck = Deck()
        deck.shuffle()
        score -= 1
        player = Hand()
        dealer = Hand()
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    if in_play == False:
        # starts a new hand
        deck = Deck()
        deck.shuffle()
        player = Hand()
        dealer = Hand()
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        message = "New Hand. Hit or Stand?"
        in_play = True
           

def hit():
    global in_play, deck, score, message
    if in_play == True:
        player.add_card(deck.deal_card())
        message = "Hit or Stand?"
        if player.get_value() > 21:
            in_play = False
            message = "Player has busted! Play again?"
            score -= 1
            outcome = "Dealer: " + str(dealer.get_value()) + "  Player: " + str(player.get_value())
       
def stand():
    # hits dealer until >=17 or busts. Determines winner of hand and adjusts score, game state, and messages
    global in_play, score, message, outcome
    if in_play == False:
        message = "Hand over. New deal?"
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            message = "Dealer busted. Player wins! Play again?"
            score += 1
            in_play = False
        elif dealer.get_value() >= player.get_value():
            message = "Dealer wins. Play again?"
            score -= 1
            in_play = False
        elif dealer.get_value() < player.get_value():
            message = "Player wins! Play again?"
            score += 1
            in_play = False
        outcome = "Dealer: " + str(dealer.get_value()) + "  Player: " + str(player.get_value())

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [20,50], 50, "White")
    canvas.draw_text("Player's Score: " + str(score), [300,100], 36, "Black")
    canvas.draw_text("Dealer", [80,140], 30, "Black")
    canvas.draw_text("Player", [80,430], 30, "Black")
    canvas.draw_text(message, [200,355], 24, "Black")
    canvas.draw_text(outcome, [320,130], 24, "Yellow")
    player.draw(canvas, [80,450])
    dealer.draw(canvas, [80,180])
   
    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50,350], CARD_BACK_SIZE)# draw a hand on the canvas, use the draw method for cards


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
