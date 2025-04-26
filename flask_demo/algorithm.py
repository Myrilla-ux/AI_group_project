import itertools
import time
import numpy as np
from numba import njit
import math

def run_algorithm(n, k, j, s, random_numbers, t):
    start_time = time.time()

    threshold = 13
    all_combinations = math.comb(j, s)

    # 生成 s 矩阵
    num_zeros_s = n - s
    positions_zeros_s = list(itertools.combinations(range(n), num_zeros_s))
    arr_s = np.ones((len(positions_zeros_s), n), dtype=int)
    for i, pos in enumerate(positions_zeros_s):
        arr_s[i, pos] = 0

    # 生成 k 矩阵
    num_zeros_k = n - k
    positions_zeros_k = list(itertools.combinations(range(n), num_zeros_k))
    arr_k = np.ones((len(positions_zeros_k), n), dtype=int)
    for i, pos in enumerate(positions_zeros_k):
        arr_k[i, pos] = 0

    # 生成 j 矩阵
    num_zeros_j = n - j
    positions_zeros_j = list(itertools.combinations(range(n), num_zeros_j))
    arr_j = np.ones((len(positions_zeros_j), n), dtype=int)
    for i, pos in enumerate(positions_zeros_j):
        arr_j[i, pos] = 0

    @njit
    def count_k_covers_s_1(arr_k, arr_s, n):
        K, N = arr_k.shape
        S = arr_s.shape[0]
        cover_counts = np.zeros(K, dtype=np.int32)
        for i in range(K):
            for j in range(S):
                valid = True
                for col in range(N):
                    if arr_k[i, col] == 0 and arr_s[j, col] != 0:
                        valid = False
                        break
                if valid:
                    cover_counts[i] += 1
        return cover_counts

    def count_k_covers_s_2(arr_k, arr_s_remaining, n):
        k_zero_mask = (arr_k == 0)
        match_mask = np.logical_or(~k_zero_mask[:, None, :], arr_s_remaining[None, :, :] == 0)
        can_cover = np.all(match_mask, axis=2)
        k_cover_count = np.sum(can_cover, axis=1)
        return k_cover_count

    def greedy_select_k_rows(arr_k, arr_s, arr_j, t):
        num_s = arr_s.shape[0]
        num_j = arr_j.shape[0] if arr_j is not None else 0

        selected_k_indices = []
        uncovered_s_indices = set(range(num_s))
        j_coverage_counter = np.zeros(num_j, dtype=int)

        if t < all_combinations:
            while np.any(j_coverage_counter < t):
                arr_s_remaining = arr_s[list(uncovered_s_indices)] if uncovered_s_indices else arr_s
                cover_counts = count_k_covers_s_1(arr_k, arr_s_remaining, n) if n > threshold else count_k_covers_s_2(arr_k, arr_s_remaining, n)
                best_k_idx = np.argmax(cover_counts)
                selected_k_indices.append(best_k_idx)

                k_row = arr_k[best_k_idx]
                k_zero_mask = (k_row == 0)
                can_cover_s = np.all(arr_s_remaining[:, k_zero_mask] == 0, axis=1)
                uncovered_s_list = list(uncovered_s_indices)
                relative_indices = np.where(can_cover_s)[0]
                covered_s_indices = [uncovered_s_list[i] for i in relative_indices]
                uncovered_s_indices.difference_update(covered_s_indices)

                selected_s_rows = arr_s[covered_s_indices]
                s_zero_mask = (selected_s_rows == 0)
                j_mask = (arr_j == 0)
                match_mask = np.logical_or(~j_mask[None, :, :], s_zero_mask[:, None, :])
                can_cover_j = np.all(match_mask, axis=2)
                j_coverage_counter += np.sum(can_cover_j, axis=0)
        else:
            while uncovered_s_indices:
                arr_s_remaining = arr_s[list(uncovered_s_indices)]
                cover_counts = count_k_covers_s_1(arr_k, arr_s_remaining, n) if n > threshold else count_k_covers_s_2(arr_k, arr_s_remaining, n)
                best_k_idx = np.argmax(cover_counts)
                selected_k_indices.append(best_k_idx)
                k_row = arr_k[best_k_idx]
                k_zero_mask = (k_row == 0)
                can_cover_s = np.all(arr_s_remaining[:, k_zero_mask] == 0, axis=1)
                uncovered_s_list = list(uncovered_s_indices)
                relative_indices = np.where(can_cover_s)[0]
                covered_s_indices = [uncovered_s_list[i] for i in relative_indices]
                uncovered_s_indices.difference_update(covered_s_indices)

        return selected_k_indices

    def decode_selected_k_rows(arr_k, selected_k_indices, random_numbers):
        selected_rows = arr_k[selected_k_indices]
        decoded_k = selected_rows * random_numbers
        return decoded_k

    selected_k = greedy_select_k_rows(arr_k, arr_s, arr_j, t)
    decoded_k = decode_selected_k_rows(arr_k, selected_k, np.array(random_numbers))
    compressed_answer = [[num for num in row if num != 0] for row in decoded_k.tolist()]

    end_time = time.time()
    total_time = end_time - start_time

    return compressed_answer, total_time
