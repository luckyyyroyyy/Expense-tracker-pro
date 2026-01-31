from flask import send_file
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import matplotlib.pyplot as plt
import os, csv

app = Flask(__name__)
app.secret_key = "secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= MODELS =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    category = db.Column(db.String(100))
    note = db.Column(db.String(200))
    expense_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

# ============== LOGIN REQUIRED ==============
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

# ================= REGISTER =================
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for('register'))

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Login now.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ================= LOGIN =================
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('index'))

        flash("Invalid credentials", "danger")

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= DASHBOARD =================
@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=session['user_id']).order_by(Expense.expense_date.desc()).all()
    total = sum(e.amount for e in expenses)

    generate_charts(expenses)

    return render_template('dashboard.html', expenses=expenses, total=total)

# ================= ADD =================
@app.route('/add', methods=['GET','POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        expense = Expense(
            amount=float(request.form['amount']),
            category=request.form['category'],
            note=request.form['note'],
            expense_date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
            user_id=session['user_id']
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_expense.html')

# ================= EDIT =================
@app.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']
        expense.note = request.form['note']
        expense.expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_expense.html', expense=expense)

# ================= DELETE =================
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

# ================= CHARTS =================
def generate_charts(expenses):
    chart_dir = os.path.join(BASE_DIR, 'static', 'charts')
    os.makedirs(chart_dir, exist_ok=True)

    categories = {}
    amounts = []

    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + e.amount
        amounts.append(e.amount)

    # Pie
    if categories:
        plt.figure()
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.savefig(os.path.join(chart_dir, 'pie.png'))
        plt.close()

    # Histogram
    if amounts:
        plt.figure()
        plt.hist(amounts, bins=5)
        plt.title("Expense Distribution")
        plt.savefig(os.path.join(chart_dir, 'hist.png'))
        plt.close()

# ================= CSV REPORT =================
@app.route('/report')
@login_required
def report():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    with open('report.csv', 'w') as f:
        f.write('Category,Amount,Note,Date\n')
        for e in expenses:
            f.write(f'{e.category},{e.amount},{e.note},{e.date}\n')

    return send_file('report.csv', as_attachment=True)

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)