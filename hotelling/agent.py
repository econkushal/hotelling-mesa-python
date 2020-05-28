from mesa import Agent
import math
import copy

class Consumer(Agent):
    """docstring for Consumer"""
    def __init__(pos, model, self, currentcost):
        super().__init__(pos, model)
        
        self.pos = pos
        #the position(fixed) of the consumer agent
        self.preffirm  = 0
        #the preferred firm of the consumer
        self.currentcost = 0 
        # the cost for transaction of the consumer, sum of cost and distance
        
    def get_cost(self, firm_pos, firm_id):
        '''
        The cost of a firm has to be obtained, function that adds distance and price

        '''
        #price = model.agent.

        consumer_pos = self.get_pos
        #to get the current position of the consumer
        distance = get_distance(firm_pos, consumer_pos)
        #to get distance from the function
        cost = distance + price  
        #sum of distance and price is the cost
        return cost
    def set_preffirm(self):
        '''
        A function that sets the Preffered firm of each of the agent
        '''
        self.currentcost = self.get_cost(self.pos, self.preffirm)
        #updating the current cost of the consumer
        firms = get.Agent.Firms 
        #to get the list of firms 
        costs={}
        for i in firms:

            new_cost = get_cost(self, pos, i)
            temp_dict = {i:new_cost}
            costs.update(temp_dict)


        new_preffirm = min(costs, key=costs.get) 
        new_cost = costs.get(new_preffirm)

        self.preffirm = new_preffirm

    def decision_to_buy(self, firm_location, firm_price):
    	'''
     The decision of the consumer whether to buy from specifc firm with location and price given
    	'''
    	old_cost = copy.copy(self.currentcost)
    	distance = get_distance(firm_location,self.pos)
    	new_cost = distance + firm_price
    	if new_cost < old_cost:
    		return True

    def get_pos(self):
        return self.pos
    #def step(self): 
"""
        The consumer at each step has to evaluate the cost (price+distance) and identify

        the firm with least cost, Fmin. 

        The consumer has to buy one unit of Good from Fmin and set it as Preferred Firm   """

        #To select the Firm, Fmin
     #   self.set_preffirm()



class Firm(Agent):
    """
    Introducing the Class for Firms
        x, y: Grid coordinates at a point of time
        area: total number of consumers that the firm has at a point of time
        price: price charged by the firm
    """
    def __init__(self, unique_id, pos, model,price, area):
        """
        Create Firms.
        Args:
            pos: The consumers coordinates on the grid.
            model: std model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        #the location of the firm
        self.price = 10
        #price the firm charges
        self.area = area
        #the firms 
        self.unique_id = 0
        #unique ID
        self.profit = self.area * self.price
    
    def empty_neighborhood(self):
        """
        returns the empty neighborhood for a given (agent) position 
        """
        self.neighborhood = self.model.grid.get_neighborhood(self.pos,moore=False, radius=1)
        self.empty_positions = self.neighborhood #[c for c in self.neighborhood if self.model.grid.is_cell_filled(c)]


        return self.empty_positions

    def location_change(self): 
    	neighborhood = self.empty_neighborhood()
    	#print (neighborhood)
    	areas = {}
    	#if self.model.schedule.step() == 1:
    	area_before = self.area
    	#print(area_before, "areabefore")
    	#else:
    		#area_before = self.model.compute_area(self.unique_id, self.pos)
    	dict_areas = {}
    	for (x,y) in neighborhood:
    		area = self.model.compute_area(self.unique_id, self.price, (x,y))
    		dict_areas[(x,y)] = area
    		#temp_dict = {(x,y):area}
    		#areas.update(temp_dict)
    		#print(temp_dict)

    	final_move = max(dict_areas, key=dict_areas.get)
    	area_final_move = dict_areas.get(final_move)
    	if area_final_move > area_before:
    		self.model.grid.move_agent(self, final_move)
    	#print(area_final_move)


    def price_change(self):
        area_after = {}
        current_price = self.price 
        area_before = self.area
        for i in (1,0,-1):
            old_price = current_price
            new_price = current_price + i 
            self.price = new_price
            temp_dict = {i:self.area}
            area_after.update(temp_dict)
            self.price = current_price

        final_price = max(area_after, key=area_after.get)
        area_final_price = area_after.get(final_price)
        if area_final_price > area_before:
            self.price = final_price 

    def step(self):
        """
        Has to select a move, Mi such that the Profit is maximised.

        Has to select a price, Pi such that the profit is maximised. 

        """   
        #To identify the maximised move decision and move to the place

        self.location_change()

        #To identify the maximised price decision and change the price 
        self.price_change()

    def get_pos(self):
        return self.pos


def get_distance(pos_1,pos_2):
        x1,y1 = pos_1
        x2,y2 = pos_2
        
        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)

        return d 


"""
    def location_change(self):
        '''
        '''
        # Pick the next cell from the adjacent cells.
        area_after = {}
        all_moves = self.model.grid.get_neighborhood(self.pos, moore=False , include_center=True)
        area_before = copy.copy(self.area) #import copy
        for x,y in all_moves:
            current_move = (x,y)
            old_pos = copy.deepcopy(self.pos)
            self.model.grid.move_agent(self, current_move)
            temp_dict = {current_move:self.area}           #Change the area to time step or to create a function. Consumer function which can take in arg new posn of the firm and the same price, returns if it will buy from the firm. 
            area_after.update(temp_dict)
            self.model.grid.move_agent(self, old_pos)

        final_move = max(area_after, key=area_after.get)
        area_final_move = area_after.get(final_move)
        if area_final_move > area_before:
            self.model.grid.move_agent(self, final_move) """
