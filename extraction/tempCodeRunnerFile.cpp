// test_gp.cpp
#include "algorithms.cpp" // brings in N, POW2_N, types, helpers
#include <iostream>
#include <vector>
#include <functional>
using namespace std;

// ---------- your structs (as provided) ----------
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

// ---------- your helpers (as provided) ----------
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
        this_scc_feats.size = (int)scc[i].size();
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
            this_vertex_feats.outdegree_inside_scc = (int)adj1[u].size();
            this_vertex_feats.outdegree_outside_scc = (int)adj2[u].size();
            this_vertex_feats.longest_path_using_dfs_paths = this_vertex_feats.first_dfs_path_used = 1;
            this_vertex_feats.scc_feats = &this_scc_feats;
            for (int v : adj1[u])
                revAdj[v].push_back(u);
        }
        for (int u : scc[i])
        {
            vertex_feats[u].indegree_inside_scc = (int)revAdj[u].size();
            int s = 0, remaining = 0;
            for (int v : adj2[u])
                remaining = max(remaining, vertex_feats[v].longest_path_using_dfs_paths);
            auto dfs = [&](int u_, int len, auto &&self) -> void
            {
                toggle(s, u_);
                vertex_features &this_vertex_feats = vertex_feats[u_];
                this_scc_feats.longest_dfs_path = max(this_scc_feats.longest_dfs_path, len);
                if (len + remaining > this_vertex_feats.longest_path_using_dfs_paths ||
                    (len + remaining == this_vertex_feats.longest_path_using_dfs_paths && len < this_vertex_feats.first_dfs_path_used))
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

// ---------- your graph_processor (as provided) ----------
struct graph_processor
{
    bool_grid dp;
    int_map lp;
    list_of_lists adj1, adj2;
    vector<vector<int>> scc;
    int_array id, t, st;
    array<scc_features, N> scc_feats;
    array<vertex_features, N> vertex_feats;

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
            {
                if (!contains(s, u) || !reaches_all(u, adj, s))
                    continue;

                id.fill(-1);
                get_sccs(scc, adj, id, t, st, s);
                extract_scc_features(scc, id, adj, adj1, adj2, scc_feats, s);
                extract_vertex_features(scc, id, adj1, adj2, scc_feats, vertex_feats);
                vertex_feats[u].longest_path = lp[s];
                process_example(vertex_feats[u]);

                // reset
                t.fill(0);
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

// ---------- tiny printer for the callback ----------
static void print_vf(const vertex_features &vf)
{
    cout << "vertex_features{ "
         << "LP=" << vf.longest_path
         << ", out_in=" << vf.outdegree_inside_scc
         << ", out_out=" << vf.outdegree_outside_scc
         << ", in_in=" << vf.indegree_inside_scc
         << ", LP_dfs=" << vf.longest_path_using_dfs_paths
         << ", first_dfs=" << vf.first_dfs_path_used;
    if (vf.scc_feats)
    {
        cout << ", scc.size=" << vf.scc_feats->size
             << ", scc.edges_in=" << vf.scc_feats->number_of_edges_inside_scc
             << ", scc.edges_out=" << vf.scc_feats->number_of_edges_to_other_sccs
             << ", scc.sum=" << vf.scc_feats->largest_path_sum
             << ", scc.longest_dfs=" << vf.scc_feats->longest_dfs_path;
    }
    else
    {
        cout << ", scc=NULL";
    }
    cout << " }\n";
}

// ---------- build two tiny graphs ----------
static void build_graph_1(list_of_lists &adj)
{
    // 0↔1↔2 form an SCC; 2→3 (3 is a tail)
    // Make sure we don't exceed N:
    if (N < 4)
    {
        cerr << "N < 4; adjust test\n";
        return;
    }

    adj[0].push_back(1);
    adj[1].push_back(2);
    adj[2].push_back(0); // closes the cycle
    adj[2].push_back(3);
}

static void build_graph_2(list_of_lists &adj)
{
    // Two disjoint 2-cycles: (0↔1) and (2↔3)
    if (N < 4)
    {
        cerr << "N < 4; adjust test\n";
        return;
    }

    adj[0].push_back(1);
    adj[1].push_back(0);
    adj[2].push_back(3);
    adj[3].push_back(2);
}

// ---------- main test ----------
int main()
{
    cout << "N = " << N << " nodes\n";

    graph_processor gp;

    // prepare a NON-TEMPORARY std::function (your API requires lvalue ref)
    std::function<void(vertex_features &)> cb = [&](vertex_features &vf)
    {
        print_vf(vf);
    };

    // Test 1
    {
        list_of_lists adj;
        build_graph_1(adj);
        cout << "\n=== Test 1: cycle(0,1,2) with tail to 3 ===\n";
        gp.process_graph(adj, cb);
    }

    // Test 2
    {
        list_of_lists adj;
        build_graph_2(adj);
        cout << "\n=== Test 2: two disjoint 2-cycles ===\n";
        gp.process_graph(adj, cb);
    }

    cout << "\nDone.\n";
    return 0;
}
