from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)

def run_algorithm(n, k, j, s, random_numbers):
    # 模拟计算结果（你自己的算法逻辑替换这里）
    return [sorted(random.sample(random_numbers, k)) for _ in range(n)]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    value_input = ''
    input_n_values = []

    if request.method == 'POST':
        try:
            m = int(request.form.get('m'))
            n = int(request.form.get('n'))
            k = int(request.form.get('k'))
            j = int(request.form.get('j'))
            s = int(request.form.get('s'))
            at_least_s = int(request.form.get('at_least_s'))
            n_mode = request.form.get('n_mode')

            if n_mode == 'random':
                random_numbers = random.sample(range(1, m + 1), n)
                input_n_values = []
            else:
                input_n_values = [request.form.get(f"input_n_{i}", '') for i in range(1, n + 1)]
                random_numbers = [int(x) for x in input_n_values if x.strip().isdigit()]

            value_input = ', '.join(str(x) for x in random_numbers)

            # 调用算法并计时
            start_time = time.time()
            compressed_answer = run_algorithm(n=n, k=k, j=j, s=s, random_numbers=random_numbers)
            total_time = time.time() - start_time

            result = {
                'answers': [
                    f"Running time: {total_time:.6f} seconds",
                    f"Sample size: {len(compressed_answer)}"
                ] + [str(row) for row in compressed_answer]
            }

        except Exception as e:
            result = {
                'answers': [f"Error: {str(e)}"]
            }

    return render_template("index.html",
                           result=result,
                           value_input=value_input,
                           input_n_values=input_n_values)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5050)