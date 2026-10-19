# Resource Outage Explorer

[Français](README.md) · [Español](README.es.md)

**More capacity does not necessarily repair a common failure point. This lab shows why.**

It allocates shared resources, explores every permitted outage combination in a small catalog, and compares supplied reinforcements. Every allocation carries an independently checked flow/cut certificate. Synthetic exercise scenario; no real resource is dispatched.

## Try it

Python 3.11 or newer; standard library, no key.

```sh
python3 -m outage_explorer serve --lang en
```

Open `http://127.0.0.1:8770/?lang=en`. Eight units are initially covered. Losing the shared depot leaves two available and **six unmet**. Adding four units to the main device or putting backup in that depot does not change the worst case. Three independent backup units reduce worst shortfall to **three** within this catalog.

```sh
python3 -m outage_explorer demo > analysis.json
python3 -m outage_explorer analyze outage_explorer/examples/shared-depot.json
python3 -m outage_explorer verify scenario.json certificate.json
```

`pip install .` also provides `outage-explorer`. FR/EN/ES interface and CLI messages.

## What is proven

The model is bipartite: each resource has integer capacity and explicit eligible demands. Each demand needs integer interchangeable units. Incompatible resources are never substituted merely because total capacity exists.

A maximum-flow calculation produces an allocation. A second checker directly verifies capacities, eligibility and demand, then recomputes cut capacity. **Feasible allocation = cut capacity** proves maximal flow within this model, preventing hidden better allocations under the same assumptions. Fingerprints bind certificates to their scenario.

An outage can disable multiple resources. Search enumerates every event subset whose declared cost fits the budget, up to three points. Results distinguish worst case, all combinations and minimal failure-causing event sets. **Scenario counts are not outage probabilities.**

Reinforcements increase capacity or add a resource with explicit exposure to existing outages. The choice is the best **single supplied catalog reinforcement** within budget, not universal optimization over every infrastructure configuration.

## Existing tools and limits

[NetworkX already provides flow/cut algorithms](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.minimum_cut.html). This project does not invent the theorem: it packages **common outage → proven shortfall → misleading reinforcement → compared alternative** as a standalone, checkable demo. The shared-exercise direction extends our PICS Stress Lab; [CNIG works on PCS/PICS data](https://cnig.gouv.fr/gt-plans-communaux-et-intercommunaux-de-sauvegarde-a30138.html), but this prototype is not an official tool.

Units are comparable exercise slots, not implicit conversions of people, kW or vehicles. No travel, duration, hidden skills, priorities, probabilities or real availability are modeled. No emergency response is operated, contacted, reserved or dispatched. Results do not guarantee real service continuity.

Limits: fourteen resources, twelve demands, twelve outage events, ten reinforcements and outage budget up to three points. Exhaustiveness covers only this bounded catalog; omitted failures and incorrectly declared exposures remain absent. No SOTA superiority or field effectiveness is claimed.

## Verify

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Twelve tests cover common outages, upgrades, budgets, cuts, forged certificates, eligibility and exhaustive allocation comparisons on twenty small networks. FR/EN/ES browser flows, export and mobile; CI Python 3.11/3.12 and wheel installation outside sources. MIT license; exercise/research alpha.
