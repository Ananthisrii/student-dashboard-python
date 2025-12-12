from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            course TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# ---------- ROUTES ----------
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=data)


@app.route("/add")
def add_student():
    return render_template("add.html")


@app.route("/add_student", methods=["POST"])
def add_student_post():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students(name, email, course) VALUES (?, ?, ?)",
                   (name, email, course))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:id>")
def edit(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template("edit.html", student=student)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students SET name=?, email=?, course=? WHERE id=?
    """, (name, email, course, id))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
