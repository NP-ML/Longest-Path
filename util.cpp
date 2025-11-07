#include <config.hpp>
using namespace std;

// Fills the `dp` grid where `dp[u][s]` is whether or not there's a path starting from `u` containing all vertices in `s`
//
// Requirements: 
//  `dp` must be initialized to 0s
static void find_longest_path(adjacency_list& adj, bool_grid& dp) {
    int temp, u;
    for(u = 0; u < N; ++u) dp[u][1 << u] = true;
    for(int mask = 1; mask < POW2_N; ++mask)
        for(u = 0; u < N; ++u)
            if(contains(mask, u) && (mask & (mask - 1))) {
                temp = mask ^ (1 << u);
                for(int& v: adj[u])
                    if(dp[v][temp]) {
                        dp[u][mask] = true;
                        break;
                    }
            }
}

// Fills the `id` array where `id[u]` is number of SCC containing `u` and returns `SCC` where `SCC[i]` is list of vertices in `i`th SCC
//
// Requirements:
//  `id` must be initialized to -1s
//  `s` and `t` must be initialized to 0s
vector<vector<int>> getSCCs(adjacency_list& adj, int_array& id, int_array& t, int_array& s, int mask) {
    int tick = 0, group_id = 0;
    vector<vector<int>> scc;
    auto dfs = [&](int u, auto&& self) -> int {
        int low = t[u] = ++tick;
        s.add(u);
        for(int v: adj[u])
            if(id[v] == -1 && contains(mask, v))
                low = min(low, t[v] != 0 ? t[v] : self(v, self));
        if(low == t[u]) {
            int v;
            scc.push_back(vector<int>());
            while(true) {
                id[v = s.pop()] = group_id;
                scc[group_id].push_back(v);
                if(v == u) break;
            }
            ++group_id;
        }
        return low;
    };
    for(int u = 0; u < N; ++u)
        if(t[u] == 0 && contains(mask, u))
            dfs(u, dfs);
    return scc;
}