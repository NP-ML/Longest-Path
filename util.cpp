#include <config.hpp>
using namespace std;

static void find_longest_path(adjacency_list& adj, bool_grid& dp) {
    int temp, u;
    for(u = 0; u < N; ++u) dp[u][1 << u] = true;
    for(int mask = 1; mask < POW2_N; ++mask)
        for(u = 0; u < N; ++u)
            if(((mask >> u) & 1) && (mask & (mask - 1))) {
                temp = mask ^ (1 << u);
                for(int& v: adj[u])
                    if(dp[v][temp]) {
                        dp[u][mask] = true;
                        break;
                    }
            }
}