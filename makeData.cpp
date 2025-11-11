#include "feature_calculation.cpp"
#include <fstream>
static void build_X_y_single_pass(list_of_lists &adj,
                                  std::vector<std::vector<int>> &X,
                                  std::vector<int> &y)
{
    // full subset mask
    const int s = (N >= 31 ? -1 : (1u << N) - 1);

    // scratch
    std::vector<std::vector<int>> scc;
    int_array id, t, st;
    list_of_lists adj1, adj2;
    std::array<scc_features, N> scc_feats;
    std::array<vertex_features, N> vertex_feats;

    // run your already-written pipeline once on G[s]
    id.fill(-1);
    t.fill(0);
    st.size = 0;
    get_sccs(scc, adj, id, t, st, s);
    extract_scc_features(scc, id, adj, adj1, adj2, scc_feats, s);
    extract_vertex_features(scc, id, adj1, adj2, scc_feats, vertex_feats);

    // pack rows: SCC features + vertex features, one row per u
    X.clear();
    y.clear();
    X.resize(N);
    y.resize(N);

    for (int u = 0; u < (int)N; ++u)
    {
        scc_features *sf = vertex_feats[u].scc_feats;
        int scc_size = sf ? sf->size : 0;
        int scc_edges_inside = sf ? sf->number_of_edges_inside_scc : 0;
        int scc_edges_to_other = sf ? sf->number_of_edges_to_other_sccs : 0;
        int scc_largest_path_sum = sf ? sf->largest_path_sum : 0;
        int scc_longest_dfs_path = sf ? sf->longest_dfs_path : 0;

        int out_in = vertex_feats[u].outdegree_inside_scc;
        int out_out = vertex_feats[u].outdegree_outside_scc;
        int in_in = vertex_feats[u].indegree_inside_scc;
        int v_longest_dfs_plus = vertex_feats[u].longest_path_using_dfs_paths;
        int v_first_dfs_used = vertex_feats[u].first_dfs_path_used;

        X[u] = {
            scc_size,
            scc_edges_inside,
            scc_edges_to_other,
            scc_largest_path_sum,
            scc_longest_dfs_path,
            out_in,
            out_out,
            in_in,
            v_longest_dfs_plus,
            v_first_dfs_used};

        // label: longest path per node (use the per-vertex quantity your extractor computes)
        y[u] = v_longest_dfs_plus;
    }
}

// int main()
// {
//     list_of_lists adj;
//     // One line: chain 0→1→…→N-1 (works for N=30)
//     for (int i = 0; i < (int)N - 1; ++i)
//         adj[i].push_back(i + 1);

//     std::vector<std::vector<int>> X;
//     std::vector<int> y;

//     build_X_y_single_pass(adj, X, y);

//     std::ofstream csv("dataset.csv", std::ios::trunc);
//     csv << "u,"
//            "scc_size,scc_edges_inside,scc_edges_to_other,scc_largest_path_sum,scc_longest_dfs_path,"
//            "outdegree_inside_scc,outdegree_outside_scc,indegree_inside_scc,"
//            "longest_path_using_dfs_paths,first_dfs_path_used,"
//            "y\n";

//     for (int u = 0; u < (int)N; ++u)
//     {
//         const auto &R = X[u]; // R has 10 features in this order
//         csv << u << ","
//             << R[0] << "," << R[1] << "," << R[2] << "," << R[3] << "," << R[4] << ","
//             << R[5] << "," << R[6] << "," << R[7] << ","
//             << R[8] << "," << R[9] << ","
//             << y[u] << "\n";
//     }
//     csv.close();

//     std::cout << "Wrote dataset.csv with " << N << " rows.\n";

//     return 0;
// }
