#include <config.hpp>
using namespace std;

// Fills the `dp` grid where `dp[u][s]` is whether or not there's a path starting from `u` containing all vertices in `s`
//
// Requirements: 
//  `dp` must be initialized to 0s
static void fill_dp_grid(
    list_of_lists& adj, 
    bool_grid& dp
) {
    int temp, u;
    for(u = 0; u < N; ++u) dp[u][1 << u] = true;
    for(int mask = 1; mask < POW2_N; ++mask)
        for(u = 0; u < N; ++u)
            if(contains(mask, u) && (mask & (mask - 1))) {
                temp = mask ^ (1 << u);
                for(int v: adj[u])
                    if(dp[v][temp]) {
                        dp[u][mask] = true;
                        break;
                    }
            }
}

// Fills the `id` array where `id[u]` is number of SCC containing `u` and returns `scc` where `scc[i]` is list of vertices in `i`th SCC
//
// Requirements:
//  `scc` is empty
//  `id` must be initialized to -1s
//  `t` must be initialized to 0s
void get_sccs(
    vector<vector<int>>& scc, 
    list_of_lists& adj, 
    int_array& id, 
    int_array& t, 
    int_array& st, 
    int s
) {
    int tick = 0, group_id = 0;
    auto dfs = [&](int u, auto&& self) -> int {
        int low = t[u] = ++tick;
        st.add(u);
        for(int v: adj[u])
            if(id[v] == -1 && contains(s, v))
                low = min(low, t[v] != 0 ? t[v] : self(v, self));
        if(low == t[u]) {
            scc.push_back(vector<int>());
            int v;
            while(true) {
                id[v = st.pop()] = group_id;
                scc[group_id].push_back(v);
                if(v == u) break;
            }
            ++group_id;
        }
        return low;
    };
    for(int u = 0; u < N; ++u)
        if(t[u] == 0 && contains(s, u))
            dfs(u, dfs);
}

// Returns whether or not `u` reaches all of `s` in `G[s]`
bool reaches_all(
    int u,
    list_of_lists& adj,
    int s
) {
    auto dfs = [&](int u_, auto&& self) -> void {
        toggle(s, u_);
        for(int v: adj[u_])
            if(contains(s, v))
                self(v, self);
    };
    dfs(u, dfs);
    return s == 0;
}