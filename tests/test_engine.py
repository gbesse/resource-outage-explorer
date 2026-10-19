from copy import deepcopy
import itertools
import json
from pathlib import Path
import random
import unittest

from outage_explorer.engine import allocate,analyze,outage_sweep,upgraded,verify_certificate

ROOT=Path(__file__).resolve().parent.parent


def example():return json.loads((ROOT/"outage_explorer/examples/shared-depot.json").read_text())


class OutageTests(unittest.TestCase):
    def test_baseline_has_capacity_but_common_cause_removes_it(self):
        case=example()
        self.assertEqual(allocate(case)["delivered_units"],8)
        sweep=outage_sweep(case)
        self.assertEqual(sweep["worst"]["events"],["shared-depot-loss"])
        self.assertEqual(sweep["worst"]["shortfall"],6)
        self.assertEqual(sweep["worst"]["flow"]["cut_capacity"],2)

    def test_bigger_or_colocated_backup_does_not_fix_common_cause(self):
        result=analyze(example())
        values={u["upgrade"]:u["worst_shortfall"] for u in result["upgrade_comparisons"]}
        self.assertEqual(values,{"larger-main-device":6,"backup-in-same-depot":6,"independent-backup":3})
        self.assertEqual(result["best_single_catalog_upgrade"],"independent-backup")
        self.assertFalse(result["dispatch_performed"])

    def test_upgrade_budget_is_respected(self):
        result=analyze(example(),investment_budget=1)
        self.assertEqual(result["upgrade_comparisons"],[])
        self.assertIsNone(result["best_single_catalog_upgrade"])

    def test_zero_outage_budget_only_checks_baseline(self):
        result=outage_sweep(example(),budget=0)
        self.assertEqual(result["scenarios_checked"],1)
        self.assertEqual(result["worst"]["shortfall"],0)

    def test_all_budgeted_combinations_are_enumerated(self):
        result=outage_sweep(example(),budget=2)
        self.assertEqual(result["scenarios_checked"],7)
        self.assertTrue(result["exhaustive_within_catalog_and_budget"])
        for scenario in result["all_scenarios"]:self.assertTrue(scenario["flow"]["certificate"]["valid"])

    def test_minimal_failures_are_an_antichain(self):
        failures=outage_sweep(example(),budget=2)["minimal_failing_event_sets"]
        self.assertIn(["shared-depot-loss"],failures)
        self.assertTrue(all(not set(a)<set(b) for a in failures for b in failures))

    def test_lack_of_eligibility_is_not_replaced_by_total_capacity(self):
        case={"resources":[{"id":"r","capacity":100,"serves":["a"]}],"demands":[{"id":"a","need":1},{"id":"b","need":5}]}
        result=allocate(case)
        self.assertEqual(result["delivered_units"],1)
        self.assertEqual(result["unmet"]["b"],5)
        self.assertTrue(result["certificate"]["maximum_flow_proven"])

    def test_independent_checker_rejects_forged_flow_and_shortfall(self):
        case=example();result=allocate(case)
        for key,value in (("delivered_units",100),("cut_capacity",0),("unmet",{}),("source_side_cut",["source","sink"])):
            fake=deepcopy(result);fake[key]=value
            self.assertFalse(verify_certificate(case,fake)["valid"])

    def test_disabled_resource_cannot_allocate_units(self):
        case=example();result=allocate(case,["depot-main"])
        fake=deepcopy(result);fake["allocations"].append({"resource":"depot-main","demand":"north","units":1})
        self.assertFalse(verify_certificate(case,fake)["valid"])

    def test_maxflow_matches_exhaustive_integer_allocation_oracle(self):
        rng=random.Random(42)
        for _ in range(20):
            resources=[{"id":f"r{i}","capacity":rng.randint(0,2),"serves":[d for d in ("a","b") if rng.choice([True,False])]} for i in range(2)]
            demands=[{"id":"a","need":rng.randint(1,2)},{"id":"b","need":rng.randint(1,2)}]
            case={"resources":resources,"demands":demands};edges=[(r["id"],d) for r in resources for d in r["serves"]]
            best=0
            for values in itertools.product(range(3),repeat=len(edges)):
                flow=dict(zip(edges,values))
                if any(sum(v for (r,_),v in flow.items() if r==resource["id"])>resource["capacity"] for resource in resources):continue
                if any(sum(v for (_,d),v in flow.items() if d==demand["id"])>demand["need"] for demand in demands):continue
                best=max(best,sum(values))
            self.assertEqual(allocate(case)["delivered_units"],best)

    def test_upgrades_preserve_source_scenario(self):
        case=example();copy=deepcopy(case);upgraded(case,case["upgrades"][1]);self.assertEqual(case,copy)

    def test_case_changes_invalidate_old_certificate(self):
        case=example();certificate=allocate(case);case["resources"][0]["capacity"]+=1
        self.assertFalse(verify_certificate(case,certificate)["valid"])


if __name__=="__main__":unittest.main()
