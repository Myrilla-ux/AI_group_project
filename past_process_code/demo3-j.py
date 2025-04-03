# version 2025/4/1 解决k有多个0的问题
# version 2025/4/2 定义递归函数解决选择重复的问题

import random
import itertools
import time
import numpy as np

start_time = time.time()


n = 8
k = 6
j = 5
s = 4
t = 2
# 从45-54中选7个不重复数字作为实际数值
random_numbers = random.sample(range(1, 55), n)
print(f"生成的7个数字: {random_numbers}")
# 生成 s 矩阵
num_zeros_s = n-s
positions_zeros = list(itertools.combinations(range(n), num_zeros_s))
arr_s = []
for pos in positions_zeros:
    binary_s = [1] * n  # 初始化为1
    for p in pos:
        binary_s[p] = 0  # 选中的位置设为0
    arr_s.append(binary_s)  # 添加到二维数组中
#-------------输出-----------------------#
# for binary_s in arr_s:
#     print(binary_s)  # 打印每个二进制数组
# print(f'n / k: {j} / {s}')
#-----------------------------------------#

# 生成 k 矩阵
num_zeros_k = n-k
positions_zeros = list(itertools.combinations(range(n), num_zeros_k))
arr_k = []
for pos in positions_zeros:
    binary_k = [1] * n  # 初始化为1
    for p in pos:
        binary_k[p] = 0  # 选中的位置设为0
    arr_k.append(binary_k)  # 添加到二维数组中
#-------------输出-----------------------#
# for binary_k in arr_k:
#     print(binary_k)  # 打印每个二进制数组
# print(f'n / k: {n} / {k}')
#-----------------------------------------#

# 生成 j 矩阵
num_zeros_j = n-j
positions_zeros = list(itertools.combinations(range(n), num_zeros_j))
arr_j = []
for pos in positions_zeros:
    binary_j = [1] * n  # 初始化为1
    for p in pos:
        binary_j[p] = 0  # 选中的位置设为0
    arr_j.append(binary_j)  # 添加到二维数组中
#-------------输出-----------------------#
for binary_j in arr_j:
    print(binary_j)  # 打印每个二进制数组
print(f'n / k: {n} / {j}')
#-----------------------------------------#


# ---------------定义回溯方法----------------#
def backtrack(arr_s, arr_k, num_zeros_k, selected_combinations, covered_rows_s, covered_rows_k, arr_j, j_counters, t):
    # 统计未被覆盖的行中每列的 0 的个数
    column_zero_counts = [0] * n
    for row_idx, row in enumerate(arr_s):
        if row_idx not in covered_rows_s:
            for col in range(n):
                if row[col] == 0:
                    column_zero_counts[col] += 1

    # 选择 0 最多的列（并列时随机）
    sorted_counts = sorted(enumerate(column_zero_counts), key=lambda x: x[1], reverse=True)
    current_combination = [col for col, _ in sorted_counts[:num_zeros_k]]

    # 将当前选择的列组合转化为元组并检查是否已经选中过
    current_combination = tuple(sorted(current_combination))  # 转化为元组，并按升序排序

    # 检查是否已经选过该组合
    if current_combination in selected_combinations:
        print(f"组合 {current_combination} 已经选择过，尝试替换列。")
        
        # 尝试替换组合中的列，逐个替换直到找到一个新的组合
        for i in range(len(current_combination)):
            for col, count in sorted_counts:
                if col not in current_combination:
                    # 替换当前列
                    new_combination = list(current_combination)
                    new_combination[i] = col
                    new_combination = tuple(sorted(new_combination))
                    
                    # 检查新的组合是否已选过
                    if new_combination not in selected_combinations:
                        current_combination = new_combination
                        print(f"替换后的组合: {current_combination}")
                        break
            if current_combination not in selected_combinations:
                break
        if current_combination in selected_combinations:
            print(f"无法找到新的组合，跳过当前选择。")
            return  

    # 如果没有选过该组合，则将其加入已选组合集合
    selected_combinations.add(current_combination)
    print(f"选中的列组合: {current_combination}")

    # 找到 k 矩阵中对应行
    for row_idx, row in enumerate(arr_k):
        # 检查选中列中的每个列是否为0，并且该行未被选中过
        if all(row[col] == 0 for col in current_combination) and row_idx not in covered_rows_k:
            covered_rows_k.append(row_idx)

    print("选中列为0的k行索引：", covered_rows_k)

    # 收集所有本轮覆盖到的 s 行索引
    newly_covered_s_rows = []
    for row_idx, row in enumerate(arr_s):
        if all(row[col] == 0 for col in current_combination) and row_idx not in covered_rows_s:
            covered_rows_s.add(row_idx)
            newly_covered_s_rows.append(row_idx)
            print(f"选中s行 {row_idx}，已覆盖总数：{len(covered_rows_s)}")

    # 如果启用 j 判断，并且有新覆盖的 s 行
    if t != s and newly_covered_s_rows:
        j_matrix = np.array(arr_j)
        s_matrix = np.array([arr_s[i] for i in newly_covered_s_rows])  # shape: (S, n)

        # 比较：j 行是否逐位 >= 每个 s 行
        mask_matrix = (j_matrix[:, None, :] >= s_matrix[None, :, :])  # shape: (J, S, n)
        coverage_matrix = mask_matrix.all(axis=2)  # shape: (J, S) 每个 j 是否能覆盖每个 s 是56*15因为第一轮要覆盖的就只有15个s

        # 累加计数：j 被匹配到多少个 s
        j_counters_np = np.array(j_counters)
        match_counts = coverage_matrix.sum(axis=1)
        j_counters_np += match_counts
        #---------调试-------------#
        # 遍历每个 j，看它命中了哪些 s
        for j_idx, count in enumerate(match_counts):
            if count > 0:
                matched_s_indices = np.where(coverage_matrix[j_idx])[0].tolist()
                print(f"j 行索引 {j_idx} 命中 s 行: {matched_s_indices}，本轮 +{int(count)}，当前总计数: {j_counters_np[j_idx]}")
        #--------------------------#
        j_counters[:] = j_counters_np.tolist()

        # 打印匹配详情
        for j_idx, count in enumerate(match_counts):
            if count > 0:
                print(f"j 行索引 {j_idx} 被覆盖 {int(count)} 次，当前总计数：{j_counters[j_idx]}")












# 初始化
covered_rows_s = set()  # 记录已被覆盖的 s 的行索引
covered_rows_k = [] # 存储选中的列为0的行索引
answer_matrix = []  # 存储最终匹配的 k 的行
selected_combinations = set() # 已被选择的组合情况 要再外面初始化
j_counters = [0] * len(arr_j)

while len(covered_rows_s) < len(arr_s) and not all(count >= t for count in j_counters):
    backtrack(arr_s, arr_k, num_zeros_k, selected_combinations, covered_rows_s, covered_rows_k, arr_j, j_counters, t)

answer_matrix = [arr_k[row_idx] for row_idx in covered_rows_k]    
print("\n最终选中的列：", covered_rows_k)

# ----------- 替换answer_matrix中的1并压缩0维度 ------------------------------------
compressed_answer = []
for row in answer_matrix:
    # 替换1为对应数字
    replaced = [random_numbers[i] if val == 1 else 0 for i, val in enumerate(row)]
    # 压缩0维度（移除所有0）
    compressed = [num for num in replaced if num != 0]
    compressed_answer.append(compressed)

print("\n压缩后的最终答案:")
for i, row in enumerate(compressed_answer, 1):
    print(f"行{i}: {row}")
    

# 计算并打印运行时间
end_time = time.time()
total_time = end_time - start_time
print(f"\n程序总运行时间: {total_time:.4f} 秒")