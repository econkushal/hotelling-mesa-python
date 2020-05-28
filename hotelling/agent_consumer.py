from mesa import Agent
import math
import copy
import random

class Consumer(Agent):
    """docstring for Consumer"""
    def __init__( self, pos, model,currentcost):
        super().__init__(pos, model)
        
        self.pos = pos
        #the position(fixed) of the consumer agent
        self.preffirm  = 0
        #the preferred firm of the consumer
        self.currentcost = 0 
        # the cost for transaction of the consumer, sum of cost and distance
        #self.probability = 0
    def which_firm(self,firms_positions,firms_prices):
        all_costs = {}
        for ID in firms_positions:
            my_position = copy.deepcopy(self.get_pos)
            position = firms_positions[ID]
            price = firms_prices[ID]
            cost = self.get_cost( firm_pos=position, firm_price=price)
            all_costs[ID] = cost
        chosen_firm_ID = min(all_costs, key=all_costs.get)
        self.currentcost = all_costs[chosen_firm_ID]
        return chosen_firm_ID

    def get_cost(self, firm_pos, firm_price):
        '''
        The cost of a firm has to be obtained, function that adds distance and price
        '''
        distance = get_distance(self.pos,firm_pos)
        #to get distance from the function
        cost = distance + firm_price  
        #sum of distance and price is the cost
        return cost

    def decision_to_buy(self, firm_location, firm_price):
        '''
     The decision of the consumer whether to buy from specifc firm with location and price given
        '''
        old_cost = copy.copy(self.currentcost)
        (x1,y1) = copy.deepcopy(self.pos)
        (x2,y2) = copy.deepcopy(firm_location)
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        new_cost = distance + firm_price
        
        if new_cost < old_cost:
            return True
        else:
            return False

    def get_pos(self):
        return self.pos
    

    #def step(self):
    #    self.introduce_shock(self.probability)

def get_distance(pos_1,pos_2):
    (x1,y1) = copy.deepcopy(pos_1)
    (x2,y2) = copy.deepcopy(pos_2)
    d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return d


