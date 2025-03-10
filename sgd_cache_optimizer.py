import pandas as pd
import numpy as np

# Load the normalized request data
df = pd.read_csv("normalized_request_data.csv")

# Define cache capacity dynamically based on dataset size (20% of total size)
TOTAL_DATASET_SIZE = df["size"].sum()
CACHE_CAPACITY = int(TOTAL_DATASET_SIZE * 0.2)  # 20% of dataset size

print(f"Total dataset size: {TOTAL_DATASET_SIZE} KB")
print(f"New cache capacity: {CACHE_CAPACITY} KB")

# Learning rate and momentum for SGD updates
LEARNING_RATE = 0.01
MOMENTUM = 0.9  # Momentum coefficient

# Adaptive penalty (lambda) for enforcing cache size constraints
LAMBDA = 5  # Initial penalty

# Weighting factors for hit rate and latency optimization
ALPHA = 1.0  # Cache hit rate importance
BETA = 0.5   # Latency penalty importance
GAMMA = 0.5  # Bonus for increasing cache size usage

# Initialize cache selection probabilities randomly
df["cache_prob"] = np.random.uniform(0.2, 0.8, len(df))  # Between 20% and 80%

# Initialize momentum for velocity-based SGD updates
velocity = np.zeros(len(df))

# Sigmoid function for probability mapping
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Loss function: maximize cache hit rate, minimize latency, enforce cache constraints
def compute_loss(df):
    return - (
        ALPHA * (df["frequency"] * df["cache_prob"]).sum()
        - BETA * (df["latency"] * (1 - df["cache_prob"])).sum()
        + GAMMA * df["cache_prob"].sum()
    ) + LAMBDA * max(0, df["size"].dot(df["cache_prob"]) - CACHE_CAPACITY)

# Adaptive penalty function (dynamically adjusts lambda)
def adjust_lambda(df):
    global LAMBDA
    cache_usage = df["size"].dot(df["cache_prob"])
    if cache_usage > CACHE_CAPACITY * 0.9:
        LAMBDA *= 1.1  # Increase penalty when cache is near full
    elif cache_usage < CACHE_CAPACITY * 0.7:
        LAMBDA *= 0.9  # Decrease penalty when cache is under-utilized

# SGD update step with momentum
def update_cache_probabilities(df):
    global LAMBDA
    for _ in range(500):  # Increased iterations for better convergence
        adjust_lambda(df)  # Adjust lambda dynamically

        # Compute gradient based on frequency, latency, and cache constraint
        df["gradient"] = ALPHA * df["frequency"] - BETA * df["latency"] - LAMBDA * df["size"]

        # Apply momentum-based update
        global velocity
        velocity = MOMENTUM * velocity + (1 - MOMENTUM) * df["gradient"]
        df["cache_prob"] += LEARNING_RATE * velocity

        # Apply sigmoid activation to keep values between 0 and 1
        df["cache_prob"] = sigmoid(df["cache_prob"])

        # Enforce cache capacity constraint by reducing probabilities if needed
        while df["size"].dot(df["cache_prob"]) > CACHE_CAPACITY:
            df.loc[df["cache_prob"].idxmax(), "cache_prob"] *= 0.9  # Reduce highest probability

    return df

# Run optimization
df = update_cache_probabilities(df)

# Select final cached items based on probabilities > 0.5 threshold
df["cached"] = (df["cache_prob"] > 0.5).astype(int)

# Save the optimized caching strategy
df.to_csv("optimized_cache_selection.csv", index=False)
print("Optimized cache selection saved to optimized_cache_selection.csv")