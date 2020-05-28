from mesa import Agent
import math
import random
import copy

class Firm(Agent):
    """
    This is the Class for Firms
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
        self.price = random.uniform(0.0,1.0)
        #price the firm charges
        self.area = area
        #the firms 
        self.unique_id = 0
        #unique ID
        self.profit = self.area * self.price
        # The revenue the firm will make in a move 
        self.pricechange = 0 
        #The change in price of each firm in a time step 
        self.distancemoved = 0
        #The distance a firm moves in every time step
   
    def empty_neighborhood(self):
        """
        returns the empty neighborhood for a given (agent) position 
        """
        self.neighborhood = self.model.grid.get_neighborhood(self.pos, moore = False , include_center=True)
        self.empty_positions = self.neighborhood #[c for c in self.neighborhood if self.model.grid.is_cell_filled(c)]
        return self.empty_positions

    def location_change(self):
        neighborhood = self.empty_neighborhood()
        area_before = self.area
        dict_areas = {}
        for (x,y) in neighborhood:
            area = self.model.compute_area(self.price, (x,y))
            dict_areas[(x,y)] = area
        #print(self.unique_id, "<<<<",dict_areas,",","<><><><><><>",self.unique_id)
        final_move = max(dict_areas, key=dict_areas.get)
        area_final_move = dict_areas.get(final_move)
        old_pos = self.get_pos()
        distance = get_distance(old_pos,final_move)
        #if area_final_move > area_before:
        self.model.grid.move_agent(self, final_move)
        self.distancemoved = distance
        print(self.unique_id, "<><><", final_move,",","<><><><><><>",self.unique_id)

    def price_change(self):
        profit_after = {}
        area_after = {}
        #print(self.price, "firm price")
        for i in (-0.01,0.01,0):
            test_price = copy.copy(self.price + i)
            test_area = self.model.compute_area(test_price, self.pos)
            area_after[i] = test_area
            profit_after[i] = test_area * test_price


        price_change_move = max(profit_after, key=profit_after.get)
        #print(price_change, "price change")
        #print(profit_after, "profit after")
        #print(area_after, "AREA after")     
        self.price += price_change_move
        self.area = area_after[price_change_move]
        self.pricechange = price_change_move

    def step(self):
        """
        Has to select a move, Mi such that the Profit is maximised.
        Has to select a price, Pi such that the profit is maximised.
        """   
        self.price_change()
        self.location_change()
        #To identify the maximised move decision and move to the place 
        #To identify the maximised price decision and change the price

    def get_pos(self):
        return self.pos

def get_distance(pos_1,pos_2):
    x1,y1 = pos_1
    x2,y2 = pos_2
    d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return d 