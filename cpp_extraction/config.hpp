#include <bits/stdc++.h>
using namespace std;

constexpr unsigned int N = 30; // Graph size
constexpr unsigned int POW2_N = 1 << N;

struct int_map : vector<int> {
    int_map() : vector<int>(POW2_N) {}
};
class int_set {
    vector<uint64_t> data = vector<uint64_t>(POW2_N >> 6, 0);
public:
    int_set() {}
    class ref {
        uint64_t &block;
        uint64_t mask;
    public:
        ref(uint64_t &b, uint64_t m) : block(b), mask(m) {}
        ref& operator=(bool v) {
            if (v) block |= mask;
            else block &= ~mask;
            return *this;
        }
        operator bool() const { return (block & mask) != 0; }
    };
    ref operator[](size_t i) { return ref(data[i >> 6], 1ULL << (i & 63)); }
    bool operator[](size_t i) const { return (data[i >> 6] >> (i & 63)) & 1ULL; }
    void reset() { fill(data.begin(), data.end(), 0ULL); }
};
using list_of_lists = array<vector<int>, N>;
struct bool_grid : public vector<int_set> {
    bool_grid() : vector<int_set>(N) {}
};
// Array or stack of `N` integers
struct int_array : public array<int, N> {
    int size = 0;
    int_array() {};
    void add(int x) { this->operator[](size++) = x; }
    int top() { return this->operator[](size - 1); }
    int pop() { return this->operator[](--size); }
};

#define contains(mask, b) (((mask) >> (b)) & 1)
#define toggle(mask, b) ((mask) ^= (1 << (b)))
