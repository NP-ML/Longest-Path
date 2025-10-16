#include <bitset>
#include <array>
#include <vector>
using namespace std;

constexpr unsigned int N = 25; // Graph size
constexpr unsigned int POW2_N = 1 << N;
using int_array = array<int, N>;
using adjacency_list = array<vector<int>, N>;
using bool_grid = vector<bitset<POW2_N>>;

struct longest_path_solver {
    bool_grid dp;
    longest_path_solver() : dp(N) {}
    void find_longest_path(adjacency_list& adj, int_array& lp) {
        // Provide the lp array so it can be reused
        int temp;
        for(int u = 0; u < N; ++u) dp[u][1 << u] = true;
        for(int mask = 1; mask < POW2_N; ++mask)
            for(int u = 0; u < N; ++u)
                if(((mask >> u) & 1) && (mask & (mask - 1))) {
                    temp = mask ^ (1 << u);
                    for(int& v: adj[u])
                        if(dp[v][temp]) {
                            dp[u][mask] = true;
                            break;
                        }
                }
        for(int u = 0; u < N; ++u) {
            temp = 0;
            for(int mask = 1; mask < POW2_N; ++mask)
                if(dp[u][mask])
                    temp = max(temp, __builtin_popcount(mask));
            lp[u] = temp;
            dp[u].reset();
        }
    }
};
