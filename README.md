# Comparing Knapsack-Based Stochastic Gradient Descent Approach To Typical Web Caching Methods

## 📄 Project Summary

This project evaluates and compares the effectiveness of a **Knapsack-Based Stochastic Gradient Descent (SGD) Approach** to traditional web caching methods such as **LRU (Least Recently Used)**, **LFU (Least Frequently Used)**, and **Greedy Knapsack** strategies.

The pipeline simulates web requests, applies different caching algorithms, records cache hit rates, latency reduction, and cache usage, then summarizes and visualizes the results.

---

## 📂 Project Structure Overview

```
├── interim_data/           # Temporary and intermediate data files
│   ├── request_data.csv
│   ├── processed_request_data.csv
│   ├── optimized_cache_selection.csv
│   ├── cache_results.json
│   └── web_resources.json
│
├── logs/                   # Logs and detailed iteration outputs
│   ├── flask_server.log
│   ├── cache_baselines_output.txt
│   └── comprehensive_metrics.txt
│
├── result_data/            # Processed data summaries
│   ├── cumulative_performance_metrics.csv
│   └── average_performance_metrics.csv
│
├── result_visuals/         # Visual outputs of analysis
│   ├── cache_usage_percentage_iterations.png
│   ├── latency_reduction_iterations.png
│   └── cache_hit_rate_iterations.png
│
├── server.py               # Flask server to simulate content requests
├── simulate_requests.py    # Generates random web requests and logs them
├── data_preprocessing.py   # Processes request data (assigns size/latency)
├── sgd_cache_optimizer.py  # Applies SGD-based caching strategy
├── cache_baselines.py      # Runs baseline caching strategies
├── analyze_results.py      # Analyzes single iteration results
├── metric_summary_analysis.py # Aggregates and visualizes metrics over all iterations
└── pipeline_automation.py  # Full pipeline to automate the entire process
```

---

## ⚙️ Dependencies Installation

Ensure you have **Python 3.9+** installed.

Install required packages:

```
py -m pip install flask numpy pandas matplotlib scikit-learn redis tqdm requests
```

---

## ▶️ Running the Full Pipeline

To run the entire automated process:

```bash
py pipeline_automation.py
```

Once the pipeline completes, execute the summary analysis:

```bash
py metric_summary_analysis.py
```

This will generate cumulative metrics, average metrics, and visualizations under `result_data/` and `result_visuals/`.

---

## 🔄 Running Individual Components (Optional)

If you want to run each script manually, execute them in this order:

```bash
py server.py               # Run Flask server in separate terminal
py simulate_requests.py    # Simulate request data
py data_preprocessing.py   # Assign size and latency to requests
py sgd_cache_optimizer.py  # Optimize cache using SGD
py cache_baselines.py      # Apply baseline caching methods
py analyze_results.py      # Analyze current iteration
py metric_summary_analysis.py # Summarize all iterations
```

---

## 📌 Notes
- `pipeline_automation.py` will automatically clean `logs/comprehensive_metrics.txt` at the start.
- All logs, data files, and result images will be organized into their respective folders.
- Each iteration result is appended to cumulative metrics and averaged at the end.