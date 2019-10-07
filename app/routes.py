from flask import render_template, request, flash, redirect, url_for
from app import app
from datetime import datetime
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    user = {"username": "Miguel"}
    title = "Alienbook - log in or sign up"
    year = datetime.now().year
    form = LoginForm()
    if request.method == "POST":
        print(request, flush=True)
        if form.validate_on_submit():
            flash(f"Login requested for user {form.email.data}")
            return redirect(url_for("index"))
        else:
            return redirect(url_for("failed_login"))
    return render_template("index.html", title=title, user=user, year=year, form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = LoginForm()
    title = "Sign up for Alienbook | Alienbook"
    return render_template(
        "signup.html",
        title=title,
        hidden_menu=True,
        year=datetime.now().year,
        form=form,
    )


@app.route("/failed_login", methods=["POST", "GET"])
def failed_login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if request.method == "POST":
        print(request, flush=True)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return render_template(
                "failed_login.html", title="Log in to Alienbook | Alienbook", form=form
            )
        login_user(user)
        flash(f"Login successful for user {form.email.data}")
        return redirect(url_for("index"))
    return render_template(
        "failed_login.html", title="Log in to Alienbook | Alienbook", form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
