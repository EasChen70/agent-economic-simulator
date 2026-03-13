from sim.market import Market
from sim.citizen import CitizenAgent
from sim.producer import Producer
from config import (
     WAGE_PER_TICK
)

class Nation:
    def __init__(self, num_citizens, efficiency):
        self.market = Market()
        self.producer = Producer(efficiency)
        self.citizens = [CitizenAgent() for _ in range(num_citizens)]
    
    def tick(self):
        # Wages
        alive = [citizen for citizen in self.citizens if citizen.is_alive]
        self.market.pay_wages(len(alive))
        for citizen in alive:
             citizen.wealth += WAGE_PER_TICK

        # Production
        labor = len(alive) 
        self.producer.produce(labor, self.market)

        # Consumption + Hunger / Deaths
        for citizen in alive:
           fed = citizen.consume(self.market)
           citizen.update_hunger(fed)

        # Price Update
        self.market.update_price()
    
    def snapshot(self):
        alive = sum(1 for citizen in self.citizens if citizen.is_alive)
        return {
            "alive_citizens": alive,
            "dead_citizens": len(self.citizens) - alive,
            "market": self.market.snapshot()
        }