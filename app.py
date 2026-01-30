from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
import os
import csv

app = Flask(__name__)
app.secret_key = "expense_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# Database Model
# ======================
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200))
    expense_date = db.Column(db.Date, default=datetime.utcnow)

# ======================
# Create DB
# ======================
with app.app_context():
    db.create_all()

# ======================
# Home / Dashboard
# ======================
@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    total = sum(e.amount for e in expenses)

    generate_charts(expenses)

    return render_template(
        'dashboard.html',
        expenses=expenses,
        total=total
    )

# ======================
# Add Expense
# ======================
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        new_expense = Expense(
            amount=float(request.form['amount']),
            category=request.form['category'],
            note=request.form['note'],
            expense_date=datetime.strptime(request.form['date'], '%Y-%m-%d')
        )

        db.session.add(new_expense)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_expense.html')

# ======================
# Edit Expense
# ======================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']
        expense.note = request.form['note']
        expense.expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        db.session.commit()
        flash('Expense updated successfully!', 'info')
        return redirect(url_for('index'))

    return render_template('edit_expense.html', expense=expense)

# ======================
# Delete Expense
# ======================
@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

# ======================
# Generate Charts
# ======================
def generate_charts(expenses):
    chart_dir = os.path.join(BASE_DIR, 'static', 'charts')
    os.makedirs(chart_dir, exist_ok=True)

    categories = {}
    monthly = {}

    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + e.amount
        month = e.expense_date.strftime('%b')
        monthly[month] = monthly.get(month, 0) + e.amount

    if categories:
        plt.figure()
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title('Category-wise Expenses')
        plt.savefig(os.path.join(chart_dir, 'pie.png'))
        plt.close()

    if monthly:
        plt.figure()
        plt.bar(monthly.keys(), monthly.values())
        plt.title('Monthly Expenses')
        plt.savefig(os.path.join(chart_dir, 'bar.png'))
        plt.close()

        plt.figure()
        plt.plot(list(monthly.keys()), list(monthly.values()), marker='o')
        plt.title('Expense Trend')
        plt.savefig(os.path.join(chart_dir, 'line.png'))
        plt.close()

# ======================
# Report Download (CSV) ✅ FIXED
# ======================
@app.route('/report')
def report():
    file_path = os.path.join(BASE_DIR, 'expense_report.csv')
    expenses = Expense.query.all()

    # 🔥 FIX IS HERE (UTF-8)
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Category', 'Note', 'Amount'])
        for e in expenses:
            writer.writerow([
                e.expense_date.strftime('%Y-%m-%d'),
                e.category,
                e.note,
                e.amount
            ])

    return send_file(file_path, as_attachment=True)

# ======================
# Run App
# ======================
if __name__ == '__main__':
    app.run(debug=True)