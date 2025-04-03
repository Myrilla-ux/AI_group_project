import random
import itertools
import time

def run_algorithm(n, k, j, s, random_numbers):
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

    # 回溯函数
    def backtrack(arr_s, arr_k, num_zeros_k, selected_combinations, covered_rows_s, covered_rows_k):
        column_zero_counts = [0] * n
        for row_idx, row in enumerate(arr_s):
            if row_idx not in covered_rows_s:
                for col in range(n):
                    if row[col] == 0:
                        column_zero_counts[col] += 1

        sorted_counts = sorted(enumerate(column_zero_counts), key=lambda x: x[1], reverse=True)
        current_combination = []
        remaining_count = num_zeros_k

        for col, _ in sorted_counts:
            if remaining_count == 0:
                break
            current_combination.append(col)
            remaining_count -= 1

        if remaining_count > 0:
            for col, _ in sorted_counts:
                if col not in current_combination:
                    current_combination.append(col)
                    remaining_count -= 1
                if remaining_count == 0:
                    break

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

        for row_idx, row in enumerate(arr_s):
            if all(row[col] == 0 for col in current_combination) and row_idx not in covered_rows_s:
                covered_rows_s.add(row_idx)

    # 正式执行
    covered_rows_s = set()
    covered_rows_k = []
    selected_combinations = set()

    while len(covered_rows_s) < len(arr_s):
        backtrack(arr_s, arr_k, num_zeros_k, selected_combinations, covered_rows_s, covered_rows_k)

    answer_matrix = [arr_k[row_idx] for row_idx in covered_rows_k]

    # 替换并压缩
    compressed_answer = []
    for row in answer_matrix:
        replaced = [random_numbers[i] if val == 1 else 0 for i, val in enumerate(row)]
        compressed = [num for num in replaced if num != 0]
        compressed_answer.append(compressed)

    end_time = time.time()
    total_time = end_time - start_time

    return compressed_answer, total_time
