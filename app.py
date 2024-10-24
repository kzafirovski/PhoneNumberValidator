import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup

#configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#Create database

db = SQL("sqlite:///project.db")

connection = sqlite3.connect('project.db')

cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS numbers (
               id INTEGER PRIMARY KEY,
               valid TEXT NOT NULL,
               number INTEGER,
               local_format INTEGER,
               international_format TEXT NOT NULL,
               country_prefix TEXT NOT NULL,
               country_code TEXT NOT NULL,
               country_name TEXT NOT NULL,
               location TEXT NOT NULL,
               carrier TEXT NOT NULL,
               line_type TEXT NOT NULL
               )
               ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               hash TEXT NOT NULL
               )
               ''')


connection.close()


@app.route("/")
@login_required
def index():
    users = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("MISSING USERNAME")

        if not request.form.get("password"):
            return apology("MISSING PASSWORD")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if not (username := request.form.get("username")):
            return apology("MISSING USERNAME")

        if not (password := request.form.get("password")):
            return apology("MISSING PASSWORD")

        if not (confirmation := request.form.get("confirmation")):
            return apology("PASSWORD DON'T MATCH")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # Ensure username not in database
        if len(rows) != 0:
            return apology(f"The username '{username}' already exists. Please choose another name.")

        # Ensure first password and second password are matched
        if password != confirmation:
            return apology("password not matched")

        # Insert username into database
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                        username, generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = id

        flash("Registered!")

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    if request.method == "POST":
        if not (password := request.form.get("password")):
            return apology("MISSING OLD PASSWORD")

        rows = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("INVALID PASSWORD")

        if not (new_password := request.form.get("new_password")):
            return apology("MISSING NEW PASSWORD")

        if not (confirmation := request.form.get("confirmation")):
            return apology("MISSING CONFIRMATION")

        if new_password != confirmation:
            return apology("PASSWORD NOT MATCH")

        db.execute("UPDATE users set hash = ? WHERE id = ?;",
                   generate_password_hash(new_password), session["user_id"])

        flash("Password reset successful!")

        return redirect("/")
    else:
        return render_template("reset.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        # Ensure Symbol is exists
        if not (query := lookup(request.form.get("number"))):
            return apology("INVALID SYMBOL")

        return render_template("search.html", query=query)
    else:
        return render_template("search.html")

@app.route("/record", methods=['POST'])
def record():
    # Extract data from the form
    valid = request.form.get("valid")
    number = request.form.get("number")
    local_format = request.form.get("local_format")
    international_format = request.form.get("international_format")
    country_prefix = request.form.get("country_prefix")
    country_code = request.form.get("country_code")
    country_name = request.form.get("country_name")
    location = request.form.get("location")
    carrier = request.form.get("carrier")
    line_type = request.form.get("line_type")

    # Convert fields to appropriate types if necessary
    number = int(number)
    local_format = int(local_format)

    # Connect to the SQLite database
    connection = sqlite3.connect('project.db')
    cursor = connection.cursor()

    # Insert the data into the numbers table
    cursor.execute('''
        INSERT INTO numbers (valid, number, local_format, international_format, country_prefix, country_code, country_name, location, carrier, line_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (valid, number, local_format, international_format, country_prefix, country_code, country_name, location, carrier, line_type))

    # Commit the transaction and close the connection
    connection.commit()
    connection.close()

    # Render a confirmation page or redirect to another page
    return render_template("recorded.html", number=number)


@app.route("/phonebook")
@login_required
def phonebook():

    # Connect to SQLite database
    connection = sqlite3.connect('project.db')
    cursor = connection.cursor()

    # Execute a query to retrieve all rows from the numbers table
    cursor.execute('SELECT * FROM numbers')
    rows = cursor.fetchall()

    # Get column names from the cursor description
    column_names = [description[0] for description in cursor.description]

    # Close the connection
    connection.close()

    return render_template("phonebook.html", rows=rows, column_names=column_names)


def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

@app.route("/delete_record", methods=["POST"])
@login_required
def delete_record():
    # Get the record_id from the form data
    record_id = request.form.get("record_id")

    if record_id:
        try:
            # Establish a database connection
            conn = sqlite3.connect('project.db')
            cursor = conn.cursor()

            # Execute the DELETE statement
            cursor.execute("DELETE FROM numbers WHERE id = ?", (record_id,))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Flash a success message
            flash("Record deleted successfully!", "success")
        except Exception as e:
            # Flash an error message if something goes wrong
            flash(f"An error occurred: {e}", "danger")
            conn.close()
    else:
        flash("No record ID provided!", "warning")

    # Redirect back to the phonebook page
    return render_template ("phonebook.html")
