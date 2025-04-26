from flask import Flask, render_template, request, redirect, url_for, flash
from algorithm import run_algorithm
from db_utils import save_to_db, get_all_results, delete_result_by_id

import random
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# ✅ 用于缓存最近一次执行的结果
last_result_matrix = None
last_random_numbers = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_result_matrix, last_random_numbers

    result = None
    value_input = ''
    input_n_values = []

    if request.method == 'POST':
        try:
            action = request.form.get('action')
            m = int(request.form.get('m'))
            n = int(request.form.get('n'))
            k = int(request.form.get('k'))
            j = int(request.form.get('j'))
            s = int(request.form.get('s'))
            at_least_s = int(request.form.get('at_least_s'))
            n_mode = request.form.get('n_mode')

            if action == 'clear':
                last_result_matrix = None
                last_random_numbers = []
                return render_template("index.html",
                                       result=None,
                                       value_input='',
                                       input_n_values=[])

            # 获取 n 的值
            if n_mode == 'random':
                random_numbers = random.sample(range(1, m + 1), n)
                input_n_values = []
            else:
                input_n_values = [request.form.get(f"input_n_{i}", '') for i in range(1, n + 1)]
                random_numbers = [int(x) for x in input_n_values if x.strip().isdigit()]

            value_input = ', '.join(str(x) for x in random_numbers)

            if action == 'execute':
                result_matrix, total_time = run_algorithm(
                    n=n, k=k, j=j, s=s, random_numbers=random_numbers, t=at_least_s
                )
                last_result_matrix = result_matrix
                last_random_numbers = random_numbers

                result = {
                    'answers': [
                        f"Running time: {total_time:.6f} seconds",
                        f"Sample size: {len(result_matrix)}"
                    ] + [f"results{i+1}: {' '.join(map(str, row))}" for i, row in enumerate(result_matrix)]
                }

            elif action == 'store':
                if last_result_matrix is None:
                    flash("⚠️ Please execute the algorithm before storing.", "warning")
                    return render_template("index.html", result=None,
                                           value_input=value_input,
                                           input_n_values=input_n_values)

                optimal_count = len(last_result_matrix)
                identifier = f"{m}-{n}-{k}-{j}-{s}-{at_least_s}-{optimal_count}"

                try:
                    save_to_db(identifier, last_result_matrix, last_random_numbers)
                    result = {
                        'answers': [
                            f"✅ Stored to DB with ID: {identifier}",
                            f"Total optimal groups: {optimal_count}"
                        ]
                    }
                except Exception as e:
                    result = {'answers': [f"🔥 DB Error: {str(e)}"]}
                    print("🔥 Store error:", e)
                    print("Detailed error:", str(e))

        except Exception as e:
            result = {
                'answers': [f"Error: {str(e)}"]
            }

    return render_template("index.html",
                           result=result,
                           value_input=value_input,
                           input_n_values=input_n_values)

@app.route('/results')
def show_results():
    records = get_all_results()
    return render_template('results.html', records=records)

@app.route('/delete_record', methods=['POST'])
def delete_record():
    record_id = request.form.get('id')
    if record_id:
        delete_result_by_id(record_id)
        flash(f"✅ Deleted record ID: {record_id}")
    else:
        flash("Error: Missing record ID")
    return redirect(url_for('show_results'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
