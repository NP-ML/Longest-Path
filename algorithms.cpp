#include <config.hpp>
using namespace std;

// Fills the `dp` grid where `dp[u][s]` is whether or not there's a path starting from `u` containing all vertices in `s`
//
// Requirements: 
//  `dp` must be initialized to 0s
static void find_longest_path(list_of_lists& adj, bool_grid& dp) {
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

// Fills the `id` array where `id[u]` is number of SCC containing `u` and returns `scc` where `scc[i]` is list of vertices in `i`th SCC
//
// Requirements:
//  `scc[i]` is empty
//  `id` must be initialized to -1s
//  `s` and `t` must be initialized to 0s
void getSCCs(list_of_lists& scc, list_of_lists& adj, int_array& id, int_array& t, int_array& st, int s) {
    int tick = 0, group_id = 0;
    auto dfs = [&](int u, auto&& self) -> int {
        int low = t[u] = ++tick;
        st.add(u);
        for(int v: adj[u])
            if(id[v] == -1 && contains(s, v))
                low = min(low, t[v] != 0 ? t[v] : self(v, self));
        if(low == t[u]) {
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

// Fill the `reach` array where `reach[i]` is mask of all reachable vertices from SCC `i`
//
// Requirements:
//  `reach` is filled with 0s
void reachable(list_of_lists& scc, int_array& id, list_of_lists& adj2, int_array& reach) {
    int k = scc.size();
    for(int i = 0; i < k; ++i) {
        for(int u: scc[i]) {
            addto(reach[i], u);
            for(int v: adj2[u]) reach[i] |= reach[id[v]];
        }
    }
}