import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name             = request.form.get("name", "").strip()
        email            = request.form.get("email", "").strip()
        password         = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name:
            return render_template("register.html", error="Full name is required.", name=name, email=email)
        if not email:
            return render_template("register.html", error="Email address is required.", name=name, email=email)
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match.", name=name, email=email)

        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash),
            )
            db.commit()
            db.close()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

        flash("Account created! Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html",
                                   error="Email and password are required.",
                                   email=email)

        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html",
                                   error="Invalid email or password.",
                                   email=email)

        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You've been signed out.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        flash("Please sign in to view your profile.", "error")
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2025",
        "initials": "D",
    }

    stats = {
        "total_spent": "₹12,450",
        "transaction_count": 8,
        "top_category": "Food",
    }

    transactions = [
        {"date": "Apr 14, 2026", "description": "Grocery run",      "category": "Food",          "amount": "₹1,200"},
        {"date": "Apr 12, 2026", "description": "Electricity bill",  "category": "Bills",         "amount": "₹2,300"},
        {"date": "Apr 10, 2026", "description": "Metro pass",        "category": "Transport",     "amount": "₹500"},
        {"date": "Apr 08, 2026", "description": "Pharmacy",          "category": "Health",        "amount": "₹850"},
        {"date": "Apr 05, 2026", "description": "Movie tickets",     "category": "Entertainment", "amount": "₹700"},
        {"date": "Apr 03, 2026", "description": "Lunch out",         "category": "Food",          "amount": "₹420"},
        {"date": "Apr 01, 2026", "description": "Amazon order",      "category": "Shopping",      "amount": "₹3,200"},
        {"date": "Mar 29, 2026", "description": "Cab fare",          "category": "Transport",     "amount": "₹280"},
    ]

    categories = [
        {"name": "Food",          "amount": "₹4,850", "percent": 39},
        {"name": "Shopping",      "amount": "₹3,200", "percent": 26},
        {"name": "Bills",         "amount": "₹2,300", "percent": 18},
        {"name": "Health",        "amount": "₹850",   "percent": 7},
        {"name": "Entertainment", "amount": "₹700",   "percent": 6},
        {"name": "Transport",     "amount": "₹780",   "percent": 6},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
