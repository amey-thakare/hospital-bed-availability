print("THIS app.py IS RUNNING")

from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = "super_secret_key"

def get_hospitals():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, available_beds FROM hospitals")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------- USER DASHBOARD ----------
@app.route("/")
def user_dashboard():
    hospitals = get_hospitals()
    return render_template("user_dashboard.html", hospitals=hospitals)

# ---------- HOSPITAL LOGIN ----------
@app.route("/hospital/login", methods=["GET", "POST"])
def hospital_login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM hospital_users WHERE name=?",
            (name,)
        )
        row = cursor.fetchone()
        conn.close()

        if row and check_password_hash(row[0], password):
            session["hospital"] = name
            return redirect("/hospital/dashboard")
        else:
            return "Invalid login"

    return render_template("hospital_login.html")

@app.route("/hospital/dashboard")
def hospital_dashboard():
    if "hospital" not in session:
        return redirect("/hospital/login")

    name = session["hospital"]

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT available_beds FROM hospitals WHERE name=?",
        (name,)
    )
    beds = cursor.fetchone()[0]
    conn.close()

    return render_template(
        "hospital_dashboard.html",
        name=name,
        beds=beds
    )

@app.route("/hospital/update", methods=["POST"])
def update_beds():
    if "hospital" not in session:
        return redirect("/hospital/login")

    beds = request.form["beds"]
    name = session["hospital"]

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE hospitals SET available_beds=? WHERE name=?",
        (beds, name)
    )
    conn.commit()
    conn.close()

    return redirect("/hospital/dashboard")

@app.route("/hospital/signup", methods=["GET", "POST"])
def hospital_signup():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        beds = request.form["beds"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        try:
            # Insert login credentials
            cursor.execute(
                "INSERT INTO hospital_users (name, password) VALUES (?, ?)",
                (name, hashed_password)
            )

            # Insert hospital data
            cursor.execute(
                "INSERT INTO hospitals (name, available_beds) VALUES (?, ?)",
                (name, beds)
            )

            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Hospital already exists"

        conn.close()
        return redirect("/hospital/login")

    return render_template("hospital_signup.html")


@app.route("/hospital/logout")
def hospital_logout():
    session.pop("hospital", None)
    return redirect("/hospital/login")



# ---------- RUN SERVER (ALWAYS LAST) ----------
if __name__ == "__main__":
    app.run()
