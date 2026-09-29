from flask import Flask, jsonify
import redis
import os
import mysql.connector


app = Flask(__name__)


# MySQL configuration
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")
DB_NAME = os.getenv("DB_NAME", "appdb")


# Redis connection
redis_client = redis.StrictRedis(
    host="redis",
    port=6379,
    db=0
)


# Get visitor count
@app.route("/api", methods=["GET"])
def index():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cur = conn.cursor()

    cur.execute("SELECT count FROM visitors WHERE id = 1")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "visitors": row[0]
    })


# Get current MySQL server time
@app.get("/api/time")
def time():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cur = conn.cursor()

    cur.execute("SELECT NOW()")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "mysql_time": str(row[0])
    })


# Increase visitor count using Redis
@app.post("/api/visit")
def visit():
    count = redis_client.incr("visitor_count")

    return jsonify({
        "visitors": count
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )