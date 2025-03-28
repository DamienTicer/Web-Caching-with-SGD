import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load caching results from JSON file
with open("cache_results.json", "r") as f:
    cache_results = json.load(f)

# Load processed request dataset
df = pd.read_csv("processed_request_data.csv")

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
breakdown_lines = []

for method, cache in cache_results.items():
    cache_df = df[df["resource"].isin(cache)]
    cache_usage = cache_df["size"].sum()

    metrics[method] = {
        "Cache Hit Rate (%)": compute_cache_hit_rate(cache, df),
        "Latency Reduction (%)": compute_latency_reduction(cache, df),
        "Cache Usage (KB)": cache_usage,
        "Max Cache Size (KB)": CACHE_CAPACITY_KB
    }

    # Add detailed breakdown to log
    breakdown_lines.append(f"Method: {method}")
    breakdown_lines.append("Resources Cached (resource: size KB):")
    for _, row in cache_df.iterrows():
        breakdown_lines.append(f"  {row['resource']}: {row['size']} KB")
    breakdown_lines.append(f"Total Cache Usage: {cache_usage:.2f} KB")
    breakdown_lines.append("\n")

# Convert metrics to DataFrame and save
metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
metrics_df.to_csv("performance_metrics.csv")

# Save comprehensive metrics table to a separate file
with open("comprehensive_metrics.txt", "w") as file:
    file.write(metrics_df.to_string())

# Save cache usage breakdown
with open("cache_usage_breakdown.txt", "w") as f:
    f.write("\n".join(breakdown_lines))

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
plt.savefig("cache_hit_rate_comparison.png")
plt.show()

# Latency Reduction Comparison
plt.figure(figsize=(10, 6))
plt.plot(methods, metrics_df["Latency Reduction (%)"], marker='o', linestyle='-', color='lime')
plt.xlabel("Caching Method")
plt.ylabel("Latency Reduction (%)")
plt.title("Latency Reduction Comparison")
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig("latency_reduction_comparison.png")
plt.show()

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
plt.savefig("cache_usage_comparison.png")
plt.show()