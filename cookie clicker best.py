"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random


# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    def __init__(self):
        self._total = 0.0 
        self._cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._item = None
        self._history = [(self._time, self._item, 0.0, self._cookies, self._total)]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        out = "Time: " + str(self._time) + " Current Cookies: " + str(self._cookies) + \
        " CPS: " + str(self._cps) + " Total Cookies: " + str(self._total) # + \
        #" History(length: " + str(len(self._history)) + "): "  + str(self._history)
        return out
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies-self._cookies)/self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._time += time
            self._cookies += self._cps * time
            self._total += self._cps * time       
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies >= cost :
            self._item = item_name
            self._cps += additional_cps
            self._cookies -= cost
            self._history.append((self._time, self._item, cost, self._cookies, self._total))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # Replace with your code
    cbi = build_info.clone()
    cks = ClickerState()
    stop = False
    
    while cks.get_time() <= duration and (not stop):
        time_left = duration - cks.get_time()
        item = strategy(cks.get_cookies(), cks.get_cps() , time_left, cbi)
        if item == None:
            cks.wait(time_left)
            stop = True
        else:
            if cks.get_time() + cks.time_until(cbi.get_cost(item)) > duration:
                cks.wait(time_left)
                stop = True
            else:
                cks.wait(cks.time_until(cbi.get_cost(item)))
                cks.buy_item(item, cbi.get_cost(item), cbi.get_cps(item))
                cbi.update_item(item)
                
    return cks


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    To get the cheapest strategy.
    """
    cbi = build_info.clone()
    cheap = []
    temp = []
    for item in cbi.build_items():
        if cbi.get_cost(item) <= time_left*cps + cookies:
            temp.append(cbi.get_cost(item))
            cheap.append(item)
    if len(cheap)>0:
        return cheap[temp.index(min(temp))]
    else:
        return None


def strategy_expensive(cookies, cps, time_left, build_info):
    """
    To get the most expensive strategy.
    """
    cbi = build_info.clone()
    exp = []
    temp = []
    for item in cbi.build_items():
        if cbi.get_cost(item) <= time_left*cps + cookies:
            temp.append(cbi.get_cost(item))
            exp.append(item)
    if len(exp)>0:
        return exp[temp.index(max(temp))]
    else:
        return None

def strategy_best(cookies, cps, time_left, build_info):
    """
    To get the best strategy.
    """
    cbi = build_info.clone()
    best = []
    temp = []
    
    if  cookies < 600  and time_left > 0:
        for item in cbi.build_items():
            temp.append(cbi.get_cost(item))
            best.append(item)
        return best[temp.index(min(temp))]               
    else:
        for item in cbi.build_items():
            if cbi.get_cost(item) < time_left*cps + cookies:
                ev = cbi.get_cps(item)/cbi.get_cost(item)
                temp.append(ev)
                best.append(item)                          
        if len(best)>0:
            return best[temp.index(max(temp))]
        else:
            return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

