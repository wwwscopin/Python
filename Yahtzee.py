"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def gen_sorted_sequences(outcomes, length):
    """
    Function that creates all sorted sequences via gen_all_sequences
    """    
    all_sequences = gen_all_sequences(outcomes, length)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    return set(sorted_sequences)


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = []
    for num in hand:
        scores.append(hand.count(num)*num)
    if scores != []:    
        return max(scores)
    else:
        return 0


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """ 

    outcomes = [dummy + 1 for dummy in range(num_die_sides)]
    seq = gen_all_sequences(outcomes, num_free_dice)
    scores = 0.0
    for item in seq:
        scores  += score(tuple(list(item)+ list(held_dice)))
    return scores/len(seq)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    hold = set([()])
    for ind in range(len(hand)):
        all_sequences = gen_sorted_sequences(set(list(hand)), ind+1)
        wbh = gen_sorted_sequences(set(list(hand)), ind+1)
        for sequence in all_sequences:
            for num in hand:
                if sequence.count(num) > hand.count(num):
                    wbh.discard(sequence)
        for sequence in wbh:
            hold.add(sequence)
    return hold

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    expv = []
    holds = []
    
    for held_dice in gen_all_holds(hand):
        expv.append(expected_value(held_dice, num_die_sides, len(hand) - len(held_dice)))
        holds.append(held_dice)    
    return (max(expv), holds[expv.index(max(expv))])

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



