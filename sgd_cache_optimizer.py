import pandas as pd
import numpy as np
from tqdm import tqdm

# Load dataset
df = pd.read_csv("processed_request_data.csv")

TOTAL_DATASET_SIZE = df["size"].sum()  # Sum of all file sizes
CACHE_CAPACITY = int(TOTAL_DATASET_SIZE * 0.2)  # Set cache to 20% of total size

print(f"Total dataset size: {TOTAL_DATASET_SIZE} KB")
print(f"New cache capacity: {CACHE_CAPACITY} KB")

# Hyperparameters
ETA_INITIAL = 0.0005
ADJUSTMENT_FACTOR = 0.01
LAMBDA = 10
MU = 0.01  # Capacity violation penalty
MIN_LR = 1e-5
MAX_LR = 0.02
MARGIN = 0.10
MAX_RETRIES = 75
SGD_ITERATIONS = 500
THRESHOLD = 0.3
THETA_CLIP = 10  # Lowered clipping for smoother behavior

# Margin boundaries
lower_bound = CACHE_CAPACITY * (1 - MARGIN)
upper_bound = CACHE_CAPACITY

# Initialize cache selection probabilities
df["cache_prob"] = np.random.uniform(0.6, 0.9, len(df))

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Loss function with capacity penalty
def compute_loss(df):
    capacity_violation = max(0, df["size"].dot(df["cache_prob"]) - CACHE_CAPACITY)
    return - (df["frequency"] * df["cache_prob"]).sum() + LAMBDA * capacity_violation + MU * capacity_violation

# SGD update step
def update_cache_probabilities(df, learning_rate, iterations=SGD_ITERATIONS):
    df["theta"] = np.random.uniform(-0.1, 0.1, len(df))

    for _ in range(iterations):
        df["gradient"] = df["frequency"] - LAMBDA * df["size"]
        df["theta"] += learning_rate * df["gradient"]
        df["theta"] = np.clip(df["theta"], -THETA_CLIP, THETA_CLIP)
        df["cache_prob"] = sigmoid(df["theta"])

    return df

# Projection step to enforce cache capacity
def enforce_capacity(df):
    total_usage = df["size"].dot(df["cache_prob"])
    if total_usage > CACHE_CAPACITY:
        scaling_factor = CACHE_CAPACITY / total_usage
        df["cache_prob"] *= scaling_factor
    return df

# Post-optimization cleanup step
def cleanup_cache(df):
    df = df.copy()
    df.sort_values("cache_prob", ascending=False, inplace=True)
    cumulative_size = 0
    selected = []

    for index, row in df.iterrows():
        if cumulative_size + row["size"] <= CACHE_CAPACITY:
            selected.append(1)
            cumulative_size += row["size"]
        else:
            selected.append(0)

    df["cached"] = selected
    df.sort_index(inplace=True)
    return df

# Adaptive retry loop
def adaptive_retry_optimizer(df):
    learning_rate = ETA_INITIAL
    best_cache_prob = None
    best_usage = 0

    for retry in tqdm(range(1, MAX_RETRIES + 1), desc="Adaptive Retry Optimization"):
        df_copy = df.copy()
        df_copy = update_cache_probabilities(df_copy, learning_rate)

        # Enforce capacity constraint strictly
        df_copy = enforce_capacity(df_copy)

        # Cleanup and measure usage
        df_copy = cleanup_cache(df_copy)
        cache_usage = df_copy.loc[df_copy["cached"] == 1, "size"].sum()

        # Learning rate adjustment
        if cache_usage < lower_bound:
            learning_rate *= (1 + ADJUSTMENT_FACTOR)
        elif cache_usage > upper_bound:
            learning_rate *= (1 - ADJUSTMENT_FACTOR)

        learning_rate = np.clip(learning_rate, MIN_LR, MAX_LR)

        if best_usage < cache_usage <= CACHE_CAPACITY:
            best_cache_prob = df_copy["cache_prob"].copy()
            best_usage = cache_usage

        if lower_bound <= cache_usage <= upper_bound:
            break

    if best_cache_prob is not None:
        df["cache_prob"] = best_cache_prob
    else:
        df["cache_prob"] = sigmoid(df["cache_prob"])

    return df

# Run adaptive retry optimization
df = adaptive_retry_optimizer(df)

# Enforce capacity one last time (cleanup)
df = cleanup_cache(df)

# Save optimized caching strategy
df.to_csv("optimized_cache_selection.csv", index=False)
print("Optimized cache selection saved to optimized_cache_selection.csv")