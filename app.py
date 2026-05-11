from flask import Flask, jsonify, request
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    max_retries = 10
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
            return conn
        except Exception as e:
            print(f"Attempt {i+1}/{max_retries} failed: {e}")
            time.sleep(3)
    raise Exception("Could not connect to database")

@app.route('/')
def hello():
    return jsonify({"message": "Hello DevOps!"})

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data.get('username')
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO users (username) VALUES (%s) RETURNING id, username, created_at',
            (username,)
        )
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "id": user[0],
            "username": user[1],
            "created_at": str(user[2])
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, username, created_at FROM users')
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify([{
            "id": u[0],
            "username": u[1],
            "created_at": str(u[2])
        } for u in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
    app.run(host='0.0.0.0', port=8080)