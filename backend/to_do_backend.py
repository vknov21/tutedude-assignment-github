from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, redirect
from urllib.parse import urlencode

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
app = Flask(__name__, template_folder=template_dir)


class MongoDBConn():
    def __init__(self, db_name):
        load_dotenv()
        # Create a new client and connect to the server
        client = MongoClient(os.getenv('MONGODB_URL'))
        self.db = client.__getattr__(db_name)

    def get_table(self, table_name):
        self.table = self.db[table_name]
        return self.table

    def get_all(self):
        cursor = self.table.find()
        return cursor


def create_conn(db_name, table_name):
    db_conn = MongoDBConn(db_name)
    table = db_conn.get_table(table_name)
    return db_conn, table


db_conn, table = create_conn("todo_db", "todo_list")


@app.route('/')
def home():
    return redirect("/todo_list")


@app.route('/submittodoitem', methods=["GET"])
def form_req():
    error = request.args.get("error", "")
    return render_template("form.html", error=error)


@app.route("/success")
def success():
    return "Data submitted successfully!"


@app.route("/submittodoitem", methods=["POST"])
def submit():
    try:
        user_input = dict(request.form)
        if any(val=="" for val in user_input.values()):
            raise Exception("The values cannot be empty")
        table.insert_one(user_input)
        return redirect("/success")
    except Exception as e:
        query_string = urlencode({"error": str(e)})
        return redirect(f"/submittodoitem?{query_string}")


@app.route("/todo_list", methods=["GET"])
def todo_list():
    data = db_conn.get_all()
    return render_template("index.html", items=data)


if __name__ == "__main__":
    app.run(debug=True)
