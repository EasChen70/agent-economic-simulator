#Simulation
NUM_CITIZENS = 100
NUM_TICKS = 500
POLICY_INTERVAL = 10 #Ticks until policy is applied

#Citizen Agent
CITIZEN_STARTING_WEALTH = 10.0
WAGE_PER_TICK = 2.0
HUNGER_PER_TICK = 10
HUNGER_DEATH_THRESHOLD = 80 # dies after 8 consecutive missed meals (80/10)

#Producer Agent



#Nations' Efficiency
EFFICIENCY_NATION_A = 1.0
EFFICIENCY_NATION_B = 0.8

#Trader Agent
TRADER_STARTING_WEALTH = 500.0
TRADER_STARTING_INVENTORY = 0.0
TRANSPORT_COST = 0.3

#Market
STARTING_FOOD = 150.0
STARTING_CASH = 400.0
STARTING_PRICE = 2.0
PRICE_K = 0.1 #How aggressive market reacts to shortage; Low k = slow, sluggish market. High k = volatile, reactive market
PRICE_FLOOR = 0.5 
PRICE_CEILING = 20.0
