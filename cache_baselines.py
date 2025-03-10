import pandas as pd
import heapq
from collections import deque

df = pd.read_csv("processed_request_data.csv")  # Load dataset

TOTAL_DATASET_SIZE = df["size"].sum()  # Sum of all file sizes
CACHE_CAPACITY = int(TOTAL_DATASET_SIZE * 0.2)  # Set cache to 20% of total size

print(f"Total dataset size: {TOTAL_DATASET_SIZE} KB")
print(f"New cache capacity: {CACHE_CAPACITY} KB")

# LRU Cache Implementation
def lru_caching(df):
    cache = deque()  # LRU uses a queue for tracking order of use
    cache_size = 0
    cache_set = set()

    for index, row in df.iterrows():
        if row["resource"] in cache_set:
            cache.remove(row["resource"])  # Move accessed item to most recent
        elif cache_size + row["size"] <= CACHE_CAPACITY:
            cache.append(row["resource"])
            cache_set.add(row["resource"])
            cache_size += row["size"]

        if cache_size > CACHE_CAPACITY:
            removed = cache.popleft()  # Evict the least recently used item
            cache_set.remove(removed)
            cache_size -= df[df["resource"] == removed]["size"].values[0]

    return list(cache)

# LFU Cache Implementation
def lfu_caching(df):
    cache = []
    cache_size = 0
    cache_set = set()

    # Sort by frequency (highest first)
    df = df.sort_values(by="frequency", ascending=False)

    print("\nLFU Sorted Resources (Highest Frequency First):")
    print(df[["resource", "frequency"]].sort_values(by="frequency", ascending=False))

    for index, row in df.iterrows():
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

    # Compute value-to-size ratio and sort by it
    df["value_ratio"] = (df["frequency"] / df["size"]) * (1/ df["latency"] + 1)
    df = df.sort_values(by="value_ratio", ascending=False)

    print("\nGreedy Knapsack Sorted Resources (Highest Value-to-Size Ratio First):")
    print(df[["resource", "value_ratio"]].sort_values(by="value_ratio", ascending=False))

    for index, row in df.iterrows():
        if cache_size + row["size"] <= CACHE_CAPACITY:
            cache.append(row["resource"])
            cache_set.add(row["resource"])
            cache_size += row["size"]
    
    return cache

# Run all caching methods
lru_cache = lru_caching(df)
lfu_cache = lfu_caching(df)
knapsack_cache = knapsack_caching(df)

# Load the SGD-optimized cache selection for comparison
sgd_df = pd.read_csv("optimized_cache_selection.csv")
sgd_cache = list(sgd_df[sgd_df["cached"] == 1]["resource"])

# Save results for later analysis
results = {
    "LRU": lru_cache,
    "LFU": lfu_cache,
    "Greedy Knapsack": knapsack_cache,
    "SGD-Based": sgd_cache
}

import json
with open("cache_results.json", "w") as f:
    json.dump(results, f)

print("Cache comparison results saved.")

# Print the cache selections for debugging
print("\nLRU Cache:", lru_cache)
print("\nLFU Cache:", lfu_cache)
print("\nGreedy Knapsack Cache:", knapsack_cache)
print("\nSGD-Based Cache:", sgd_cache)