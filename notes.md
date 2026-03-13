##### Architecture:
```
Rust Sim Core  ←──────────────────────────────┐
  └─ tick()                                    │
  └─ get_snapshot() → JSON                     │ apply_policy() ← JSON
  └─ PyO3 bindings                             │
        │                                      │
        ▼                                      │
Python Agent Layer                             │
  └─ every 10 ticks: observe → decide → apply ─┘
  └─ LLM call (Claude/GPT via API)
  └─ validator/clamper
```
##### Interaction:
- Nation:
	- Population (people who need food)
	- Production Capacity 
	- Market (domestic price + inventory + cashflows)
	
- Feedback Loop:
	- Death Spiral `Citizens die -> less labor -> less production -> prices rise -> citizens can't afford consumption -> more citizens die`
	- Price Oscillation
	- Wage-Price Squeeze `Producer raises wages to attract labor → Citizens have more cash → demand rises → Market price rises → real purchasing power unchanged.`
- Geopolitical Dependency
	- Track `import_reliance = imports / total_consumption` per nation
	- If `import_reliance > 0.5`, nation is "dependent" — Trader can raise transport cost and the nation has no choice
	- Add a **Trade War** trigger: Nation policy agent can set `export_ban = true`, Trader is blocked, dependent nation enters crisis. (Here is potential for LLM policy)

##### Tick Order (per nation, per tick)
1. **Policy** — apply `tariff` / `export_ban` / `subsidy` for this tick
2. **Wages** — Market transfers wage to each alive Citizen
3. **Production** — Producer generates food (`alive_labor × efficiency`) → Market inventory
4. **Consumption** — Citizens attempt to buy 1 food at posted price
5. **Hunger / Deaths** — failed buyers get `hunger++`, deaths applied
6. **Price Update** — new price derived from this tick's shortage/surplus
7. **Trade** — Trader arbitrages using final end-of-tick prices

##### Roles:
- The "Citizen" Agent (Consumer + Laborer)
	- **Purpose:** To drive demand and provide the labor required for production.
	- **Internal State:** `wealth` (Currency), `hunger` (0–100), `is_alive` (Boolean).
	- **The Logic:** 
		1. **Work:** Each tick, they "provide labor" to a National Production facility in exchange for a fixed wage. 
		2. **Consume:** They check the local `Market` price. They buy exactly 1 unit of food. 
		3. **Survival:** If they can't afford food, `hunger` increases. If `hunger > threshold`, they die (removing their labor from the pool).

- The "Producer" Agent (The Firm)
	- **Purpose:** A pure production function — converts labor into food. No treasury, cannot go bankrupt (POC).
	- **Internal State:** `efficiency_multiplier` (this is your **Asymmetry** trigger between nations).
	- **The Logic:**
		1. **Hire:** Collect labor units from all living Citizens.
		2. **Produce:** $Food\_Generated = Labor\_Units \times Efficiency$
		3. **Sell:** Deposit all generated food into the National Market. Wages are paid directly from Market cash reserve (not Producer capital).

- The "Trader" Agent (The International Trader)
	- **Purpose:** To equalize prices and facilitate geopolitical dependency.
	- **Internal State:** `inventory` (Food), `balance` (Currency).
	- **The Logic:**
		1. **Compare:** Check $Price\_A$ vs $Price\_B$ at end of tick.
		2. **Trade:** If $Price\_A + \text{Transport\_Cost} < Price\_B$, buy food in Nation A, sell in Nation B.
		3. **Impact:** Drains food from the cheap nation → forces its price up → creates dependency over time.

- The "National Market" (The System Manager)
	- **Purpose:** A Deterministic State Machine. Acts as the national treasury — holds Currency and Food pools, posts price, pays wages.
	- **Money Flow:** Market is initialized with starting cash. Wages flow out to Citizens each tick; Citizens spend back when buying food. Money circulates, never leaves the system.
	- **Price Discovery (shortage-based):**
		- `shortage = (attempted_demand - fulfilled) / max(1, attempted_demand)`
		- If shortage > 0: `price *= (1 + k × shortage)`
		- If surplus: `price *= (1 - k2 × surplus_ratio)` *(optional)*
		- Clamp: `price_floor ≤ price ≤ price_ceiling`