from bitarray import bitarray

N = 30
POW2_N = 1 << N

def contains(mask, b): return (mask >> b) & 1 == 1

def isPowOf2(x): return (x & (x - 1)) == 0

def popcount(x): return x.bit_count()

dp = [bitarray(POW2_N) for _ in range(N)]
for b in dp:
    b.setall(False)


def extract_longest_path(adj):
    n = len(adj)
    pow2_n = 1 << n

    # Initialize dp[u][1 << u] = True
    for u in range(n):
        dp[u][1 << u] = True

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

    # Recover path
    path = []
    for _ in range(bestSize):
        path.append(bestStart)
        bestMask ^= 1 << bestStart
        for nxt in adj[bestStart]:
            if dp[nxt][bestMask]:
                bestStart = nxt
                break

    # Reset dp to all False
    for b in dp:
        b.setall(False)

    return path