from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key="expense_secret"

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect("expense.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- CREATE TABLE ----------
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            expense_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------- GENERATE CHARTS ----------
def generate_charts():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return

    os.makedirs("static/charts", exist_ok=True)

    # -------- PIE CHART (Category-wise) --------
    category_sum = df.groupby("category")["amount"].sum()
    plt.figure(figsize=(6, 6))
    category_sum.plot.pie(autopct='%1.1f%%', startangle=140)
    plt.title("Category-wise Expenses")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("static/charts/pie.png")
    plt.close()

    # -------- BAR CHART (Monthly) --------
    df["month"] = pd.to_datetime(df["expense_date"]).dt.to_period("M").astype(str)
    monthly_sum = df.groupby("month")["amount"].sum()
    plt.figure(figsize=(7, 4))
    monthly_sum.plot(kind="bar")
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("static/charts/bar.png")
    plt.close()

    # -------- LINE CHART (Daily Trend) --------
    daily_sum = df.groupby("expense_date")["amount"].sum()
    plt.figure(figsize=(7, 4))
    daily_sum.plot(marker="o")
    plt.title("Spending Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("static/charts/line.png")
    plt.close()


# ---------- DASHBOARD ----------
@app.route("/")
def dashboard():
    generate_charts()

    conn = get_db_connection()
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC"
    ).fetchall()
    conn.close()

    total = sum(exp["amount"] for exp in expenses)

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total=total
    )


# ---------- ADD EXPENSE ----------
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        note = request.form.get("note", "")
        expense_date = request.form["date"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (amount, category, note, expense_date) VALUES (?, ?, ?, ?)",
            (amount, category, note, expense_date)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")


# ---------- RUN APP ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# ✅ REQUIRED FOR FLASH MESSAGES
app.secret_key = "expense_secret"


# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect("expense.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- CREATE TABLE ----------
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            expense_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------- GENERATE CHARTS ----------
def generate_charts():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return

    os.makedirs("static/charts", exist_ok=True)

    # -------- PIE CHART (Category-wise) --------
    category_sum = df.groupby("category")["amount"].sum()
    plt.figure(figsize=(6, 6))
    category_sum.plot.pie(autopct='%1.1f%%', startangle=140)
    plt.title("Category-wise Expenses")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("static/charts/pie.png")
    plt.close()

    # -------- BAR CHART (Monthly) --------
    df["month"] = pd.to_datetime(df["expense_date"]).dt.to_period("M").astype(str)
    monthly_sum = df.groupby("month")["amount"].sum()
    plt.figure(figsize=(7, 4))
    monthly_sum.plot(kind="bar")
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("static/charts/bar.png")
    plt.close()

    # -------- LINE CHART (Daily Trend) --------
    daily_sum = df.groupby("expense_date")["amount"].sum()
    plt.figure(figsize=(7, 4))
    daily_sum.plot(marker="o")
    plt.title("Spending Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("static/charts/line.png")
    plt.close()


# ---------- DASHBOARD ----------
@app.route("/")
def dashboard():
    generate_charts()

    conn = get_db_connection()
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC"
    ).fetchall()
    conn.close()

    total = sum(exp["amount"] for exp in expenses)

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total=total
    )


# ---------- ADD EXPENSE ----------
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        note = request.form.get("note", "")
        expense_date = request.form["date"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (amount, category, note, expense_date) VALUES (?, ?, ?, ?)",
            (amount, category, note, expense_date)
        )
        conn.commit()
        conn.close()

        # ✅ FLASH MESSAGE ADDED HERE
        flash("Expense added successfully!", "success")

        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")


# ---------- RUN APP ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)