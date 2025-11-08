#include "config.hpp"
using namespace std;

struct scc_features {
    int size; 
    int number_of_edges_inside_scc = 0;
    int number_of_edges_to_other_sccs = 0;
    int largest_path_sum;
    int longest_dfs_path_to_exit;
};

struct vertex_features {
    int outdegree_inside_scc = 0;
    int outdegree_outside_scc = 0;
    int indegree_inside_scc = 0;
    int longest_path_using_dfs_paths;
    int first_dfs_path_used;
    scc_features* scc_feats = NULL;
};

// Returns `vector` of `scc_feature` structs for each SCC
vector<scc_features> extract_scc_features(vector<vector<int>>& scc, int_array& id, adjacency_list& adj, int s) {
    int k = scc.size();
    vector<scc_features> scc_feats(k);
    for(int i = 0; i < k; ++i) {
        scc_features& this_scc_feats = scc_feats[i];
        this_scc_feats.size = scc[i].size();
        this_scc_feats.largest_path_sum = this_scc_feats.size;
        for(int u: scc[i]) {
            if(!contains(s, u)) continue;
            for(int v: adj[u]) {
                if(!contains(s, v)) continue;
                if(id[u] == id[v]) {
                    ++this_scc_feats.number_of_edges_inside_scc;
                }
                else {
                    ++this_scc_feats.number_of_edges_to_other_sccs;
                    this_scc_feats.largest_path_sum = max(
                        this_scc_feats.largest_path_sum, 
                        this_scc_feats.size + scc_feats[id[v]].largest_path_sum
                    );
                }
            }
        }
    }
    return scc_feats;
}

// Fills the `vertex_feats` array where `vertex_feats[u]` is the `vertex_features` struct for the vertex `u`
void extract_vertex_features(int_array& id, adjacency_list& adj, array<vertex_features, N>& vertex_feats) {

}