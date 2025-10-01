import pandas as pd
import heapq
from collections import deque
import json
import os

# Create folders
os.makedirs("result_data", exist_ok=True)
os.makedirs("result_visuals", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("interim_data", exist_ok=True)

# Open output file for writing logs
output_file = open("logs/cache_baselines_output.txt", "w")

# Helper function to write logs to file
def log(msg):
    output_file.write(msg + "\n")

# Load dataset
df = pd.read_csv("interim_data/processed_request_data.csv")

TOTAL_DATASET_SIZE = df["size"].sum()
CACHE_CAPACITY = int(TOTAL_DATASET_SIZE * 0.1)

log(f"Total dataset size: {TOTAL_DATASET_SIZE} KB")
log(f"New cache capacity: {CACHE_CAPACITY} KB")

# LRU Cache Implementation
def lru_caching(df):
    cache = deque()
    cache_size = 0
    cache_set = set()

    for index, row in df.iterrows():
        if row["resource"] in cache_set:
            cache.remove(row["resource"])
        elif cache_size + row["size"] <= CACHE_CAPACITY:
            cache.append(row["resource"])
            cache_set.add(row["resource"])
            cache_size += row["size"]

        if cache_size > CACHE_CAPACITY:
            removed = cache.popleft()
            cache_set.remove(removed)
            cache_size -= df[df["resource"] == removed]["size"].values[0]

    return list(cache)

# LFU Cache Implementation
def lfu_caching(df):
    cache = []
    cache_size = 0
    cache_set = set()

    df_sorted = df.sort_values(by="frequency", ascending=False)

    log("\nLFU Sorted Resources (Highest Frequency First):")
    log(df_sorted[["resource", "frequency"]].to_string(index=False))

    for index, row in df_sorted.iterrows():
        if cache_size + row["size"] <= CACHE_CAPACITY:
            cache.append(row["resource"])
            cache_set.add(row["resource"])
            cache_size += row["size"]

    return cache

# Greedy Knapsack Caching
def knapsack_caching(df):
    cache = []
    cache_size = 0
    cache_set = set()

    df["value_ratio"] = (df["frequency"] / df["size"]) * (1 / df["latency"] + 1)
    df_sorted = df.sort_values(by="value_ratio", ascending=False)

    log("\nGreedy Knapsack Sorted Resources (Highest Value-to-Size Ratio First):")
    log(df_sorted[["resource", "value_ratio"]].to_string(index=False))

    for index, row in df_sorted.iterrows():
        if cache_size + row["size"] <= CACHE_CAPACITY:
            cache.append(row["resource"])
            cache_set.add(row["resource"])
            cache_size += row["size"]

    return cache

# Execute caching methods
lru_cache = lru_caching(df)
lfu_cache = lfu_caching(df)
knapsack_cache = knapsack_caching(df)

# Load the SGD-optimized cache selection for comparison
sgd_df = pd.read_csv("interim_data/optimized_cache_selection.csv")
sgd_cache = list(sgd_df[sgd_df["cached"] == 1]["resource"])

# Save results for later analysis
results = {
    "LRU": lru_cache,
    "LFU": lfu_cache,
    "Greedy Knapsack": knapsack_cache,
    "SGD-Based": sgd_cache
}

with open("interim_data/cache_results.json", "w") as f:
    json.dump(results, f)

log("Cache comparison results saved.")

# Log cache selections for debugging
log("\nLRU Cache: " + str(lru_cache))
log("\nLFU Cache: " + str(lfu_cache))
log("\nGreedy Knapsack Cache: " + str(knapsack_cache))
log("\nSGD-Based Cache: " + str(sgd_cache))

# Close output file
output_file.close()