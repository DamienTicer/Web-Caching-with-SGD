import subprocess
import time
import pandas as pd
from tqdm import tqdm
import signal
import os

# Number of iterations
NUM_ITERATIONS = 100

# Directories
os.makedirs("result_data", exist_ok=True)
os.makedirs("result_visuals", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("interim_data", exist_ok=True)

# File paths
METRICS_FILE = "result_data/cumulative_performance_metrics.csv"
AVERAGE_FILE = "result_data/average_performance_metrics.csv"
COMPREHENSIVE_FILE = "logs/comprehensive_metrics.txt"
LOG_FILE = "logs/flask_server.log"

# Function to run a Python script
def run_script(script_name):
    result = subprocess.run(["python", script_name])
    if result.returncode != 0:
        print(f"Error running {script_name}")
    else:
        print(f"Finished {script_name}")

# Function to append metrics
def append_metrics(iteration):
    metrics_df = pd.read_csv("result_data/performance_metrics.csv")
    metrics_df.insert(0, "Iteration", iteration)
    with open(METRICS_FILE, "a") as f:
        metrics_df.to_csv(f, header=f.tell() == 0, index=False)

# Function to calculate averages
def calculate_average():
    df = pd.read_csv(METRICS_FILE)
    avg_df = df.groupby("Method").mean().reset_index()
    avg_df.to_csv(AVERAGE_FILE, index=False)

# ---- Clear comprehensive_metrics.txt ----
with open(COMPREHENSIVE_FILE, "w") as f:
    f.write("")

# Start Flask server in background and redirect output to log file
with open(LOG_FILE, "w") as log_file:
    server_process = subprocess.Popen(
        ["python", "server.py"],
        stdout=log_file,
        stderr=log_file
    )

# Give server time to start
time.sleep(2)

try:
    for i in tqdm(range(1, NUM_ITERATIONS + 1), desc="Pipeline Execution"):
        run_script("simulate_requests.py")
        run_script("data_preprocessing.py")
        run_script("sgd_cache_optimizer.py")
        run_script("cache_baselines.py")
        run_script("analyze_results.py")
        append_metrics(i)

    calculate_average()
    print("All iterations completed. Average metrics saved.")

except Exception as e:
    print(f"Pipeline failed: {e}")

finally:
    server_process.send_signal(signal.SIGTERM)
    print("Flask server stopped.")