#include "algorithms.cpp"
#include <functional>
#include <fstream>
#include <iostream>
using namespace std;

struct longest_path_solver
{
    ofstream out;
    bool_grid dp;
    list_of_lists adj;

    longest_path_solver(string output_file) : out(output_file, ios::app) {}

    void process_graphs(string input_file) {
        ifstream in(input_file);
        int t, u, v, m;
        in >> t;
        while (t--) {
            in >> m;
            while (m--) {
                in >> u >> v;
                adj[u].push_back(v);
            }
            fill_dp_grid(adj, dp);
            int bestStart = 0, bestMask = 1, bestSize = 1;
            for(int mask = 1; mask < POW2_N; ++mask)
                for(int u = 0; u < N; ++u)
                    if(dp[u][mask]) {
                        int size = __builtin_popcount(mask);
                        if(size > bestSize) {
                            bestStart = u;
                            bestMask = mask;
                            bestSize = size;
                        }
                    }
            vector<int> path;
            path.reserve(bestSize);
            for (int i = 0; i < bestSize; i++) {
                path.push_back(bestStart);
                toggle(bestMask, bestStart);
                for (int nxt : adj[bestStart]) {
                    if (dp[nxt][bestMask]) {
                        bestStart = nxt;
                        break;
                    }
                }
            }
            out << bestSize << "\n";
            for(int u: path) out << u << " ";
            out << "\n";
            for (int u = 0; u < N; ++u) {
                adj[u].clear();
                dp[u].reset();
            }
        }
    }
};

int main() {
    longest_path_solver lps("longest_paths.txt");
    lps.process_graphs("graphs.txt");
    return 0;
}