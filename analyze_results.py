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
CACHE_CAPACITY_KB = df['size'].sum() * 0.2  # Example: 20% of total dataset size

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

# Global dark theme style
plt.style.use('dark_background')
methods = list(metrics.keys())

# Cache Hit Rate Comparison
plt.figure(figsize=(10, 6))
plt.plot(methods, metrics_df["Cache Hit Rate (%)"], marker='o', linestyle='-', color='cyan')
plt.xlabel("Caching Method")
plt.ylabel("Cache Hit Rate (%)")
plt.title("Cache Hit Rate Comparison")
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig("result_visuals/cache_hit_rate_comparison.png")
plt.close()

# Latency Reduction Comparison
plt.figure(figsize=(10, 6))
plt.plot(methods, metrics_df["Latency Reduction (%)"], marker='o', linestyle='-', color='lime')
plt.xlabel("Caching Method")
plt.ylabel("Latency Reduction (%)")
plt.title("Latency Reduction Comparison")
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig("result_visuals/latency_reduction_comparison.png")
plt.close()

# Cache Usage Comparison
plt.figure(figsize=(10, 6))
plt.plot(methods, metrics_df["Cache Usage (KB)"], marker='o', linestyle='-', color='magenta', label='Cache Usage (KB)')
plt.axhline(y=CACHE_CAPACITY_KB, color='yellow', linestyle='--', linewidth=1.5, label=f'Max Cache Size ({CACHE_CAPACITY_KB:.1f} KB)')
for method in methods:
    plt.text(method, metrics_df.loc[method, "Cache Usage (KB)"] + 500, 
             f'{metrics_df.loc[method, "Cache Usage (KB)"]:.1f} KB',
             color='white', ha='center')

plt.xlabel("Caching Method")
plt.ylabel("Cache Usage (KB)")
plt.title("Cache Usage Comparison")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig("result_visuals/cache_usage_comparison.png")
plt.close()

print("Performance metrics and graphs saved.")