import pandas as pd
import numpy as np

df = pd.read_csv("processed_request_data.csv")  # Load dataset

TOTAL_DATASET_SIZE = df["size"].sum()  # Sum of all file sizes
CACHE_CAPACITY = int(TOTAL_DATASET_SIZE * 0.2)  # Set cache to 20% of total size

print(f"Total dataset size: {TOTAL_DATASET_SIZE} KB")
print(f"New cache capacity: {CACHE_CAPACITY} KB")


# Learning rate for SGD updates
LEARNING_RATE = 0.001

# Regularization penalty to enforce cache size constraint
LAMBDA = 5

# Initialize cache selection probabilities (randomized start)
df["cache_prob"] = np.random.uniform(0.2, 0.8, len(df))  # Between 20% and 80% probability

# Sigmoid function for probability mapping
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Loss function: maximize cache hit rate while minimizing latency
def compute_loss(df):
    return - (df["frequency"] * df["cache_prob"]).sum() + LAMBDA * max(0, df["size"].dot(df["cache_prob"]) - CACHE_CAPACITY)

# SGD update step
def update_cache_probabilities(df):
    for _ in range(100):  # Run SGD for 100 iterations
        # Compute gradient of the loss function
        df["gradient"] = df["frequency"] - LAMBDA * df["size"]

        # Update cache probabilities using SGD rule
        df["cache_prob"] += LEARNING_RATE * df["gradient"]

        # Apply sigmoid activation to ensure values remain between 0 and 1
        df["cache_prob"] = sigmoid(df["cache_prob"])

        # Enforce cache capacity constraint
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