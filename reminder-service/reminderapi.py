"""Code for a flask API to Create, Read reminders"""
import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL
import json
import datetime

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USERNAME")
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("DB_PASSWORD")
app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT"))
mysql.init_app(app)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"


@app.route("/api/reminders", methods=["POST"])
def add_reminder():
    """Function to create a reminder to the MySQL database"""
    json = request.json
    reminder_message = json["message"]
    reminder_time = json["time"]
    if reminder_message and reminder_time  and request.method == "POST":
        sql = "INSERT INTO reminders(reminder_message, reminder_time) " \
              "VALUES(%s, %s)"
        data = (reminder_message, reminder_time)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("reminder created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide time and message")

@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    """Function to retrieve all reminders from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT reminder_message, TIME_FORMAT(reminder_time, '%h:%i %p') reminder_time FROM reminders")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
