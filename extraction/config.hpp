#include <bits/stdc++.h>
using namespace std;

constexpr unsigned int N = 5; // Graph size
constexpr unsigned int POW2_N = 1 << N;

using int_map = array<int, POW2_N>;
using int_set = bitset<POW2_N>;
using list_of_lists = array<vector<int>, N>;
struct bool_grid : public vector<int_set>
{
    bool_grid() : vector<int_set>(N) {}
};
// Array or stack of `N` integers
struct int_array : public array<int, N>
{
    int size = 0;
    int_array() {};
    void add(int x) { this->operator[](size++) = x; }
    int top() { return this->operator[](size - 1); }
    int pop() { return this->operator[](--size); }
};

#define contains(mask, b) (((mask) >> (b)) & 1)
#define toggle(mask, b) ((mask) ^= (1 << (b)))