# version 2025/4/27 测试k=6固定的所有情况 这个是通过request的
# version 2025/4/27 直接测试算法而不是给前端发消息了 那个格式解析没处理liao

import math
import random
from algorithm import run_algorithm

# 固定 k 为 6
k = 6

# 遍历所有可能的 m, n, j, s, at_least_s 和 n_mode
m_values = range(45, 55)  # 45 ≤ m ≤ 54
n_values = range(7, 26)   # 7 ≤ n ≤ 25
s_values = range(3, 8)
# 遍历所有可能的组合并发送请求
for n in n_values:
    random_numbers = random.sample(range(1, 100), n) 
    for s in range(k, 2, -1):  # s 必须小于或等于 k
        j_values = range(s, k + 1) # 必须在循环里面处理j的值
        for j in range(s, k + 1):  # j 必须小于或等于 k 且大于或等于 s
            comb = math.comb(j, s)
            at_least_s_values = range(1, comb + 1)
            for at_least_s in range(1, comb + 1):
                # 构建请求数据
                data = {
                    'action': 'execute',  # 执行算法
                    'm': 45, # 固定
                    'n': n,
                    'k': k,
                    'j': j,
                    's': s,
                    'at_least_s': at_least_s,
                    'n_mode': 'random',
                }
                result_matrix, total_time = run_algorithm(n, k, j, s, random_numbers, at_least_s)

                # 保存结果到文件
                with open('flask_demo\\test_result.txt', 'a') as file:
                    file.write(f"Parameters (n, k, j, s): ({n}, {k}, {j}, {s})")
                    file.write(f"Result Matrix: {len(result_matrix)}")
                    file.write(f"Total Time: {total_time:.4f}\n")
                    print("test\n")