import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import db_config

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-only-key")


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# REGISTRATION
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        qualification = request.form["qualification"]

        hashed_password = generate_password_hash(password)

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = """
            INSERT INTO users
            (full_name, email, password, phone, qualification)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                full_name,
                email,
                hashed_password,
                phone,
                qualification
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            return "Registration Successful! Welcome to CareerLaunch."

        except mysql.connector.Error as error:
            return f"Registration Failed: {error}"

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user and check_password_hash(user["password"], password):

                session["user_id"] = user["id"]
                session["user_name"] = user["full_name"]

                return redirect("/dashboard")

            else:
                return "Invalid Email or Password."

        except mysql.connector.Error as error:
            return f"Login Failed: {error}"

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# RUN APPLICATION

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )