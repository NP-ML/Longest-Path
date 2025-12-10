# Longest Path Graph Benchmark

This repository implements tools to generate, analyze and (approximately) solve the Longest Simple Path problem on small graphs. It combines a C++ DP core, Python feature extraction / heuristics, and simple learned predictors.

Contents (selected)
- C++ core and helpers:
  - [`cpp_extraction/config.hpp`](cpp_extraction/config.hpp)
  - [`cpp_extraction/algorithms.cpp`](cpp_extraction/algorithms.cpp) — contains functions such as [`fill_dp_grid`](cpp_extraction/algorithms.cpp) and [`get_sccs`](cpp_extraction/algorithms.cpp)
  - runner / extraction utilities in `cpp_extraction/`
- Python code:
  - [`algorithm.py`](algorithm.py) — heuristic / greedy routines (e.g. [`path_from_kth_best_start`](algorithm.py))
  - [`top_k_paths.py`](top_k_paths.py) — top-k approximate path search ([`find_top_k_paths`](top_k_paths.py))
  - [`evaluate.py`](evaluate.py) — path-file loader and evaluation; see [`load_paths`](evaluate.py)
  - [`model/net.py`](model/net.py) — small PyTorch regressor model class [`Net`](model/net.py)
  - [`Generalisation/testing_on_generated_dataset.py`](Generalisation/testing_on_generated_dataset.py) — runs comparisons between model and greedy (contains [`run_model_pipeline`](Generalisation/testing_on_generated_dataset.py) and [`run_greedy_pipeline`](Generalisation/testing_on_generated_dataset.py))
  - misc scripts and notebooks in `model/` and `initial_method_scratched/`
- Datasets & computed results:
  - [datasets/graphs.txt](datasets/graphs.txt)
  - [computed_paths/graphs.txt](computed_paths/graphs.txt)
  - [computed_paths/longest_paths.txt](computed_paths/longest_paths.txt)
  - [computed_paths/approximate_paths.txt](computed_paths/approximate_paths.txt)
- Utilities:
  - [`graph_util/graph_generator.py`](graph_util/graph_generator.py) — random graph generator (see [`parse_existing`](graph_util/graph_generator.py))
  - `evaluate.py` — quick stats script over approximate-vs-greedy comparison ([evaluate.py](evaluate.py))
