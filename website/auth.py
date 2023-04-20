from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for("auth.Login"))


@auth.route("/login", methods=['GET', 'POST'])
def Login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user)
                return redirect(url_for("views.Home"))
            else:
                flash("Incorrect password!", category="error")
        else:
            flash("Email does not exist!", category="error")

    return render_template("Login.html", user=current_user)


@auth.route("/signup", methods=['GET', 'POST'])
def SignUp():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        password = request.form.get("password")
        confirmation = request.form.get("password_confirm")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exist!", category="error")
        elif len(email) < 4:
            flash("Email must be longer then 3 character.", category="error")
        elif len(first_name) < 2:
            flash("First name must be longer then 1 character.", category="error")
        elif len(password) < 8:
            flash("Password must be at least 7 character.", category="error")
        elif password != confirmation:
            flash("Passwords don't match.", category="error")
        else:
            new_user = User(email=email, first_name=first_name.title(),
                            last_name=last_name.title(), password=generate_password_hash(password, 'sha256'),is_admin=True)
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            flash("Account created!", category="success")
            return redirect(url_for("views.Home"))
    return render_template("SignUp.html", user=current_user)
