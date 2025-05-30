# version 2025/4/1 解决k有多个0的问题

import random
import itertools
import time
start_time = time.time()


n = 8
k = 6
j = 5
s = 4
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

# 初始化
covered_rows_s = set()  # 记录已被覆盖的 s 的行索引
covered_rows_k = [] # 存储选中的列为0的行索引
answer_matrix = []  # 存储最终匹配的 k 的行
selected_combinations = set() # 已被选择的组合情况 要再外面初始化

while len(covered_rows_s) < len(arr_s):
    # 统计未被覆盖的行中每列的 0 的个数
    column_zero_counts = [0] * n
    for row_idx, row in enumerate(arr_s):
        if row_idx not in covered_rows_s:
            for col in range(n):
                if row[col] == 0:
                    column_zero_counts[col] += 1

    # 选择 0 最多的列（并列时会是排前面的 不是故意的 是程序这样）
    # 这里如果s和k都有多个0就要按照k的来 k有几个就选几个 k的零一定比s少 "num_zeros_k"
    sorted_counts = sorted(enumerate(column_zero_counts), key=lambda x: x[1], reverse=True)# 获取零的数量和对应列的索引，并按照零的数量从多到少排序
    selected_col = [] # 选择零最多的列
    current_combination = []  # 当前选中的列组合
    remaining_count = num_zeros_k
    # 填充零最多的列
    for col, count in sorted_counts:
        if remaining_count == 0:
            break
        selected_col.append(col)
        current_combination.append(col) # 添加当前选中的组合 以组合为基础判断是否重复
        remaining_count -= 1
    # 如果零最多的列不够a列，继续选择零次多的列
    if remaining_count > 0:
        for col, count in sorted_counts:
            if count < sorted_counts[remaining_count-1][1]:
                selected_col.append(col)
                current_combination.append(col)
                remaining_count -= 1
            if remaining_count == 0:
                break

    print(selected_col)

    #-------------------给已选择组合查重-----------------------#
    # 将当前选择的列组合转化为元组并检查是否已经选中过
    current_combination = tuple(sorted(current_combination))  # 转化为元组，并按升序排序，以避免相同组合但顺序不同的情况

    # 检查是否已经选过该组合
    if current_combination in selected_combinations:
        print(f"组合 {current_combination} 已经选择过，跳过。")
        continue  # 如果该组合已选过，则跳过本次循环 ！！！这里有一个回溯可以讲！！！！！

    # 如果没有选过该组合，则将其加入已选组合集合
    selected_combinations.add(current_combination)
    print(f"已选中的列组合: {selected_combinations}")
    #-------------------------------------------------------------#

    # 找到 k 矩阵中对应行并添加到答案
    # 遍历 K 矩阵的每一行
    for row_idx, row in enumerate(arr_k):
        # 检查选中列中的每个列是否为0
        if all(row[col] == 0 for col in selected_col) and row_idx not in covered_rows_k:  # 如果选中的列都为0
            covered_rows_k.append(row_idx)
    print("选中列为0的k行索引：", covered_rows_k)

    # 标记新覆盖的 s 的行（这些行的 selected_col 列为 0）
    for row_idx, row in enumerate(arr_s):
        if all(row[col] == 0 for col in selected_col)and row_idx not in covered_rows_s:  # 如果所有选中的列都为0 选过的不能再选
            covered_rows_s.add(row_idx)
            print(f"选中s行 {row_idx}，已覆盖总数：{len(covered_rows_s)}")

answer_matrix = [arr_k[row_idx] for row_idx in covered_rows_k]    
print("\n最终选中的列：", covered_rows_k)
print("\n匹配的 k 矩阵行：")

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