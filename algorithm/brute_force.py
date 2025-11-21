from config import *

dp = [[False] * POW2_N for _ in range(N)]

def extract_longest_path(adj):
    n = len(adj)
    pow2_n = 1 << n
    for u in range(n): dp[u][1 << u] = True
    bestStart = 0
    bestMask = 1
    bestSize = 1
    for mask in range(pow2_n):
        for u in range(n):
            if contains(mask, u) and not isPowOf2(mask):
                temp = mask ^ (1 << u)
                for v in adj[u]:
                    if dp[v][temp]:
                        dp[u][mask] = True
                        size = popcount(mask)
                        if size > bestSize:
                            bestStart = u
                            bestMask = mask
                            bestSize = size
                        break
    path = []
    for _ in range(bestSize):
        path.append(bestStart)
        bestMask ^= 1 << bestStart
        for next in adj[bestStart]:
            if dp[next][bestMask]:
                bestStart = next
                break
    # resetting dp
    for mask in range(pow2_n):
        for u in range(n):
            dp[u][mask] = False
    return path