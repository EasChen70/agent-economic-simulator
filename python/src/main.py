from sim.nation import Nation
from config import NUM_CITIZENS, NUM_TICKS, EFFICIENCY_NATION_A

nation = Nation(NUM_CITIZENS, EFFICIENCY_NATION_A)

for tick in range(NUM_TICKS):
    nation.tick()
    if tick % 10 == 0:  # print every 10 ticks
        snap = nation.snapshot()
        print(f"Tick {tick:3d} | Alive: {snap['alive_citizens']:3d} | Price: {snap['market']['price']:.2f} | Food: {snap['market']['food']:.1f}")

