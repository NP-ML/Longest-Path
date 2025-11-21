N = 25
POW2_N = 1 << N

def contains(mask, b): return (mask >> b) & 1 == 1

def isPowOf2(x): return (x & (x - 1)) == 0

def popcount(x): return x.popcount()