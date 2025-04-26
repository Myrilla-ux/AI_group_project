import requests

# 设置 Flask 应用的基本 URL
base_url = 'http://127.0.0.1:5050'

# 固定 k 为 6
k = 6

# 遍历所有可能的 m, n, j, s, at_least_s 和 n_mode
m_values = [5, 10, 15]  # 你可以根据需要增加更多的 m 值
n_values = [3, 5, 7]  # 你可以根据需要增加更多的 n 值
j_values = [1, 2, 3]  # 你可以根据需要增加更多的 j 值
s_values = [1, 2, 3]  # 你可以根据需要增加更多的 s 值
at_least_s_values = [1, 2, 3]  # 你可以根据需要增加更多的 at_least_s 值
n_modes = ['random', 'manual']  # 选择手动输入或随机生成

# 遍历所有可能的组合并发送请求
for m in m_values:
    for n in n_values:
        for j in j_values:
            for s in s_values:
                for at_least_s in at_least_s_values:
                    for n_mode in n_modes:
                        # 构建请求数据
                        data = {
                            'action': 'execute',  # 执行算法
                            'm': m,
                            'n': n,
                            'k': k,
                            'j': j,
                            's': s,
                            'at_least_s': at_least_s,
                            'n_mode': n_mode,
                        }

                        if n_mode == 'manual':
                            # 如果选择手动输入，给出一些随机的 n 值作为示例
                            for i in range(1, n + 1):
                                data[f'input_n_{i}'] = str(i)

                        # 发送 POST 请求到 Flask 服务器
                        response = requests.post(f'{base_url}/', data=data)

                        # 打印响应内容
                        print(f"Test for m={m}, n={n}, j={j}, s={s}, at_least_s={at_least_s}, n_mode={n_mode}")
                        print("Response:", response.text)

# 如果你需要清除记录，可以发送清除请求
clear_data = {'action': 'clear'}
requests.post(f'{base_url}/', data=clear_data)
