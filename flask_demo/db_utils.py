import pymysql

# ✅ MySQL 连接信息（请根据你实际情况修改）
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'optimal_samples',
    'charset': 'utf8mb4'
}

def save_to_db(identifier, result_matrix):
    result_text = '\n'.join([' '.join(map(str, row)) for row in result_matrix])

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql = "INSERT INTO results (identifier, sample_groups) VALUES (%s, %s)"
    cursor.execute(sql, (identifier, result_text))
    conn.commit()
    conn.close()

def get_all_results():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, identifier, sample_groups FROM results ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_result(identifier):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql = "DELETE FROM results WHERE identifier = %s"
    cursor.execute(sql, (identifier,))
    conn.commit()
    conn.close()
    
def delete_result_by_id(record_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql = "DELETE FROM results WHERE id = %s"
    cursor.execute(sql, (record_id,))
    conn.commit()
    conn.close()
