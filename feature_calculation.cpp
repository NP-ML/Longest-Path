#include "config.hpp"
using namespace std;

struct scc_features {
    int size;
    int number_of_edges_inside_scc = 0;
    int number_of_edges_to_other_sccs = 0;
    int largest_path_sum;
};

struct vertex_features {
    int outdegree_inside_scc = 0;
    int outdegree_outside_scc = 0;
    int indegree_inside_scc = 0;
    scc_features* scc_feats = NULL;
    int longest_shortest_path_inside_scc;
    int longest_path_using_shortest_paths;
};
