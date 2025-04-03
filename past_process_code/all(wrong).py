import random
import itertools
import time
start_time = time.time()


n = 7
k = 6
j = 5
s = 4
# 从45-54中选7个不重复数字作为实际数值
random_numbers = random.sample(range(45, 55), n)
print(f"生成的7个数字: {random_numbers}")
# 生成 s 矩阵
positions_s = list(itertools.combinations(range(n), s))
arr_s = []
for pos in positions_s:
    binary_s = [0] * n
    for p in pos:
        binary_s[p] = 1
    arr_s.append(binary_s)

# 生成 k 矩阵
positions_k = list(itertools.combinations(range(n), k))
arr_k = []
for pos in positions_k:
    binary_k = [0] * n
    for p in pos:
        binary_k[p] = 1
    arr_k.append(binary_k)

# 初始化
covered_rows = set()  # 记录已被覆盖的 s 的行索引
selected_columns_history = []  # 记录所有选中的列
answer_matrix = []  # 存储最终匹配的 k 的行

while len(covered_rows) < len(arr_s):
    # 统计未被覆盖的行中每列的 0 的个数
    column_zero_counts = [0] * n
    for row_idx, row in enumerate(arr_s):
        if row_idx not in covered_rows:
            for col in range(n):
                if row[col] == 0:
                    column_zero_counts[col] += 1

    # 选择 0 最多的列（并列时随机）
    max_zero = max(column_zero_counts)
    candidates = [col for col, count in enumerate(column_zero_counts) if count == max_zero]
    selected_col = random.choice(candidates)
    selected_columns_history.append(selected_col)

    # 找到 k 矩阵中对应行并添加到答案
    row_index = len(arr_k) - selected_col - 1
    answer_matrix.append(arr_k[row_index])

    # 标记新覆盖的 s 的行（这些行的 selected_col 列为 0）
    for row_idx, row in enumerate(arr_s):
        if row[selected_col] == 0:
            covered_rows.add(row_idx)

    print(f"选中列 {selected_col}，新增覆盖 {column_zero_counts[selected_col]} 行，已覆盖总数：{len(covered_rows)}")

print("\n最终选中的列：", selected_columns_history)
print("\n匹配的 k 矩阵行：")

# 替换answer_matrix中的1并压缩0维度
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