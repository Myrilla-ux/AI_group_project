import random
from itertools import combinations
from collections import defaultdict
from math import comb
import time

def user_input():
    print("=== 最优样本选择系统 ===")
    while True:
        try:
            m = int(input("请输入总样本数量 m（45~54）: "))
            if 45 <= m <= 54:
                break
        except:
            pass
        print(" 输入不合法，请输入范围内的整数")
    while True:
        try:
            n = int(input(f"从中选择 n 个样本（7~25，且 n ≤ m）: "))
            if 7 <= n <= 25 and n <= m:
                break
        except:
            pass
        print(" 输入不合法，请输入 7~25 且 ≤ m 的整数")
    while True:
        try:
            k = int(input("每组样本数量 k（4~7 且 ≤ n）: "))
            if 4 <= k <= 7 and k <= n:
                break
        except:
            pass
        print(" 输入不合法，请输入 4~7 且 ≤ n 的整数")
    while True:
        try:
            j_input = input(f" 由于 k = {k}，所以 j 最大为 {k}\n请输入目标组合大小 j（默认 = {k}）: ")
            j = k if j_input.strip() == "" else int(j_input.strip())
            if 1 <= j <= k:
                break
        except:
            pass
        print(" 输入不合法，请输入不大于 k 的整数")
    while True:
        try:
            default_s = min(5, j)
            s_input = input(f" 由于 j = {j}，所以 s 最大为 {j}\n请输入目标子组合大小 s（默认 = {default_s}）: ")
            s = default_s if s_input.strip() == "" else int(s_input.strip())
            if 3 <= s <= 7 and s <= j:
                break
        except:
            pass
        print(" 输入不合法，请输入 3~7 且 ≤ j 的整数")
    max_t = comb(j, s)
    while True:
        try:
            t_input = input(f" 由于 j = {j}, s = {s}，可产生的 s 子组合个数为 C({j},{s}) = {max_t}\n请输入每个 j 组合中至少要覆盖的 s 子组合数 t（默认 = {max_t}）: ")
            t = max_t if t_input.strip() == "" else int(t_input.strip())
            if 1 <= t <= max_t:
                break
        except:
            pass
        print(" 输入不合法，请输入合法范围内的整数")
    return int(m), int(n), int(k), int(j), int(s), int(t)

def generate_samples(m, n):
    all_samples = [f"{i:02d}" for i in range(1, m + 1)]
    selected_n = random.sample(all_samples, n)
    print(f"\n 选出的 n = {n} 个样本为：{selected_n}")
    return selected_n
#C(j,s)
def generate_target_map(selected_n, j, s):
    print(f"\n 从 n 中生成所有 j = {j} 的组合，再生成每个 j 的 s = {s} 子组合...")
    j_groups = list(combinations(selected_n, j))
    target_map = {j_group: set(combinations(j_group, s)) for j_group in j_groups}
    total_s = sum(len(v) for v in target_map.values())
    print(f" 总共需要覆盖的 s 子组合数：{total_s}，j组数量：{len(target_map)}")
    return target_map
#C(n,k)
def generate_k_groups(selected_n, k):
    print(f"\n 从 n 个样本中生成所有 k = {k} 的组合...")
    return list(combinations(selected_n, k))

def find_minimal_k_groups_covering_t_s_optimized(target_map, k_groups, t, j, s):
    assert isinstance(s, int), f"[错误] s 必须是 int 类型，但现在是 {type(s)}, 值是 {s}"
    assert isinstance(j, int), f"[错误] j 必须是 int 类型，但现在是 {type(j)}, 值是 {j}"
    assert isinstance(t, int), f"[错误] t 必须是 int 类型，但现在是 {type(t)}, 值是 {t}"

    print(f"\n 使用倒排索引 + 剪枝：寻找最小的 k 组合集，确保每个 j={j} 组合中至少有 t={t} 个 s={s} 子组合被覆盖")

    # 索引从 s → j
    s_to_j_map = defaultdict(set)
    for j_group, s_set in target_map.items():
        for s_sub in s_set:
            s_to_j_map[s_sub].add(j_group)

    # k组合可覆盖的 s集合
    target_s_subs = set(s_to_j_map.keys())
    k_cover_map = {}
    for k_group in k_groups:
        covered_s = set()
        for s_sub in combinations(k_group, s):
            if s_sub in target_s_subs:
                covered_s.add(s_sub)
        # 没用的k组合直接跳过，好像实现不了
        if covered_s:
            k_cover_map[k_group] = covered_s

    print(f" 剪枝后剩余的k组合数量：{len(k_cover_map)} / {len(k_groups)}")

    uncovered_s_by_j = {j_group: set(s_list) for j_group, s_list in target_map.items()}
    selected_k_groups = []

    while True:
        j_groups_needed = {
            j: s_subs for j, s_subs in uncovered_s_by_j.items()
            if len(s_subs) > len(target_map[j]) - t
        }
        if not j_groups_needed:
            break

        best_k = None
        best_gain = 0
        best_contribution = defaultdict(set)

        for k_group, covered_s in k_cover_map.items():
            # 如果这个 k组合能覆盖的 s，全都已经被覆盖过，就跳过
            effective_s = set()
            for s_sub in covered_s:
                for j_group in s_to_j_map[s_sub]:
                    if j_group in j_groups_needed and s_sub in uncovered_s_by_j[j_group]:
                        effective_s.add((j_group, s_sub))
            if not effective_s:
                continue

            temp_contribution = defaultdict(set)
            for j_group, s_sub in effective_s:
                temp_contribution[j_group].add(s_sub)

            gain = sum(len(v) for v in temp_contribution.values())
            if gain > best_gain:
                best_k = k_group
                best_gain = gain
                best_contribution = temp_contribution

        if best_gain == 0:
            print(" 无法找到更多有效组合，提前退出")
            break

        print(f" 选中组合 {best_k} 覆盖了 {best_gain} 个目标 s={s} 子组合")
        selected_k_groups.append(best_k)

        for j_group, s_subs in best_contribution.items():
            uncovered_s_by_j[j_group] -= s_subs

    print(f"\n 最终选中 {len(selected_k_groups)} 个 k 组合，满足每个 j={j} 至少覆盖 {t} 个 s={s} 子组合")
    return selected_k_groups

def main():
    m, n, k, j, s, t = user_input()
    start_time = time.time()
    selected_n = generate_samples(m, n)
    target_map = generate_target_map(selected_n, j, s)
    k_groups = generate_k_groups(selected_n, k)
    result_groups = find_minimal_k_groups_covering_t_s_optimized(target_map, k_groups, t, j, s)

    print("\n=== 最终选择的 k 组样本如下 ===")
    for i, group in enumerate(result_groups, 1):
        print(f"第{i:02d}组: {group}")

    end_time = time.time()  
    print(f"\n 程序总运行时间：{end_time - start_time:.10f} 秒")

    input("\n 程序执行完毕，按回车退出。")

if __name__ == "__main__":
    main()
