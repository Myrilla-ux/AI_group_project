import random
import itertools
import time
import numpy as np

def run_algorithm(n, k, j, s, random_numbers, t):
    start_time = time.time()

    # 生成 s 矩阵
    num_zeros_s = n - s
    positions_zeros = list(itertools.combinations(range(n), num_zeros_s))
    arr_s = []
    for pos in positions_zeros:
        binary_s = [1] * n
        for p in pos:
            binary_s[p] = 0
        arr_s.append(binary_s)

    # 生成 k 矩阵
    num_zeros_k = n - k
    positions_zeros = list(itertools.combinations(range(n), num_zeros_k))
    arr_k = []
    for pos in positions_zeros:
        binary_k = [1] * n
        for p in pos:
            binary_k[p] = 0
        arr_k.append(binary_k)

    # 生成 j 矩阵
    num_zeros_j = n - j
    positions_zeros = list(itertools.combinations(range(n), num_zeros_j))
    arr_j = []
    for pos in positions_zeros:
        binary_j = [1] * n
        for p in pos:
            binary_j[p] = 0
        arr_j.append(binary_j)

    # 回溯函数
    def backtrack(arr_s, arr_k, num_zeros_k, selected_combinations, covered_rows_s, covered_rows_k, arr_j, j_counters, t):
        column_zero_counts = [0] * n
        for row_idx, row in enumerate(arr_s):
            if row_idx not in covered_rows_s:
                for col in range(n):
                    if row[col] == 0:
                        column_zero_counts[col] += 1

        sorted_counts = sorted(enumerate(column_zero_counts), key=lambda x: x[1], reverse=True)
        current_combination = [col for col, _ in sorted_counts[:num_zeros_k]]
        current_combination = tuple(sorted(current_combination))

        if current_combination in selected_combinations:
            for i in range(len(current_combination)):
                for col, _ in sorted_counts:
                    if col not in current_combination:
                        new_comb = list(current_combination)
                        new_comb[i] = col
                        new_comb = tuple(sorted(new_comb))
                        if new_comb not in selected_combinations:
                            current_combination = new_comb
                            break
                if current_combination not in selected_combinations:
                    break
            if current_combination in selected_combinations:
                return

        selected_combinations.add(current_combination)

        for row_idx, row in enumerate(arr_k):
            if all(row[col] == 0 for col in current_combination) and row_idx not in covered_rows_k:
                covered_rows_k.append(row_idx)

        newly_covered_s_rows = []
        for row_idx, row in enumerate(arr_s):
            if all(row[col] == 0 for col in current_combination) and row_idx not in covered_rows_s:
                covered_rows_s.add(row_idx)
                newly_covered_s_rows.append(row_idx)

        if t != s and newly_covered_s_rows:
            j_matrix = np.array(arr_j)
            s_matrix = np.array([arr_s[i] for i in newly_covered_s_rows])
            mask_matrix = (j_matrix[:, None, :] >= s_matrix[None, :, :])
            coverage_matrix = mask_matrix.all(axis=2)
            j_counters_np = np.array(j_counters)
            match_counts = coverage_matrix.sum(axis=1)
            j_counters_np += match_counts
            j_counters[:] = j_counters_np.tolist()

    # 正式执行
    covered_rows_s = set()
    covered_rows_k = []
    selected_combinations = set()
    j_counters = [0] * len(arr_j)

    while len(covered_rows_s) < len(arr_s) and not all(count >= t for count in j_counters):
        backtrack(arr_s, arr_k, num_zeros_k, selected_combinations, covered_rows_s, covered_rows_k, arr_j, j_counters, t)

    answer_matrix = [arr_k[row_idx] for row_idx in covered_rows_k]

    compressed_answer = []
    for row in answer_matrix:
        replaced = [random_numbers[i] if val == 1 else 0 for i, val in enumerate(row)]
        compressed = [num for num in replaced if num != 0]
        compressed_answer.append(compressed)

    end_time = time.time()
    total_time = end_time - start_time

    return compressed_answer, total_time
