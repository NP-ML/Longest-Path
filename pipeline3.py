
import torch 
import copy
def top_K_nodes(adj, model, extract_features_fn, undirected=False, neighbors_only_update=True):
    """
    1) extract_features(graph)
    2) score all nodes with model, pick argmax
    3) 'remove' node by zeroing incident edges
    4) extract_features(new graph)
    5) re-score only neighbors of the removed node
    6) repeat until all nodes are removed
    """
    model.eval()  # ⬅️ use the passed-in model
    device = next(model.parameters()).device

    graph = copy.deepcopy(adj)
    n = len(graph)
    Paths = []

    # initial features & scores for ALL nodes
    features_all = extract_features_fn(graph)                          # Nx10
    feats_t = torch.as_tensor(features_all, dtype=torch.float32, device=device)
    with torch.no_grad():
        for i in range(n):
            score = model(feats_t[i:i+1]).squeeze().item()             # ⬅️ model
            Paths.append((i, score))
    
    for _ in range(n):
        Paths.sort(key=lambda x: x[1], reverse=True)

        chosen_node = Paths[0][0]

        # neighbors of chosen_node (save before zeroing)
        neighbors_list = list(graph[chosen_node])

        # "remove" chosen node by zeroing outgoing and removing incoming refs
        for i in range(n):
            if i == chosen_node:
                graph[i] = []                                          # keep indices stable
            if chosen_node in graph[i]:
                graph[i].remove(chosen_node)

        # neighbors-only re-score
        features_new = extract_features_fn(graph)
        feats_t = torch.as_tensor(features_new, dtype=torch.float32, device=device)

        # drop chosen node from candidates
        Paths = [(idx, sc) for (idx, sc) in Paths if idx != chosen_node and (idx in neighbors_list)]

        with torch.no_grad():
            for j in neighbors_list:
                new_score = model(feats_t[j:j+1]).squeeze().item()     # ⬅️ model
                for k, (idx, _) in enumerate(Paths):
                    if idx == j:
                        Paths[k] = (idx, new_score)
                        break
                else:
                    Paths.append((j, new_score))

    return Paths

