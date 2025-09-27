from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import auth_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        if not email or not password:
            flash("Попълнете всички полета.", "error")
            return redirect(url_for("auth.register"))

        # опитай да регистрираш (вероятно ще върне None при duplicate)
        user = auth_service.register_user(email, password)
        if user is None:
            flash("Потребител с този имейл вече съществува.", "error")
            return redirect(url_for("auth.register"))

        flash("Регистрацията е успешна. (Потвърждение е отпечатано в конзолата.)", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        user = auth_service.login_user(email, password)
        if not user:
            flash("Грешен имейл или парола.", "error")
            return redirect(url_for("auth.login"))

        # съхраняваме сесия
        session["user_id"] = user["id"]
        session["is_admin"] = user.get("is_admin", False)
        flash("Влязохте успешно.", "success")
        return redirect(url_for("catalog.catalog"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("is_admin", None)
    flash("Излязохте.", "info")
    return redirect(url_for("auth.login"))
