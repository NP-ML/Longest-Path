#include <bitset>
#include <array>
#include <vector>
using namespace std;

constexpr unsigned int N = 25; // Graph size
constexpr unsigned int POW2_N = 1 << N;

using int_array = array<int, N>;
using int_subset_array = array<int, POW2_N>;
using bool_array = bitset<N>;
using bool_subset_array = bitset<POW2_N>;
using adjacency_list = array<vector<int>, N>;
struct bool_grid : public vector<bool_subset_array> { bool_grid() : vector<bool_subset_array>(N) {} };