def load_paths(path_file):
    with open(path_file, 'r') as f:
        t = int(f.readline().strip())
        lengths = []
        for _ in range(t):
            s = int(f.readline().strip())
            f.readline()  # skip the actual path line
            lengths.append(s)
    return lengths


def evaluate(real_file, approx_file):
    real = load_paths(real_file)
    approx = load_paths(approx_file)

    diffs = []
    ratios = []
    rel_err = []

    for r, a in zip(real, approx):
        diffs.append(r - a)
        ratios.append(a / r if r != 0 else 0)
        rel_err.append((r - a) / r if r != 0 else 0)

    print("avg_diff:", sum(diffs) / len(diffs))
    print("max_diff:", max(diffs))

    print("avg_ratio:", sum(ratios) / len(ratios))
    print("min_ratio:", min(ratios))

    print("avg_rel_error:", sum(rel_err) / len(rel_err))
    print("max_rel_error:", max(rel_err))

    print("avg_real_longest_path:", sum(real) / len(real))
    print("avg_approx_longest_path:", sum(approx) / len(approx))

if __name__ == "__main__":
    evaluate("computed_paths/longest_paths.txt", "computed_paths/approximate_paths.txt")