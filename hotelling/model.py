from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
import math
import copy
from .agent_firm import Firm
from .agent_consumer import Consumer



class Hotelling (Model):
    """
    Model Class
    """
    def __init__(self, given_firms, C=400, width=20, height=20 ):
        self.num_consumers = C
        self.height = height
        self.width = width
        self.given_firms = given_firms
        #self.probability = probability
        self.grid = MultiGrid(height, width, True)
        self.schedule = RandomActivation(self)
        self.firms_list = []
        self.consumers_list = []
        self.firms_dictionary = {}
        self.firms_locations = {}
        self.firms_prices = {}
        self.firms_area = {}
        self.test_record = 0 
        self.datacollector = DataCollector(model_reporters= {"Avg Price Change" : Compute_Pricechange, "Avg Distance Moved" : Compute_Distancemoved}) #agent_reporters = {"prices_firms": "pos"})        
        #self.firms_prices_compute = []
        # Create Consumers

        for (contents, x, y) in self.grid.coord_iter():
            current_cost = 0
            Agent_Consumer = Consumer((x,y), self, current_cost)
            self.schedule.add(Agent_Consumer)
            self.grid.place_agent(Agent_Consumer, (x,y))
            self.consumers_list.append(Agent_Consumer)
            #Agent_Consumer.probability = self.probability
        	
        # Create Firms 
        for i in range (self.given_firms):
            price = random.uniform(0,1)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            area = 0
            Agent_Firm = Firm(i,(x,y),self, price, area)
            Agent_Firm.unique_id = i
            Agent_Firm.price = price
            Agent_Firm.pricechange = 0 
            Agent_Firm.distancemoved = 0
            self.grid.place_agent(Agent_Firm, (x,y))
            self.schedule.add(Agent_Firm)
            self.firms_list.append(Agent_Firm)
            self.firms_locations[i] = (x,y)
            self.firms_prices[i] = price
            self.firms_area[i] = area
            self.firms_dictionary[i] = Agent_Firm
            
            #self.firms_prices_compute.append(price)

        self.running = True
        self.set_consumers_firms()
        #self.datacollector = DataCollector(model_reporters= {"firms_prices_compute" : self.get_firm_prices(), "firms_area" : self.get_firm_trade()})        
        

        self.datacollector.collect(self)

    def update_firms_locations(self):
    	for firm in self.firms_list:
    		self.firms_locations[firm.unique_id] = firm.pos
    		#print(firm.pos)

    def update_firms_prices(self):
    	for firm in self.firms_list:
    		self.firms_prices[firm.unique_id] = firm.price
    		#self.firms_prices_compute[firm.unique_id] = firm.price

    def update_firms_areas(self):
        for firm in self.firms_list:
            self.firms_areas[firm.unique_id] = firm.area
    

    def set_consumers_firms(self):

    	for c in self.consumers_list:
    		chosen_firm_ID = c.which_firm(self.firms_locations, self.firms_prices) 
    		c.preffirm = copy.copy(chosen_firm_ID)
    		firm = self.firms_dictionary[chosen_firm_ID]
    		firm.area += 1

    def update_consumers(self):
    	for c in self.consumers_list:
    		chosen_firm_ID = c.which_firm(self.firms_locations, self.firms_prices) 
    		c.preffirm = copy.copy(chosen_firm_ID)

    def get_distance(self, pos_1,pos_2):
        x1,y1 = pos_1
        x2,y2 = pos_2
        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return d 

    def compute_area(self, firm_price, new_location): 
    	count = 0

    	for c in self.consumers_list:
    		if c.decision_to_buy(new_location, firm_price) is True:
    				count += 1
    	return count

    def get_firm_prices(self):
    	Prices = []
    	for f in self.firms_list:
    		#price = f.price
    		Prices.append(f.price)
    	return Prices
    def get_firm_trade(self):
    	Areas =[]
    	for f in self.firms_list:
    		#zarea = f.area
    		Areas.append(f.area)
    	return Areas

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        self.update_consumers()
        self.update_firms_locations()
        self.update_firms_prices()
        #self.introduce_shock(self.probability)
        self.datacollector.collect(self)

        #self.update_firms_areas()
        #self.dc

def Compute_Pricechange(model):
    x=0
    for agent in model.schedule.agents:
        if type(agent) is Firm:
            x += abs(agent.pricechange)
    return x/model.given_firms

def Compute_Distancemoved(model):
    x = 0
    for agent in model.schedule.agents:
        if type(agent) is Firm:
            x += agent.distancemoved
    return x/model.given_firms