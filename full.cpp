#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include "makeData.cpp"
// full.cpp (relevant parts)
// DO NOT redefine list_of_lists here.
// Make sure you include headers that bring N and list_of_lists into scope.
#include <bits/stdc++.h>

using namespace std;

static inline void trim(string &s)
{
    auto not_space = [](int ch)
    { return !std::isspace(ch); };
    s.erase(s.begin(), find_if(s.begin(), s.end(), not_space));
    s.erase(find_if(s.rbegin(), s.rend(), not_space).base(), s.end());
}

static void clear_adj(list_of_lists &adj)
{
    for (auto &v : adj)
        v.clear();
}

// reads one graph into fixed-size adj (size N). returns false on EOF before finding a new block.
static bool read_next_graph_into_fixed_adj(istream &in, list_of_lists &adj, int &skipped_edges)
{
    skipped_edges = 0;
    clear_adj(adj);

    string line;
    long long m = -1;

    // find the next non-empty line containing the edge count
    while (getline(in, line))
    {
        trim(line);
        if (line.empty())
            continue;
        istringstream iss(line);
        if (iss >> m)
            break;
    }
    if (m < 0)
        return false; // no more graphs

    // read m edges; tolerate blank lines; skip out-of-range nodes (> N-1)
    for (long long i = 0; i < m; /* i++ inside */)
    {
        if (!getline(in, line))
            break;
        trim(line);
        if (line.empty())
            continue;
        istringstream ss(line);
        int u, v;
        if (!(ss >> u >> v))
            continue;

        if (0 <= u && u < (int)N && 0 <= v && v < (int)N)
        {
            adj[u].push_back(v); // directed; add adj[v].push_back(u) if you need undirected
            ++i;
        }
        else
        {
            ++skipped_edges;
            ++i;
        }
    }

    // consume an optional blank separator line
    streampos pos = in.tellg();
    if (getline(in, line))
    {
        trim(line);
        if (!line.empty())
            in.seekg(pos); // put back if it wasn't actually blank
    }
    return true;
}

int main()
{
    ifstream fin("graphs_adjlist.txt");
    if (!fin)
    {
        cerr << "Brooo… couldn't open graphs.txt\n";
        return 1;
    }

    std::ofstream csv("dataset.csv", std::ios::out | std::ios::trunc);
    if (!csv)
    {
        cerr << "DB said nope: can't open dataset.csv\n";
        return 1;
    }

    // header (10 features like your snippet)
    csv << "graph_id,u,"
           "scc_size,scc_edges_inside,scc_edges_to_other,scc_largest_path_sum,scc_longest_dfs_path,"
           "outdegree_inside_scc,outdegree_outside_scc,indegree_inside_scc,"
           "longest_path_using_dfs_paths,first_dfs_path_used,"
           "y\n";

    int graph_id = 0;
    list_of_lists adj; // size N (from config.hpp)
    while (true)
    {
        int skipped = 0;
        if (!read_next_graph_into_fixed_adj(fin, adj, skipped))
            break;

        vector<vector<int>> X;
        vector<int> y;
        build_X_y_single_pass(adj, X, y); // expects N vertices

        // safety checks
        if ((int)X.size() < (int)N || (int)y.size() < (int)N)
        {
            cerr << "warning: feature sizes smaller than N for graph " << graph_id << "\n";
        }

        for (int u = 0; u < (int)N; ++u)
        {
            const auto &R = (u < (int)X.size()) ? X[u] : vector<int>{};
            // expect 10 features; fill zeros if missing
            auto f = [&](int k)
            { return (k < (int)R.size()) ? R[k] : 0; };
            int yu = (u < (int)y.size()) ? y[u] : 0;

            csv << graph_id << "," << u << ","
                << f(0) << "," << f(1) << "," << f(2) << "," << f(3) << "," << f(4) << ","
                << f(5) << "," << f(6) << "," << f(7) << "," << f(8) << "," << f(9) << ","
                << yu << "\n";
        }

        cout << "Processed graph " << graph_id
             << " (skipped " << skipped << " edges out of range [0," << (N - 1) << "])\n";
        ++graph_id;
    }

    cout << "All graphs written to dataset.csv\n";
    return 0;
}
