from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)


## DB Functions
def connect_db():
    conn = sqlite3.connect("./db/RattlersUnite.db")
    conn.row_factory = sqlite3.Row
    return conn

# This function fets all events from A-Z that are after the current time.
def fetch_events():
    conn = connect_db()
    # Grabs current date
    current_date = datetime.now().isoformat()
    events = conn.execute(
        f"SELECT Events.Name, Organizations.Name AS Organization, Date FROM Events JOIN Organizations ON Organizations.ID = Events.Organization ORDER BY Date"
    )
    # Store event data in temp
    temp = events.fetchall()
    # For now loop and remove events that are before the date
    # TODO: Maybe remove dates from SQL DB too.
    for e in temp:
        print(e.keys())
        if e["Date"] < current_date:
            temp.remove(e)
    return temp


def fetch_organizations():
    conn = connect_db()
    orgs = conn.execute("SELECT Name FROM Organizations")
    return orgs.fetchall()


def fetch_leaderboards():
    conn = connect_db()
    board = conn.execute("SELECT Name, Points FROM Students")
    return board.fetchall()

def insert_student_data(student_id, password):
    conn = connect_db()
    conn.execute("INSERT INTO Students (StudentID, Name) VALUES (?, ?)", (student_id, password))
    conn.commit()
    conn.close()


## Filter Functions
@app.template_filter()
def format_datetime(iso):
    dt = datetime.fromisoformat(iso)
    return datetime.strftime(dt, "%B %d, %Y | %I:%M%p CT")


## Site Functions
@app.route("/")
def main():
    events = fetch_events()
    orgs = fetch_organizations()
    return render_template("home.html", events=events, organizations=orgs)


@app.route("/events")
def events():
    events = fetch_events()
    return render_template("events.html", events=events, categories=None)


@app.route("/organizations")
def organizations():
    orgs = fetch_organizations()
    return render_template("organizations.html", organizations=orgs)


@app.route("/leaderboards")
def leaderboards():
    board = fetch_leaderboards()
    return render_template("leaderboards.html", board=board)


@app.route("/login")
def login():
    return render_template("LogIn.html")


@app.route("/signup")
def signup():
    return render_template("SignUp.html")


@app.route("/orgLogIn")
def orgLogIn():
    return render_template("orgLogIn.html")

@app.route("/signupMethod", methods=["GET", "POST"])
def signupMethod():
    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        insert_student_data(student_id, name)
        return "Data inserted successfully"
    else:
        return render_template("SignUp.html")



if __name__ == "__main__":
    app.run()
