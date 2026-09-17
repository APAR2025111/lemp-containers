from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")
DB_NAME = os.getenv("DB_NAME", "appdb")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api")
def index():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cur = conn.cursor()

    # READ data from MySQL
    cur.execute("SELECT count FROM visitors WHERE id = 1")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "visitors": row[0]
    })


@app.get("/api/time")
def time():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cur = conn.cursor()

    # READ current server time from MySQL
    cur.execute("SELECT NOW()")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "mysql_time": str(row[0])
    })


@app.post("/api/visit")
def visit():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cur = conn.cursor()

    # WRITE data to MySQL
    cur.execute(
        "UPDATE visitors SET count = count + 1 WHERE id = 1"
    )

    conn.commit()

    # READ the new value
    cur.execute("SELECT count FROM visitors WHERE id = 1")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "visitors": row[0]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
