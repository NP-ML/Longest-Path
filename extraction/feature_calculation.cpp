#include "algorithms.cpp"
using namespace std;

struct scc_features
{
    int size;
    int number_of_edges_inside_scc;
    int number_of_edges_to_other_sccs;
    int largest_path_sum;
    int longest_dfs_path;
};

struct vertex_features
{
    int longest_path;
    int outdegree_inside_scc;
    int outdegree_outside_scc;
    int indegree_inside_scc;
    int longest_path_using_dfs_paths;
    int first_dfs_path_used;
    scc_features *scc_feats = NULL;
};

// Fills `adj1` with edges in the same SCC, `adj2` with edges between different SCCs, and `scc_feats` with structs for each SCC
//
// Requirements:
//  `adj1[u]` and `adj2[u]` must be empty
void extract_scc_features(
    vector<vector<int>> &scc,
    int_array &id,
    list_of_lists &adj,
    list_of_lists &adj1,
    list_of_lists &adj2,
    array<scc_features, N> &scc_feats,
    int s)
{
    int k = scc.size();
    for (int i = 0; i < k; ++i)
    {
        scc_features &this_scc_feats = scc_feats[i];
        this_scc_feats.size = scc[i].size();
        this_scc_feats.largest_path_sum = this_scc_feats.size;
        this_scc_feats.number_of_edges_inside_scc = this_scc_feats.number_of_edges_to_other_sccs = 0;
        for (int u : scc[i])
        {
            for (int v : adj[u])
            {
                if (!contains(s, v))
                    continue;
                if (id[u] == id[v])
                {
                    adj1[u].push_back(v);
                    ++this_scc_feats.number_of_edges_inside_scc;
                }
                else
                {
                    adj2[u].push_back(v);
                    ++this_scc_feats.number_of_edges_to_other_sccs;
                    this_scc_feats.largest_path_sum = max(
                        this_scc_feats.largest_path_sum,
                        this_scc_feats.size + scc_feats[id[v]].largest_path_sum);
                }
            }
        }
    }
}

// Fills the `vertex_feats` array where `vertex_feats[u]` is the `vertex_features` struct for the vertex `u`
void extract_vertex_features(
    vector<vector<int>> &scc,
    int_array &id,
    list_of_lists &adj1,
    list_of_lists &adj2,
    array<scc_features, N> &scc_feats,
    array<vertex_features, N> &vertex_feats)
{
    int k = scc.size();
    for (int i = 0; i < k; ++i)
    {
        list_of_lists revAdj;
        scc_features &this_scc_feats = scc_feats[i];
        this_scc_feats.longest_dfs_path = 1;
        for (int u : scc[i])
        {
            vertex_features &this_vertex_feats = vertex_feats[u];
            this_vertex_feats.outdegree_inside_scc = adj1[u].size();
            this_vertex_feats.outdegree_outside_scc = adj2[u].size();
            this_vertex_feats.longest_path_using_dfs_paths = this_vertex_feats.first_dfs_path_used = 1;
            this_vertex_feats.scc_feats = &this_scc_feats;
            for (int v : adj1[u])
                revAdj[v].push_back(u);
        }
        for (int u : scc[i])
        {
            vertex_feats[u].indegree_inside_scc = revAdj[u].size();
            int s = 0, remaining = 0;
            for (int v : adj2[u])
                remaining = max(remaining, vertex_feats[v].longest_path_using_dfs_paths);
            auto dfs = [&](int u_, int len, auto &&self) -> void
            {
                toggle(s, u_);
                vertex_features &this_vertex_feats = vertex_feats[u_];
                this_scc_feats.longest_dfs_path = max(this_scc_feats.longest_dfs_path, len);
                if (len + remaining > this_vertex_feats.longest_path_using_dfs_paths || (len + remaining == this_vertex_feats.longest_path_using_dfs_paths && len < this_vertex_feats.first_dfs_path_used))
                {
                    this_vertex_feats.longest_path_using_dfs_paths = len + remaining;
                    this_vertex_feats.first_dfs_path_used = len;
                }
                for (int v : revAdj[u_])
                    if (!contains(s, v))
                        self(v, len + 1, self);
            };
            dfs(u, 1, dfs);
        }
    }
}

struct graph_processor
{
    bool_grid dp;
    int_map lp;
    list_of_lists adj1, adj2;
    vector<vector<int>> scc;
    int_array id, t, st;
    array<scc_features, N> scc_feats;
    array<vertex_features, N> vertex_feats;
    // Takes an adjacency list and a function for processing an example
    void process_graph(
        list_of_lists &adj,
        function<void(vertex_features &)> &process_example)
    {
        int s;
        fill_dp_grid(adj, dp);
        for (int u = 0; u < N; ++u)
        {
            for (s = 0; s < POW2_N; ++s)
                lp[s] = dp[u][s] ? __popcount(s) : 0;
            // max over subset (zeta transform)
            for (int i = 0; i < N; ++i)
                for (s = 0; s < POW2_N; ++s)
                    if (contains(s, i))
                        lp[s] = max(lp[s], lp[s ^ (1 << i)]);
            for (s = 1; s < POW2_N; ++s)
            { // considering G[s]
                if (!contains(s, u) || !reaches_all(u, adj, s))
                    continue;
                t.fill(0);
                id.fill(-1);
                get_sccs(scc, adj, id, t, st, s);
                extract_scc_features(scc, id, adj, adj1, adj2, scc_feats, s);
                extract_vertex_features(scc, id, adj1, adj2, scc_feats, vertex_feats);
                vertex_feats[u].longest_path = lp[s];
                process_example(vertex_feats[u]);
                // Resetting data structures
                scc.clear();
                for (int i = 0; i < N; ++i)
                {
                    adj1[i].clear();
                    adj2[i].clear();
                }
            }
        }
        for (int i = 0; i < N; ++i)
            dp[i].reset();
    }
};