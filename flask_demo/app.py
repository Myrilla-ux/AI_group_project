from flask import Flask, render_template, request
from algorithm import run_algorithm
import random
import time

app = Flask(__name__)


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
            # start_time = time.time()
            compressed_answer = run_algorithm(n=n, k=k, j=j, s=s, random_numbers=random_numbers,t=at_least_s)
            # #----------------------------换行输出------------------------------------#
            # result_matrix, _ = compressed_answer
            # for i, row in enumerate(result_matrix):
            #     print(f"行{i}: {' '.join(map(str, row))}")
            # #------------------------------------------------------------------#
            # total_time = time.time() - start_time
            # result_matrix, _ = compressed_answer
            _, total_time = compressed_answer
            result = {
                'answers': [
                    f"Running time: {total_time:.6f} seconds",
                    f"Sample size: {len(compressed_answer[0])}"
                ] + [f"results{i}: {' '.join(map(str, row))}" for i, row in enumerate(compressed_answer[0])]
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
