import os
import time
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "taxi-booking-super-secret-key"

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "taxidb")
DB_USER = os.getenv("POSTGRES_USER", "taxiuser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "taxipass")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, cursor_factory=RealDictCursor
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    raise Exception("Không thể kết nối tới PostgreSQL")

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session.get("username"), role=session.get("role"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("admin_dashboard") if user["role"] == "admin" else url_for("index"))
        flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'customer');", (username, password))
            conn.commit()
            cur.close()
            conn.close()
            flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            return redirect(url_for("login"))
        except Exception:
            flash("Tên đăng nhập đã tồn tại!", "danger")
    return render_template("register.html")

@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("history.html", username=session.get("username"))

@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html", username=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/api/rides", methods=["GET", "POST"])
def manage_rides():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "GET":
        if session.get("role") == "admin":
            cur.execute("SELECT r.*, u.username FROM rides r JOIN users u ON r.user_id = u.id ORDER BY r.created_at DESC;")
        else:
            cur.execute("SELECT * FROM rides WHERE user_id = %s ORDER BY created_at DESC;", (session["user_id"],))
        rides = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "data": rides})
    elif request.method == "POST":
        data = request.json or {}
        cur.execute(
            "INSERT INTO rides (user_id, passenger_name, pickup_location, dropoff_location) VALUES (%s, %s, %s, %s) RETURNING id;",
            (session["user_id"], data.get("passenger_name", session["username"]), data.get("pickup_location"), data.get("dropoff_location")),
        )
        new_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "ride_id": new_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
