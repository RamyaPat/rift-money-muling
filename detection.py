import networkx as nx
import pandas as pd
from collections import defaultdict
from datetime import timedelta
import time

def run_detection(df, start_ring_counter=1):
    start_time = time.time()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )
    df = df.dropna(subset=["timestamp"])
    if len(df) > 7000:
        df = df.head(7000)

    G = nx.from_pandas_edgelist(
        df,
        source="sender_id",
        target="receiver_id",
        create_using=nx.DiGraph()
    )

    suspicious_accounts = []
    fraud_rings = []

    account_scores = defaultdict(float)
    account_patterns = defaultdict(list)
    account_ring = {}

    ring_counter = start_ring_counter

    # 1️⃣ CYCLE DETECTION
    cycles = []
    for cycle in nx.simple_cycles(G):
        if 3 <= len(cycle) <= 5:
            cycles.append(cycle)
        if len(cycles) > 50:
            break

    for cycle in cycles:
        ring_id = f"RING_{ring_counter:03d}"
        ring_counter += 1
        for acc in cycle:
            account_scores[acc] += 40
            account_patterns[acc].append("cycle")
            account_ring[acc] = ring_id
        fraud_rings.append({
            "ring_id": ring_id,
            "member_accounts": cycle,
            "pattern_type": "cycle"
        })

    # 2️⃣ FAN-IN / FAN-OUT (Smurfing)
    grouped_receiver = df.groupby("receiver_id")
    grouped_sender = df.groupby("sender_id")

    # FAN-IN
    for receiver, group in grouped_receiver:
        if len(group) >= 10 and (group["timestamp"].max() - group["timestamp"].min()) <= timedelta(hours=72):
            ring_id = f"RING_{ring_counter:03d}"
            ring_counter += 1
            members = list(group["sender_id"].unique()) + [receiver]
            for acc in members:
                account_scores[acc] += 30
                account_patterns[acc].append("fan_in")
                account_ring[acc] = ring_id
            fraud_rings.append({
                "ring_id": ring_id,
                "member_accounts": members,
                "pattern_type": "fan_in"
            })

    # FAN-OUT
    for sender, group in grouped_sender:
        if len(group) >= 10 and (group["timestamp"].max() - group["timestamp"].min()) <= timedelta(hours=72):
            ring_id = f"RING_{ring_counter:03d}"
            ring_counter += 1
            members = [sender] + list(group["receiver_id"].unique())
            for acc in members:
                account_scores[acc] += 30
                account_patterns[acc].append("fan_out")
                account_ring[acc] = ring_id
            fraud_rings.append({
                "ring_id": ring_id,
                "member_accounts": members,
                "pattern_type": "fan_out"
            })

    # 3️⃣ SHELL CHAINS
    tx_counts = df["sender_id"].value_counts().to_dict()
    candidate_nodes = [n for n in G.nodes if tx_counts.get(n, 0) <= 5]

    for source in candidate_nodes:
        for neighbor in G.successors(source):
            for next_node in G.successors(neighbor):
                if next_node != source:
                    path = [source, neighbor, next_node]
                    if all(1 <= tx_counts.get(n, 0) <= 3 for n in path):
                        ring_id = f"RING_{ring_counter:03d}"
                        ring_counter += 1
                        for acc in path:
                            account_scores[acc] += 25
                            account_patterns[acc].append("shell_chain")
                            account_ring[acc] = ring_id
                        fraud_rings.append({
                            "ring_id": ring_id,
                            "member_accounts": path,
                            "pattern_type": "shell_chain"
                        })

    # 4️⃣ HIGH VELOCITY
    for sender, group in grouped_sender:
        if len(group) >= 5 and (group["timestamp"].max() - group["timestamp"].min()) <= timedelta(hours=24):
            account_scores[sender] += 15
            account_patterns[sender].append("high_velocity")

    # BUILD SUSPICIOUS LIST
    for acc, score in account_scores.items():
        suspicious_accounts.append({
            "account_id": acc,
            "suspicion_score": float(max(0, min(100, score))),
            "detected_patterns": account_patterns[acc],
            "ring_id": account_ring.get(acc, "")
        })

    suspicious_accounts.sort(key=lambda x: x["suspicion_score"], reverse=True)

    # GRAPH DATA
    suspicious_set = set(a["account_id"] for a in suspicious_accounts)
    nodes = [{"id": node, "suspicious": node in suspicious_set, "ring_id": account_ring.get(node, "")} for node in G.nodes]
    edges = [{"source": u, "target": v} for u, v in G.edges]

    processing_time = round(time.time() - start_time, 3)

    return {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": fraud_rings,
        "graph": {"nodes": nodes, "edges": edges},
        "summary": {
            "total_accounts_analyzed": len(G.nodes),
            "suspicious_accounts_flagged": len(suspicious_accounts),
            "fraud_rings_detected": len(fraud_rings),
            "processing_time_seconds": processing_time
        },
        "next_ring_counter": ring_counter  # for continuing numbering across files
    }

# ===========================
# MULTI-FILE HANDLER
# ===========================
def run_multiple_files(file_list):
    all_results = {}
    ring_counter = 1
    for f in file_list:
        df = pd.read_csv(f)
        result = run_detection(df, start_ring_counter=ring_counter)
        all_results[f] = result
        ring_counter = result["next_ring_counter"]
    return all_results
