import pymysql
import os
import csv

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'optimal_samples',
    'charset': 'utf8mb4'
}

EXPORT_FILE = 'saved_results.csv'

# ✅ 存储函数
def save_to_db(identifier, result_matrix, n_values):
    result_text = '\n'.join([' '.join(map(str, row)) for row in result_matrix])
    n_values_str = ','.join(map(str, n_values))
    optimal_groups = len(result_matrix)

    # ✅ 插入数据库（仅两列）
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql = "INSERT INTO results (identifier, sample_groups) VALUES (%s, %s)"
    cursor.execute(sql, (identifier, result_text))
    conn.commit()
    conn.close()

    # ✅ 存入 CSV 文件（带额外字段）
    formatted_result = ', '.join([f"[{' '.join(map(str, row))}]" for row in result_matrix])
    write_header = not os.path.exists(EXPORT_FILE) or os.path.getsize(EXPORT_FILE) == 0

    with open(EXPORT_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['Identifier', 'Optimal Groups', 'n Values', 'Result'])
        writer.writerow([identifier, optimal_groups, n_values_str, formatted_result])

# ✅ 获取全部记录（从数据库 + CSV 合并）
def get_all_results():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, identifier, sample_groups FROM results ORDER BY id DESC")
    db_rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # 读取 CSV 作为附加信息
    csv_info = {}
    if os.path.exists(EXPORT_FILE):
        with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_info[row['Identifier']] = {
                    'optimal_groups': row['Optimal Groups'],
                    'n_values': row['n Values']
                }

    combined_rows = []
    for row in db_rows:
        record_id, identifier, sample_groups = row
        info = csv_info.get(identifier, {})
        optimal_groups = info.get('optimal_groups', 'N/A')
        n_values = info.get('n_values', 'N/A')
        combined_rows.append([record_id, identifier, optimal_groups, n_values, sample_groups])
    return combined_rows

# ✅ 删除记录（根据 identifier）
def delete_result(identifier):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql = "DELETE FROM results WHERE identifier = %s"
    cursor.execute(sql, (identifier,))
    conn.commit()
    conn.close()

# ✅ 删除记录（根据 ID 并同步删除 CSV）
def delete_result_by_id(record_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 查询记录内容
    cursor.execute("SELECT identifier FROM results WHERE id = %s", (record_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return

    identifier = row[0]

    # 从数据库删除
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM results WHERE id = %s", (record_id,))
    conn.commit()
    conn.close()

    # 从 CSV 删除
    if os.path.exists(EXPORT_FILE):
        with open(EXPORT_FILE, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

        header = rows[0]
        data_rows = rows[1:]
        new_rows = [header] + [r for r in data_rows if r[0] != identifier]

        with open(EXPORT_FILE, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(new_rows)
