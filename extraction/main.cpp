#include "feature_calculation.cpp"
#include <functional>
#include <fstream>
#include <iostream>
using namespace std;

struct runner
{
    ofstream out;
    graph_processor processor;
    list_of_lists adj;
    function<void(vertex_features &)> _process_example;

    runner(string output_file) : out(output_file, ios::app) {
        out << "scc_size,number_of_edges_inside_scc,number_of_edges_to_other_sccs,scc_largest_path_sum,scc_longest_dfs_path,outdegree_inside_scc,outdegree_outside_scc,indegree_inside_scc,longest_path_using_dfs_paths,first_dfs_path_used,longest_path\n";
        _process_example = [this](vertex_features& vertex_feats) {
            scc_features *scc_feats = vertex_feats.scc_feats;
            if(vertex_feats.longest_path_using_dfs_paths == scc_feats->largest_path_sum) return;
            out << scc_feats->size << ","
                << scc_feats->number_of_edges_inside_scc << ","
                << scc_feats->number_of_edges_to_other_sccs << ","
                << scc_feats->largest_path_sum << ","
                << scc_feats->longest_dfs_path << ","
                << vertex_feats.outdegree_inside_scc << ","
                << vertex_feats.outdegree_outside_scc << ","
                << vertex_feats.indegree_inside_scc << ","
                << vertex_feats.longest_path_using_dfs_paths << ","
                << vertex_feats.first_dfs_path_used << ","
                << vertex_feats.longest_path << "\n";
        };
    }

    void process_graph(string input_file) {
        ifstream in(input_file);
        int t, u, v, m;
        in >> t;
        while (t--) {
            in >> m;
            while (m--) {
                in >> u >> v;
                adj[u].push_back(v);
            }
            processor.process_graph(adj, _process_example);
            for (int u = 0; u < N; ++u)
                adj[u].clear();
        }
    }
};

int main() {
    runner r("dataset1.csv");
    r.process_graph("graph1.txt");
    return 0;
}