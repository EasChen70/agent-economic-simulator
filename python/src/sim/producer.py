class Producer:
    def __init__(self, efficiency):
        self.efficiency = efficiency

    def produce(self, labor, market):
        units = labor * self.efficiency
        market.receive_food(units)