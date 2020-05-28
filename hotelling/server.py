from mesa.visualization.ModularVisualization import ModularServer
from .model import Hotelling
from .agent_firm import Firm
import copy
from .agent_consumer import Consumer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

#COLORS = {"0":"#FFE4C4", "1":"#FFDEAD", "2":"#F5DEB3", "3":"#DEB887", "4":"#D2B48C", "5":"#BC8F8F", "6":"#F4A460", "7":"#DAA520", "8":"#CD853F", "9":"#D2691E" }#"D3D3D3", "#C0C0C0","#A9A9A9","#808080","#696969","#778899","#708090","#2F4F4F","#000000"]
COLORS_list = ["#D3D3D3", "#C0C0C0","#A9A9A9","#808080","#696969","#778899","#708090","#2F4F4F","#8F8F8F","#000000", "#FFDEAD"]#"#FFE4C4","#FFDEAD", "#F5DEB3", "#DEB887", "#D2B48C", "#BC8F8F", "#F4A460", "#DAA520", "#CD853F", "#D2691E" ]
#"D3D3D3", "#C0C0C0","#A9A9A9","#808080","#696969","#778899","#708090","#2F4F4F","#000000"]

def Consumer_Agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Firm:
        portrayal["Shape"] = "circle"
        portrayal["scale"] = 0.5
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
        portrayal["Filled"] = "true"
        k = agent.unique_id + 1
        portrayal["Color"] =  COLORS_list[k]
        

    elif type(agent) is Consumer:
        (x, y) = agent.get_pos()
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = COLORS_list[agent.preffirm]

    return portrayal
grid = CanvasGrid(Consumer_Agent_portrayal, 20, 20, 400, 400)
#DataDisplay(Hotelling)
#chart_1 = ChartModule( [{"Label":i, "Color":color} for (i,color) in COLORS.items() ]) #data_collector_name= "datacollector")
chart_2 = ChartModule( [{"Label" : "Avg Distance Moved", "Color": "Red"}])
chart_1 = ChartModule( [{"Label" : "Avg Price Change", "Color": "Blue"}])

    #{"Label":i, "Color":color} for (i,color) in COLORS.items() ], data_collector_name= "datacollector")

model_params = {
    "given_firms": UserSettableParameter('slider', "Number of Firms", 2, 2, 10, 1,
                               description="Choose how many firms to have in the model"),
    "width": 20,
    "height": 20
}

server = ModularServer(Hotelling, [grid, chart_1, chart_2], "Hotelling Model", model_params)
server.port = 8521



"""
for i in COLORS.keys():
	prices = copy.deepcopy(Hotelling.get_firm_prices(Hotelling))
	trade = copy.deepcopy(Hotelling.get_firm_trade(Hotelling))
	COLORS_prices = {prices[i], COLORS[i]}
	COLORS_areas = {trade[i], COLORS[i]}
"""
