import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create folders
os.makedirs("result_data", exist_ok=True)
os.makedirs("result_visuals", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("interim_data", exist_ok=True)

# Load caching results from JSON file
with open("interim_data/cache_results.json", "r") as f:
    cache_results = json.load(f)

# Load processed request dataset
df = pd.read_csv("interim_data/processed_request_data.csv")

# Cache capacity (assuming this is consistent across methods, adjust if needed)
CACHE_CAPACITY_KB = df['size'].sum() * 0.1  # Example: 10% of total dataset size

# Compute cache hit rate
def compute_cache_hit_rate(cache, df):
    total_requests = df["frequency"].sum()
    hits = df[df["resource"].isin(cache)]["frequency"].sum()
    return hits / total_requests * 100

# Compute latency reduction
def compute_latency_reduction(cache, df):
    total_latency_without_cache = (df["latency"] * df["frequency"]).sum()
    cached_df = df[df["resource"].isin(cache)]
    total_latency_with_cache = (cached_df["latency"] * cached_df["frequency"]).sum()
    return ((total_latency_without_cache - total_latency_with_cache) / total_latency_without_cache) * 100

# Compute cache size usage
metrics = {}
for method, cache in cache_results.items():
    metrics[method] = {
        "Cache Hit Rate (%)": compute_cache_hit_rate(cache, df),
        "Latency Reduction (%)": compute_latency_reduction(cache, df),
        "Cache Usage (KB)": df[df["resource"].isin(cache)]["size"].sum(),
        "Max Cache Size (KB)": CACHE_CAPACITY_KB
    }

# Convert metrics to DataFrame and save
metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
metrics_df.to_csv("result_data/performance_metrics.csv")

# Save comprehensive metrics table to a separate file
with open("logs/comprehensive_metrics.txt", "a") as file:
    file.write("--- Iteration ---\n")
    file.write(metrics_df.to_string())
    file.write("\n\n")

print("Performance metrics saved without comparison plots.")