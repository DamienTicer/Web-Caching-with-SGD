# Comparing Knapsack-Based Stochastic Gradient Descent Approach To Typical Web Caching Methods

## Dependency Installation

# Run the following commands:
```
py -m pip install flask numpy pandas matplotlib scikit-learn redis
py -m pip install tqdm
py -m pip install requests
```

## Test Individual Features:

1. Run the server with this command:
`py server.py`

2. Run Simulated traffic:
`py simulate_requests.py`

3. Load and preview data:
`py data_preprocessing.py`

4. SGD Cache optimizer:
`py sgd_cache_optimizer.py`

5. Cache baselines:
`py cache_baselines.py`

6. Analyze results:
`py analyze_results.py`

7. Analyze average results:
`py metric_summary_analysis.py`

## Run Overall Experiment:
1. `py pipeline_automation.py`
2. `py metric_summary_analysis.py`