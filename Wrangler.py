"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    
    list2 = []
    for idx in range(len(list1)):
        if list1[idx] not in list1[idx + 1:]:
            list2.append(list1[idx])
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    lst1 = list1[:]
    lst2 = list2[:]
    if len(lst1) == 0 or len(lst2) == 0:
        return result
    else:
        while (lst1 and lst2):
            if lst1[0] < lst2[0]: # Compare both heads
                lst1.pop(0) # Pop from the head
            elif lst1[0] > lst2[0]:
                lst2.pop(0)
            else:         
                item = lst1.pop(0)
                lst2.pop(0)
                result.append(item)
        return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """   
    result = []

    # Copy both the args to make sure the original lists are not
    # modified
    lst1 = list1[:]
    lst2 = list2[:]

    while (lst1 and lst2):
        if lst1[0] <= lst2[0]: # Compare both heads
            item = lst1.pop(0) # Pop from the head
            result.append(item)
        else:
            item = lst2.pop(0)
            result.append(item)

    # Add the remaining of the lists
    result.extend(lst1 if lst1 else lst2)
    return result
          
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    mid = len(list1)/2
    if len(list1) <= 1 :
        return list1
    elif mid >=1:
        temp = merge(merge_sort(list1[0:mid]), merge_sort(list1[mid:]))
        return temp
   
#print merge_sort([1,11,3, 4,2,6])  
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    answer = [""]
    if len(word) == 0:
        return answer
    elif len(word) == 1:
        answer.append(word)
        return answer
    else:
        first = word[0]
        rest = gen_all_strings(word[1:])
        answer = gen_all_strings(word[1:])
        for string in rest:
            for idx in range(len(string)+1):
                if idx == 0:
                    answer.append(first + string)
                else:
                    answer.append(string[0:idx] + first + string[idx:])
        return answer

#print gen_all_strings()
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    strings = []
    url = codeskulptor.file2url(filename)
    content = urllib2.urlopen(url)
    for line in content.readlines():
        strings.append(line[:-1])
    return strings

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
