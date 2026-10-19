from collections import deque
from copy import deepcopy
import hashlib
import itertools
import json


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def validate(case):
    if not isinstance(case,dict):raise ValueError("invalid_case")
    for key,maximum in (("resources",14),("demands",12),("outages",12),("upgrades",10)):
        values=case.get(key,[])
        if not isinstance(values,list) or len(values)>maximum or any(not isinstance(v,dict) for v in values):raise ValueError("invalid_collection")
        ids=[v.get("id") for v in values]
        if any(not isinstance(v,str) or not v or len(v)>64 for v in ids) or len(set(ids))!=len(ids):raise ValueError("invalid_ids")
    if not case.get("resources") or not case.get("demands"):raise ValueError("invalid_empty_network")
    demands={d["id"]:d for d in case["demands"]};resources={r["id"]:r for r in case["resources"]}
    for demand in demands.values():
        if type(demand.get("need")) is not int or not 1<=demand["need"]<=1000:raise ValueError("invalid_demand")
    def resource_valid(resource):
        return isinstance(resource,dict) and isinstance(resource.get("id"),str) and bool(resource["id"]) and type(resource.get("capacity")) is int and 0<=resource["capacity"]<=1000 and isinstance(resource.get("serves"),list) and len(set(resource["serves"]))==len(resource["serves"]) and all(d in demands for d in resource["serves"])
    for resource in resources.values():
        if not resource_valid(resource):raise ValueError("invalid_resource")
    outages={o["id"]:o for o in case.get("outages",[])}
    for outage in outages.values():
        if type(outage.get("cost")) is not int or not 1<=outage["cost"]<=10 or not isinstance(outage.get("disables"),list) or any(r not in resources for r in outage["disables"]):raise ValueError("invalid_outage")
    for upgrade in case.get("upgrades",[]):
        if type(upgrade.get("cost")) is not int or not 1<=upgrade["cost"]<=100:raise ValueError("invalid_upgrade_cost")
        if not isinstance(upgrade.get("increase",{}),dict) or any(r not in resources or type(v) is not int or not 0<=v<=1000 for r,v in upgrade.get("increase",{}).items()):raise ValueError("invalid_increase")
        if "add" in upgrade and (not resource_valid(upgrade["add"]) or upgrade["add"]["id"] in resources):raise ValueError("invalid_upgrade_resource")
        if not isinstance(upgrade.get("exposed_to",[]),list) or any(o not in outages for o in upgrade.get("exposed_to",[])):raise ValueError("invalid_upgrade_exposure")
    return resources,demands


def graph(case,disabled):
    resources,demands=validate(case)
    if not set(disabled)<=set(resources):raise ValueError("invalid_disabled_resource")
    total=sum(d["need"] for d in demands.values())
    infinity=total+sum(r["capacity"] for r in resources.values())+1
    edges=[]
    for key,resource in resources.items():
        edges.append(("source","resource:"+key,0 if key in disabled else resource["capacity"]))
        edges.extend(("resource:"+key,"demand:"+d,infinity) for d in resource["serves"])
    edges.extend(("demand:"+key,"sink",d["need"]) for key,d in demands.items())
    return edges


def allocate(case,disabled=()):
    resources,demands=validate(case)
    edges=graph(case,disabled)
    adjacency={}
    original=[]
    for start,end,capacity in edges:
        adjacency.setdefault(start,[]);adjacency.setdefault(end,[])
        forward=[end,len(adjacency[end]),capacity];backward=[start,len(adjacency[start]),0]
        adjacency[start].append(forward);adjacency[end].append(backward);original.append((start,forward,capacity))
    flow=0
    while True:
        levels={"source":0};queue=deque(["source"])
        while queue:
            node=queue.popleft()
            for end,_,capacity in adjacency[node]:
                if capacity>0 and end not in levels:levels[end]=levels[node]+1;queue.append(end)
        if "sink" not in levels:break
        cursor={node:0 for node in adjacency}
        def send(node,amount):
            if node=="sink":return amount
            while cursor[node]<len(adjacency[node]):
                edge=adjacency[node][cursor[node]];end,reverse,capacity=edge
                if capacity>0 and levels.get(end)==levels[node]+1:
                    sent=send(end,min(amount,capacity))
                    if sent:edge[2]-=sent;adjacency[end][reverse][2]+=sent;return sent
                cursor[node]+=1
            return 0
        while True:
            amount=send("source",10**9)
            if not amount:break
            flow+=amount
    reachable={"source"};queue=deque(["source"])
    while queue:
        node=queue.popleft()
        for end,_,capacity in adjacency[node]:
            if capacity>0 and end not in reachable:reachable.add(end);queue.append(end)
    allocations=[{"resource":start.removeprefix("resource:"),"demand":edge[0].removeprefix("demand:"),"units":capacity-edge[2]}
                 for start,edge,capacity in original if start.startswith("resource:") and edge[0].startswith("demand:") and capacity-edge[2]>0]
    cut=[{"from":a,"to":b,"capacity":c} for a,b,c in edges if a in reachable and b not in reachable]
    delivered={key:sum(a["units"] for a in allocations if a["demand"]==key) for key in demands}
    result={"case_sha256":digest(case),"disabled":sorted(disabled),"delivered_units":flow,
            "total_need":sum(d["need"] for d in demands.values()),"allocations":allocations,
            "unmet":{key:d["need"]-delivered[key] for key,d in demands.items()},
            "source_side_cut":sorted(reachable),"cut_edges":cut,"cut_capacity":sum(e["capacity"] for e in cut)}
    result["certificate"]=verify_certificate(case,result)
    if not result["certificate"]["valid"]:raise RuntimeError("independent_flow_certificate_failed")
    return result


def verify_certificate(case,certificate):
    """Check primal feasibility and dual cut equality without running max-flow."""
    resources,demands=validate(case)
    if not isinstance(certificate,dict):return {"valid":False,"errors":["invalid_certificate"]}
    errors=[]
    disabled=certificate.get("disabled",[])
    if not isinstance(disabled,list) or any(k not in resources for k in disabled):return {"valid":False,"errors":["disabled_resource"]}
    allocations=certificate.get("allocations",[])
    if not isinstance(allocations,list) or any(not isinstance(a,dict) for a in allocations):return {"valid":False,"errors":["invalid_allocation"]}
    for allocation in allocations:
        r,d,n=allocation.get("resource"),allocation.get("demand"),allocation.get("units")
        if r not in resources or d not in demands or type(n) is not int or n<0 or d not in resources[r]["serves"]:return {"valid":False,"errors":["invalid_allocation"]}
    for key,r in resources.items():
        if sum(a["units"] for a in allocations if a["resource"]==key)>(0 if key in disabled else r["capacity"]):errors.append("resource_capacity")
    for key,d in demands.items():
        if sum(a["units"] for a in allocations if a["demand"]==key)>d["need"]:errors.append("demand_capacity")
    total=sum(a["units"] for a in allocations)
    if certificate.get("total_need")!=sum(d["need"] for d in demands.values()):errors.append("total_need")
    if certificate.get("unmet")!={k:d["need"]-sum(a["units"] for a in allocations if a["demand"]==k) for k,d in demands.items()}:errors.append("unmet_metadata")
    edges=graph(case,disabled)
    side=set(certificate.get("source_side_cut",[]))
    all_nodes={n for a,b,_ in edges for n in (a,b)}
    if "source" not in side or "sink" in side or not side<=all_nodes:errors.append("invalid_cut_partition")
    cut=sum(c for a,b,c in edges if a in side and b not in side)
    expected_cut=[{"from":a,"to":b,"capacity":c} for a,b,c in edges if a in side and b not in side]
    if certificate.get("cut_edges")!=expected_cut:errors.append("cut_edges")
    if total!=cut or total!=certificate.get("delivered_units") or cut!=certificate.get("cut_capacity"):errors.append("primal_dual_gap")
    if certificate.get("case_sha256")!=digest(case):errors.append("case_fingerprint")
    return {"valid":not errors,"errors":errors,"feasible_allocation_units":total,"independent_cut_capacity":cut,
            "maximum_flow_proven":not errors,"scope":"supplied_integer_bipartite_capacity_model"}


def outage_sweep(case,budget=1):
    validate(case)
    if type(budget) is not int or not 0<=budget<=3:raise ValueError("invalid_outage_budget")
    events=case.get("outages",[]);reports=[];cache={}
    for count in range(min(len(events),budget)+1):
        for selected in itertools.combinations(events,count):
            cost=sum(e["cost"] for e in selected)
            if cost>budget:continue
            disabled=tuple(sorted({r for e in selected for r in e["disables"]}))
            if disabled not in cache:cache[disabled]=allocate(case,disabled)
            allocation=cache[disabled]
            reports.append({"events":[e["id"] for e in selected],"event_cost":cost,"shortfall":allocation["total_need"]-allocation["delivered_units"],"flow":allocation})
    worst=min(reports,key=lambda r:(-r["shortfall"],r["event_cost"],len(r["events"]),r["events"]))
    failing=[r for r in reports if r["shortfall"]>0]
    minimal=[r["events"] for r in failing if not any(set(other["events"])<set(r["events"]) for other in failing)]
    return {"scenarios_checked":len(reports),"distinct_disabled_sets":len(cache),"budget":budget,"worst":worst,
            "minimal_failing_event_sets":minimal,"all_scenarios":reports,"exhaustive_within_catalog_and_budget":True}


def upgraded(case,upgrade):
    result=deepcopy(case)
    result["upgrades"]=[]
    for resource in result["resources"]:resource["capacity"]+=upgrade.get("increase",{}).get(resource["id"],0)
    if "add" in upgrade:
        result["resources"].append(deepcopy(upgrade["add"]))
        for event in result.get("outages",[]):
            if event["id"] in upgrade.get("exposed_to",[]):event["disables"].append(upgrade["add"]["id"])
    validate(result)
    return result


def analyze(case,outage_budget=1,investment_budget=2):
    validate(case)
    if type(investment_budget) is not int or not 0<=investment_budget<=100:raise ValueError("invalid_investment_budget")
    baseline=outage_sweep(case,outage_budget)
    comparisons=[]
    for upgrade in case.get("upgrades",[]):
        if upgrade["cost"]<=investment_budget:
            modified=upgraded(case,upgrade);sweep=outage_sweep(modified,outage_budget)
            comparisons.append({"upgrade":upgrade["id"],"cost":upgrade["cost"],"worst_shortfall":sweep["worst"]["shortfall"],"worst_events":sweep["worst"]["events"],"worst_flow_certificate":sweep["worst"]["flow"],"modified_case":modified})
    best=min(comparisons,key=lambda r:(r["worst_shortfall"],r["cost"],r["upgrade"])) if comparisons else None
    return {"source_case":deepcopy(case),"baseline":baseline,"upgrade_comparisons":comparisons,"best_single_catalog_upgrade":best["upgrade"] if best and best["worst_shortfall"]<baseline["worst"]["shortfall"] else None,
            "investment_budget":investment_budget,"model":"synthetic_exercise_integer_capacity_model","dispatch_performed":False,"outage_probabilities_estimated":False}
