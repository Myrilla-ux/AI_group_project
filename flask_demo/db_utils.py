import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',               # ← change to your username
    password='abcd1234',        # ← your password
    database='optimal_samples',
    charset='utf8mb4'
)

def save_to_db(identifier, groups):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO results (identifier, sample_groups) VALUES (%s, %s)"
            cursor.execute(sql, (identifier, str(groups)))
        conn.commit()
    except Exception as e:
        print("Fail to write to Database：", e)

def get_all_results():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM results")
        return cursor.fetchall()
