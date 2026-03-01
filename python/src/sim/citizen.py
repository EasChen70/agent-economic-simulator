from config import (
    CITIZEN_STARTING_WEALTH,
    WAGE_PER_TICK,
    HUNGER_PER_TICK,
    HUNGER_DEATH_THRESHOLD
)
class CitizenAgent:
    def __init__(self):
        self.wealth = CITIZEN_STARTING_WEALTH
        self.hunger = 0
        self.is_alive = True

    def work(self, market):
        market.pay_wages(1)
        self.wealth += WAGE_PER_TICK

    def consume(self, market):
        success =market.sell_food(self.wealth)
        if success:
            self.wealth -= market.price
        return success

    def update_hunger(self, fed):
        if fed:
            self.hunger = max(0, self.hunger - HUNGER_PER_TICK)
        else:
            self.hunger += HUNGER_PER_TICK
            if self.hunger >= HUNGER_DEATH_THRESHOLD:
                self.is_alive = False
    
    def snapshot(self):
        return {
            "wealth": self.wealth,
            "hunger": self.hunger,
            "is_alive": self.is_alive
        }