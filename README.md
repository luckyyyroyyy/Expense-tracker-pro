# 💸 Expense Tracker Pro (Flask + Python)

A modern, colorful and dynamic Expense Tracking Web Application built using Flask, Python, SQLite, HTML, CSS, and Matplotlib.

This project allows users to register, login, add daily expenses, visualize spending through professional charts, and download expense reports as CSV.

---

## 🚀 Features

- User Registration & Login System
- Add, Edit, Delete Expenses
- Pie Chart & Histogram for expense analysis
- Date-wise expense tracking
- Download expense report as CSV
- Modern, colorful, professional UI
- Dynamic dashboard with charts
- Session-based authentication
- SQLite Database integration

---

## 🛠 Tech Stack

- Python
- Flask
- SQLite
- HTML / CSS
- Matplotlib
- Jinja2

---

## 📂 Project Structure

Expense-tracker-pro/
│
├── app.py
├── expenses.db
├── report.csv
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_expense.html
│   └── edit_expense.html
│
├── static/
│   ├── style.css
│   └── charts/
│       ├── pie.png
│       └── hist.png

---

## ⚙️ Installation & Run Locally

### Step 1 — Clone the repository

git clone https://github.com/luckyyyroyyy/Expense-tracker-pro.git  
cd Expense-tracker-pro

### Step 2 — Install dependencies

pip install -r requirements.txt

### Step 3 — Run the application

python app.py

Open browser and go to:

http://127.0.0.1:5000

---

## 📈 Charts & Reports

- Pie chart shows category-wise expense distribution
- Histogram shows expense frequency
- CSV report downloads all expenses with date, category, note, and amount

---

## 🔑 Default Workflow

1. Register a new account
2. Login
3. Add expenses
4. View dashboard with charts
5. Edit/Delete if needed
6. Download report

---

## 🎯 Purpose of Project

This project is developed as a BCA Final Year Project to demonstrate:

- Flask web development
- Database handling
- Authentication system
- Data visualization
- Professional UI design

---

## 👨‍💻 Author

Lucky Roy  
BCA Final Year Student

---

## 📌 Future Improvements

- Monthly/Yearly filters
- Export report as PDF
- Dark mode
- Category icons
- Cloud database deployment