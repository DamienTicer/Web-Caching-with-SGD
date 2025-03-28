import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the caching results from JSON file
with open("cache_results.json", "r") as f:
    cache_results = json.load(f)

# Load processed request dataset
df = pd.read_csv("processed_request_data.csv")

# Compute cache hit rate for each method
def compute_cache_hit_rate(cache, df):
    total_requests = df["frequency"].sum()
    hits = df[df["resource"].isin(cache)]["frequency"].sum()
    return hits / total_requests * 100  # Convert to percentage

# Compute latency reduction for each method
def compute_latency_reduction(cache, df):
    total_latency_without_cache = (df["latency"] * df["frequency"]).sum()
    cached_df = df[df["resource"].isin(cache)]
    total_latency_with_cache = (cached_df["latency"] * cached_df["frequency"]).sum()
    return ((total_latency_without_cache - total_latency_with_cache) / total_latency_without_cache) * 100

# Compute performance metrics
metrics = {}
for method, cache in cache_results.items():
    metrics[method] = {
        "Cache Hit Rate (%)": compute_cache_hit_rate(cache, df),
        "Latency Reduction (%)": compute_latency_reduction(cache, df),
        "Cache Size (KB)": df[df["resource"].isin(cache)]["size"].sum()
    }

# Convert metrics to DataFrame for visualization
metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
metrics_df.to_csv("performance_metrics.csv")
print("Performance metrics saved to performance_metrics.csv")

# Print metrics table
print("\nPerformance Metrics:")
print(metrics_df)

# Set dark theme style globally
plt.style.use('dark_background')

# Visualization: Cache Hit Rate
plt.figure(figsize=(8,5))
plt.bar(metrics.keys(), metrics_df["Cache Hit Rate (%)"], color=["blue", "green", "red", "purple"])
plt.xlabel("Caching Method")
plt.ylabel("Cache Hit Rate (%)")
plt.title("Cache Hit Rate Comparison")
plt.savefig("cache_hit_rate_comparison.png")
plt.show()

# Visualization: Latency Reduction
plt.figure(figsize=(8,5))
plt.bar(metrics.keys(), metrics_df["Latency Reduction (%)"], color=["blue", "green", "red", "purple"])
plt.xlabel("Caching Method")
plt.ylabel("Latency Reduction (%)")
plt.title("Latency Reduction Comparison")
plt.savefig("latency_reduction_comparison.png")
plt.show()