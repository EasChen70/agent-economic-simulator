from config import (
    STARTING_FOOD, 
    STARTING_CASH, 
    STARTING_PRICE, 
    PRICE_K, 
    PRICE_FLOOR, 
    PRICE_CEILING,
    WAGE_PER_TICK
)
class Market:
    '''
    Market - economic heart of one nation, holds two pools
        food - units available to buy
        cash - currency in circulation
    '''
    def __init__(self):
        self.food = STARTING_FOOD
        self.cash = STARTING_CASH
        self.price = STARTING_PRICE
        self.attempted_demand = 0
        self.fulfilled = 0   

    def pay_wages(self, n):
        payroll = n * WAGE_PER_TICK
        self.cash -= payroll

    def receive_food(self, units):
        self.food += units

    def sell_food(self, wealth):
        if wealth >= self.price and self.food >= 1:
            self.cash += self.price
            self.food -= 1
            self.attempted_demand += 1 #every attempt success or not
            self.fulfilled += 1 #only on success
            return True
        else:
            self.attempted_demand += 1
            return False

    def update_price(self):
        shortage = (self.attempted_demand - self.fulfilled) / max (1, self.attempted_demand)
        if shortage > 0:
            self.price *= (1 + PRICE_K * shortage)
        #clamp: price_floor <= price <= price_ceiling
        self.price = max(PRICE_FLOOR, min(PRICE_CEILING, self.price))
        self.attempted_demand = 0  
        self.fulfilled = 0          
        return shortage

    def snapshot(self):
        shortage = (self.attempted_demand - self.fulfilled) / max (1, self.attempted_demand)
        return {
            "price": self.price,
            "food": self.food,
            "cash": self.cash,
            "shortage_rate": shortage
        }
