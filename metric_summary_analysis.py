import pandas as pd
import matplotlib.pyplot as plt
import re

# File paths
COMPREHENSIVE_FILE = "comprehensive_metrics.txt"
CUMULATIVE_FILE = "cumulative_performance_metrics.csv"
AVERAGE_FILE = "average_performance_metrics.csv"

# Step 1: Parse comprehensive_metrics.txt
all_metrics = []
current_iteration = 0

with open(COMPREHENSIVE_FILE, "r") as f:
    for line in f:
        if "--- Iteration ---" in line:
            current_iteration += 1
        elif re.match(r"\s*(LRU|LFU|Greedy Knapsack|SGD-Based)", line):
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) == 5:
                method, chr, lr, usage, max_size = parts
                all_metrics.append({
                    "Iteration": current_iteration,
                    "Method": method,
                    "Cache Hit Rate (%)": float(chr),
                    "Latency Reduction (%)": float(lr),
                    "Cache Usage (KB)": float(usage),
                    "Max Cache Size (KB)": float(max_size)
                })

# Step 2: Create cumulative DataFrame
full_df = pd.DataFrame(all_metrics)
full_df.to_csv(CUMULATIVE_FILE, index=False)

# Step 3: Calculate average metrics
average_df = full_df.groupby("Method").mean().reset_index()
average_df.to_csv(AVERAGE_FILE, index=False)

# Step 4: Generate graphs
plt.style.use('dark_background')

# Cache Hit Rate
plt.figure(figsize=(10, 6))
for method in average_df["Method"]:
    plt.plot(full_df[full_df["Method"] == method]["Iteration"],
             full_df[full_df["Method"] == method]["Cache Hit Rate (%)"], label=method)
plt.title("Cache Hit Rate Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Cache Hit Rate (%)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("cache_hit_rate_iterations.png")
plt.close()

# Latency Reduction
plt.figure(figsize=(10, 6))
for method in average_df["Method"]:
    plt.plot(full_df[full_df["Method"] == method]["Iteration"],
             full_df[full_df["Method"] == method]["Latency Reduction (%)"], label=method)
plt.title("Latency Reduction Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Latency Reduction (%)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("latency_reduction_iterations.png")
plt.close()

# Cache Usage
plt.figure(figsize=(10, 6))
for method in average_df["Method"]:
    plt.plot(full_df[full_df["Method"] == method]["Iteration"],
             full_df[full_df["Method"] == method]["Cache Usage (KB)"], label=method)
plt.axhline(y=full_df["Max Cache Size (KB)"].mean(), color='yellow', linestyle='--', label=f"Avg Max Cache Size")
plt.title("Cache Usage Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Cache Usage (KB)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("cache_usage_iterations.png")
plt.close()

print("Summary analysis complete. CSV and graphs saved.")