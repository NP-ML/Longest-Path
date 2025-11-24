class SCCFeatures:
    """Equivalent to the C++ struct scc_features."""
    def __init__(self,
                 size=0,
                 number_of_edges_inside_scc=0,
                 number_of_edges_to_other_sccs=0,
                 largest_path_sum=0,
                 longest_dfs_path=0):
        self.size = size
        self.number_of_edges_inside_scc = number_of_edges_inside_scc
        self.number_of_edges_to_other_sccs = number_of_edges_to_other_sccs
        self.largest_path_sum = largest_path_sum
        self.longest_dfs_path = longest_dfs_path

    def __repr__(self):
        return (f"SCCFeatures(size={self.size}, "
                f"edges_in={self.number_of_edges_inside_scc}, "
                f"edges_out={self.number_of_edges_to_other_sccs}, "
                f"largest_path_sum={self.largest_path_sum}, "
                f"longest_dfs_path={self.longest_dfs_path})")

class VertexFeatures:
    """Equivalent to the C++ struct vertex_features."""
    def __init__(self,
                 outdegree_inside_scc=0,
                 outdegree_outside_scc=0,
                 indegree_inside_scc=0,
                 longest_path_using_dfs_paths=0,
                 first_dfs_path_used=0,
                 scc_feats=None):  # reference to SCCFeatures
        self.outdegree_inside_scc = outdegree_inside_scc
        self.outdegree_outside_scc = outdegree_outside_scc
        self.indegree_inside_scc = indegree_inside_scc
        self.longest_path_using_dfs_paths = longest_path_using_dfs_paths
        self.first_dfs_path_used = first_dfs_path_used
        self.scc_feats = scc_feats  # expected to be an SCCFeatures instance or None

    def __repr__(self):
        return (f"VertexFeatures(longest_path={self.longest_path}, "
                f"out_in={self.outdegree_inside_scc}, out_out={self.outdegree_outside_scc}, "
                f"in_in={self.indegree_inside_scc}, dfs_sum={self.longest_path_using_dfs_paths}, "
                f"first_dfs={self.first_dfs_path_used}, "
                f"scc_feats={self.scc_feats})")
    def to_list(self):
        scc_feats = self.scc_feats
        return [
            scc_feats.size, 
            scc_feats.number_of_edges_inside_scc, 
            scc_feats.number_of_edges_to_other_sccs,
            scc_feats.largest_path_sum,
            scc_feats.longest_dfs_path,
            self.outdegree_inside_scc,
            self.outdegree_outside_scc,
            self.indegree_inside_scc,
            self.longest_path_using_dfs_paths,
            self.first_dfs_path_used,
        ]

def get_sccs(adj):
    """
    Computes strongly connected components (SCCs) of a directed graph.
    Assumes all vertices are included (no subset filtering).
    
    Parameters:
        adj: list[list[int]]
            adjacency list where adj[u] is list of neighbors of u

    Returns:
        scc: list[list[int]]
            scc[i] is the list of vertices in the i-th SCC
        id: list[int]
            id[u] = index of SCC containing vertex u
    """
    n = len(adj)
    scc = []
    id = [-1] * n
    t = [0] * n
    st = []
    tick = 0
    group_id = 0

    def dfs(u):
        nonlocal tick, group_id
        tick += 1
        low = t[u] = tick
        st.append(u)
        for v in adj[u]:
            if id[v] == -1:  # not yet assigned to an SCC
                if t[v] == 0:
                    low = min(low, dfs(v))
                else:
                    low = min(low, t[v])
        if low == t[u]:
            scc.append([])
            while True:
                v = st.pop()
                id[v] = group_id
                scc[group_id].append(v)
                if v == u:
                    break
            group_id += 1
        return low

    for u in range(n):
        if t[u] == 0:
            dfs(u)

    return scc, id

def extract_scc_features(scc, id, adj):
    """
    Builds adj1 (intra-SCC edges), adj2 (inter-SCC edges),
    and computes SCC feature statistics.

    Parameters
    ----------
    scc : list[list[int]]
        scc[i] is the list of vertices in the i-th SCC
    id : list[int]
        id[u] = index of SCC containing vertex u
    adj : list[list[int]]
        adjacency list of the full graph

    Returns
    -------
    adj1 : list[list[int]]
        adj1[u] = neighbors v of u that belong to the same SCC
    adj2 : list[list[int]]
        adj2[u] = neighbors v of u that belong to *different* SCCs
    scc_feats : list[SCCFeatures]
        one feature struct per SCC
    """
    n = len(adj)
    k = len(scc)
    adj1 = [[] for _ in range(n)]
    adj2 = [[] for _ in range(n)]
    scc_feats = [SCCFeatures() for _ in range(k)]

    for i in range(k):
        this_scc_feats = scc_feats[i]
        this_scc_feats.size = len(scc[i])
        this_scc_feats.largest_path_sum = this_scc_feats.size
        this_scc_feats.number_of_edges_inside_scc = 0
        this_scc_feats.number_of_edges_to_other_sccs = 0

        for u in scc[i]:
            for v in adj[u]:
                if id[u] == id[v]:
                    adj1[u].append(v)
                    this_scc_feats.number_of_edges_inside_scc += 1
                else:
                    adj2[u].append(v)
                    this_scc_feats.number_of_edges_to_other_sccs += 1
                    # update the largest path sum
                    this_scc_feats.largest_path_sum = max(
                        this_scc_feats.largest_path_sum,
                        this_scc_feats.size + scc_feats[id[v]].largest_path_sum
                    )

    return adj1, adj2, scc_feats

def extract_vertex_features(scc, id, adj1, adj2, scc_feats):
    """
    Builds per-vertex feature data based on SCCs and adjacency lists.
    Equivalent to the given C++ extract_vertex_features function,
    but uses a boolean array for visited state.

    Parameters
    ----------
    scc : list[list[int]]
        scc[i] is the list of vertices in the i-th SCC
    id : list[int]
        id[u] = index of SCC containing u
    adj1 : list[list[int]]
        adjacency list of edges within the same SCC
    adj2 : list[list[int]]
        adjacency list of edges between SCCs
    scc_feats : list[SCCFeatures]
        feature structs per SCC

    Returns
    -------
    vertex_feats : list[VertexFeatures]
        vertex_feats[u] contains per-vertex features for vertex u
    """
    n = len(adj1)
    vertex_feats = [VertexFeatures() for _ in range(n)]

    for i, vertices in enumerate(scc):
        this_scc_feats = scc_feats[i]
        this_scc_feats.longest_dfs_path = 1

        # Build reverse adjacency within this SCC
        rev_adj = [[] for _ in range(n)]
        for u in vertices:
            this_vertex_feats = vertex_feats[u]
            this_vertex_feats.outdegree_inside_scc = len(adj1[u])
            this_vertex_feats.outdegree_outside_scc = len(adj2[u])
            this_vertex_feats.longest_path_using_dfs_paths = 1
            this_vertex_feats.first_dfs_path_used = 1
            this_vertex_feats.scc_feats = this_scc_feats
            for v in adj1[u]:
                rev_adj[v].append(u)

        # Compute indegree_inside_scc
        for u in vertices:
            vertex_feats[u].indegree_inside_scc = len(rev_adj[u])

        # Compute DFS-based longest paths within SCC
        for u in vertices:
            remaining = 0
            for v in adj2[u]:
                remaining = max(remaining, vertex_feats[v].longest_path_using_dfs_paths)

            visited = [False] * n  # boolean array, not a set

            def dfs(u_, length):
                visited[u_] = True
                this_vertex_feats = vertex_feats[u_]

                # Update SCC's longest_dfs_path
                this_scc_feats.longest_dfs_path = max(this_scc_feats.longest_dfs_path, length)

                # Update vertex's path metrics
                total = length + remaining
                if (total > this_vertex_feats.longest_path_using_dfs_paths or
                    (total == this_vertex_feats.longest_path_using_dfs_paths and
                     length < this_vertex_feats.first_dfs_path_used)):
                    this_vertex_feats.longest_path_using_dfs_paths = total
                    this_vertex_feats.first_dfs_path_used = length

                # Explore reversed edges inside SCC
                for v in rev_adj[u_]:
                    if not visited[v]:
                        dfs(v, length + 1)

            dfs(u, 1)

    return vertex_feats

def extract_features(adj):
    scc, id = get_sccs(adj)
    adj1, adj2, scc_feats = extract_scc_features(scc, id, adj)
    vertex_feats = extract_vertex_features(scc, id, adj1, adj2, scc_feats)
    return [vf.to_list() for vf in vertex_feats]
