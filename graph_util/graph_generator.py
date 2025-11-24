# Generates random graphs (PureRandom & Mixed) with fixed n=30,
# appends adjacency lists to a text file 

import os, random, argparse

# ---------- generation ----------

def gen_pure_random(n, p):
    edges = set()
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p:
                edges.add((u, v))
    return sorted(edges)

def gen_mixed(n):
    p_out = 0.15 + 0.20 * random.random()   # was 0.05–0.20 → now 0.25–0.60
    p_in = 0.3 + 0.1 * random.random()      # was 0.6–1.0 (slightly higher average)
    p_bridge = 0.15 + 0.25 * random.random()  # was 0.10–0.30 → now 0.25–0.60

    edges = set()
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p_out:
                edges.add((u, v))

    r = random.random()
    if   r < 0.30: num_blocks = 0
    elif r < 0.75: num_blocks = 1
    else:          num_blocks = 2

    unused = list(range(n))
    random.shuffle(unused)
    blocks = []
    for _ in range(num_blocks):
        if len(unused) < 3: break
        max_s = min(6, max(3, len(unused)))
        s = random.randint(3, max_s)
        block = [unused.pop() for __ in range(s)]
        blocks.append(block)

    for B in blocks:
        if random.random() < 0.6:
            # full bidirected clique
            for i in range(len(B)):
                for j in range(len(B)):
                    if i != j: edges.add((B[i], B[j]))
        else:
            # soft SCC
            for i in range(len(B)):
                edges.add((B[i], B[(i + 1) % len(B)]))
            p_in = 0.2 + 0.4 * random.random()
            for i in range(len(B)):
                for j in range(len(B)):
                    if i != j and random.random() < p_in:
                        edges.add((B[i], B[j]))

    if len(blocks) >= 2:
        p_bridge = 0.05 + 0.20 * random.random()
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                for a in blocks[i]:
                    for b in blocks[j]:
                        if random.random() < p_bridge: edges.add((a, b))
                        if random.random() < p_bridge: edges.add((b, a))
    return sorted(edges)

# ---------- file utilities ----------

def parse_existing(path):
    total = pure = mixed = 0
    last_idx = 0
    if not os.path.exists(path):
        return total, pure, mixed, last_idx
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Graph "):
                total += 1
                if "PureRandom" in line:
                    pure += 1
                elif "Mixed" in line:
                    mixed += 1
                try:
                    num = int(line.split("#")[-1].strip().split()[0])
                    last_idx = max(last_idx, num)
                except Exception:
                    pass
    return total, pure, mixed, last_idx

def append_adjlist(path, edges, idx, fsync_every):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{len(edges)}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")
        f.write("\n")
        f.flush()
        if fsync_every and (idx % fsync_every == 0):
            os.fsync(f.fileno())

# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="graphs_adjlist_sparse.txt")
    ap.add_argument("--count", type=int, default=100)
    ap.add_argument("--pure", type=int, default=10, help="target pure-random count within total")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--fsync-every", type=int, default=50)
    args = ap.parse_args()

    have_total, have_pure, have_mixed, last_idx = parse_existing(args.out)
    print(f"[resume] found total={have_total}, pure={have_pure}, mixed={have_mixed}, last_id={last_idx:04d}")

    i = last_idx
    n = 30  # fixed number of nodes

    while have_total < args.count:
        i += 1
        rnd = random.Random(args.seed ^ i)

        if have_pure < args.pure:
            kind = "PureRandom"
        else:
            kind = "Mixed"

        random_state = random.getstate()
        random.seed(rnd.getrandbits(64))
        if kind == "PureRandom":
            p = 0.1 + 0.10 * rnd.random()
            edges = gen_pure_random(n, p)
        else:
            edges = gen_mixed(n)
        random.setstate(random_state)

        append_adjlist(args.out, edges, i, args.fsync_every)

        have_total += 1
        if kind == "PureRandom": have_pure += 1
        else: have_mixed += 1

        if have_total % 50 == 0:
            print(f"[progress] {have_total}/{args.count} written (pure={have_pure}, mixed={have_mixed})")

    print(f"[done] wrote {have_total} graphs (pure={have_pure}, mixed={have_mixed}) to {args.out}")

if __name__ == "__main__":
    main()
