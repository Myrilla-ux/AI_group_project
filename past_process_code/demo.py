# version 2025/3/17 生成三个矩阵 s和k可以按位与；下一步：权重标号实现
# version 2025/3/25 这个k s按位与不太对呀

import random 
import itertools
import numpy as np

n = 7
k = 6
j = 5
s = 4

random_numbers = random.sample(range(1,46),7)

#sorted_numbers = sorted(random_numbers)

print("n:", random_numbers)

#------------------生成k的01矩阵---------------------------------#
positions_k = list(itertools.combinations(range(n),k))

arr_k = []
for pos in positions_k:
    binary_k = [0] * n #初始化为0 你初始化为1还要快一点
    for p in pos:
        binary_k[p] = 1 #选中的设为1
    arr_k.append(binary_k) #添加到二维数组中

for binary_k in arr_k:
    print(binary_k)# 检查一下 后面不用
print('n / k',n,'/',k)
#------------------------------------------------------------------#

#----------------------------生成s矩阵-------------------------------#
positions_s = list(itertools.combinations(range(n),s))

arr_s = []
for pos in positions_s:
    binary_s = [0] * n #初始化为0 你初始化为1还要快一点
    for p in pos:
        binary_s[p] = 1 #选中的设为1
    arr_s.append(binary_s) #添加到二维数组中

##----------------权重------------##
# 统计每一列的0的个数 #三个循环包慢的 不过后面来改
column_zero_counts = [0] * n
for row in arr_s:
    for col in range(n):
        if row[col] == 0:
            column_zero_counts[col] += 1

print(column_zero_counts)
##-------0最多的n-k列--------------##
num_to_select = n-k
column_zero_counts = [sum(1 for row in arr_s if row[col] == 0) for col in range(n)]
print("每一列的 0 的个数:", column_zero_counts)

# 将列按 0 的个数从高到低排序，并列的列随机排序
columns_sorted = sorted(
    range(n),
    key=lambda col: (-column_zero_counts[col], random.random())
    # -column_zero_counts[col] 降序，random.random() 并列时随机
)

# 选择前 num_to_select 列
selected_columns = columns_sorted[:num_to_select]
print(f"随机选择的 {num_to_select} 列索引:", selected_columns)
##------------------------------##
# for binary_s in arr_s:
#     print(binary_s)# 检查一下 后面不用
# print('n / s',n,'/',s)
#====================================================#


###############################################################################################
# 初始化
covered_rows = set()  # 记录已被覆盖的 s 的行索引
selected_columns_history = []  # 记录所有选中的列
answer_matrix = []  # 存储最终匹配的 k 的行


#----------找所选列对应的k（答案）-----------------------------#
selected_col = selected_columns #这是上面s选出来的0最多的列
answer_matrix = []
# 遍历每一列，找到对应的行
for col in selected_columns:
    row_index = len(arr_k) - col - 1  # 计算行号
    answer_matrix.append(arr_k[row_index])  # 添加到答案矩阵

print("匹配的行：")
for row in answer_matrix:
    print(row)


































##################################################################################
# 后续会用到的代码

#--------------------------生成j矩阵--------------------------------#
positions_j = list(itertools.combinations(range(n),j))

arr_j = []
for pos in positions_j:
    binary_j = [0] * n #初始化为0 你初始化为1还要快一点
    for p in pos:
        binary_j[p] = 1 #选中的设为1
    arr_j.append(binary_j) #添加到二维数组中

# for binary_j in arr_j:
#     print(binary_j)# 检查一下 后面不用
# print('n / k',n,'/',j)
#-------------------------------------------------------------------#