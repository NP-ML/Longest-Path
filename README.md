

Longest Path Graph Benchmark

This project combines C++ and Python to analyze graph structure features and build a baseline model that predicts the Longest Simple Path (LSP) length in random directed and undirected graphs.

Repository Structure

* config.hpp : C++ type definitions and constants
* util.cpp : Bitmask dynamic programming for subset reachability (core for longest path)
* initial_dataset.jsonl : Example dataset of graphs and expected longest path
* initial_model_training.ipynb : Notebook for feature extraction, visualization, and baseline model
* README.md : Documentation

Overview

Implemented Components:

* Dataset handling: JSONL format (one graph per line) with Python stream loaders.
* Feature extraction: Builds NetworkX graphs and computes structural descriptors such as number of nodes, edges, density, SCC statistics, degree statistics, clustering coefficient, and DAG flag.
* Visualization: Generates sample graph figures with the reference longest path highlighted.
* Baseline model: Random forest regression that predicts the longest path length or its normalized ratio using extracted features.
* C++ core: Bitset-based dynamic programming routine that checks reachability for longest paths in small graphs (defined in util.cpp and config.hpp).

Quickstart

To run in Google Colab:

1. Upload the file initial_dataset.jsonl.
2. Open the notebook initial_model_training.ipynb.
3. Run all cells to generate feature tables and plots. The outputs are written to the folders results/ and figures/.

To run locally:

1. Clone the repository and open a terminal in its directory.
2. Install dependencies:
   pip install pandas numpy networkx matplotlib scikit-learn orjson tqdm
3. Open and run initial_model_training.ipynb using Jupyter Notebook.

To compile the C++ core (optional):

1. Use any C++17 compatible compiler:
   g++ -O2 -std=c++17 util.cpp -o util
   ./util
2. You can edit constants in config.hpp to change the graph size N.

Output
The notebook automatically creates:

* results/ : contains CSV summaries and saved model files.
* figures/ : contains histograms, scatter plots, and example graph visualizations.

Planned Extensions
(Not yet implemented)

* Neural or GNN-based predictors for longest path length.
* Learned heuristic solvers guided by the regression model.
* Automated dataset generation for larger graphs.


Keywords
graphs, longest path, subset DP, graph features, random forest, networkx, data analysis

