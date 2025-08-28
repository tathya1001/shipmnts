import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import http.client
import sqlite3
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
# API_KEY = os.getenv("API_KEY", "default_api_key")


# conn = http.client.HTTPSConnection("url")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datastorage.db'
db = SQLAlchemy(app)

# class Data(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     info = db.Column(db.String(200))

    
#     def __repr__(self):
#         return f"<Data id={self.id} info={self.info}>"
def get_db_connection():
    conn = sqlite3.connect('datastorage.db')
    conn.row_factory = sqlite3.Row
    return conn


class DB(db.Model):
    location_code = db.Column(db.String(200), primary_key=True)
    parent = db.Column(db.String(200))
    type_of_storage = db.Column(db.String(200))

    
    # def __repr__(self):
        # return f"<Data id={self.id} info={self.info}>"

with app.app_context():
    db.create_all()


# warehouse = {}

def addData(location_code, parent):
    if parent == None:
        new_data = DB(location_code = location_code, parent = None, type_of_storage = "warehouse")
    else:
        new_data = DB(location_code = location_code, parent = parent, type_of_storage = "storage")
    db.session.add(new_data)
    db.session.commit()
    

@app.route("/api/create_location", methods=["POST"])
def create_location():
    location_code = request.json.get("location_code")
    parent_location_code = request.json.get("parent_location_code")
    addData(location_code, parent_location_code)
    if location_code == None:
        
        return jsonify({"success": False,
                        "message": "Location not created",
                        })
    
    if parent_location_code == None:
        # warehouse[location_code] = {}
        return jsonify({"success": True,
                        "message": "Location created successfully",
                        "data": {
                            "location_code": location_code,
                            "parent_location_code": None,
                            "type": "warehouse"
                        }})
    else:
        return jsonify({"success": True,
                        "message": "Location created successfully",
                        "data": {
                            "location_code": location_code,
                            "parent_location_code": parent_location_code,
                            "type": "storage"
                        }})

# def query_db(query, args=(), one=False):
#     cur = DB.execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv


def fetchChilds(location_code):
    # conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()

    
    childs = DB.query.filter_by(parent=location_code).all()
    # conn = DB()
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM your_table")
    # rows = cursor.fetchall()

    print(type(childs[0]))
    return childs

@app.route("/api/warehouse/tree", methods=["GET"])
def getTree():
    warehouse_code = request.args.get("warehouse_code")
    childs = fetchChilds(warehouse_code)
    tree = []
    
    
    for child in childs:
        tree.append({"location_code": child["location_code"], "type": child["type_of_storage"]})
    
    return jsonify({"location_code": warehouse_code,
                   "type": "warehouse",
                   "childs": tree})
    
    # return jsonify({"location_code": warehouse_code,
    #                "type": "warehouse",
    #                "childs": tree})
    
    
# def addData(info):
#     new_data = Data(info=info)
#     db.session.add(new_data)
#     db.session.commit()
    
# def deleteData(info):
#     data_to_delete = Data.query.filter_by(info=info).first()
#     db.session.delete(data_to_delete)
#     db.session.commit()


# @app.route("/insert", methods=["GET", "POST"])
# def insert():
#     if request.method == "POST":
#         info = request.json.get("info")
#         addData(info)
#         return jsonify({"message": "Data inserted successfully!"})
#     else:
#         all_data = Data.query.all()
#         response = [data.info for data in all_data]
#         return render_template('index.html', response=response)

# @app.route("/delete", methods=["GET", "POST"])
# def delete():
#     if request.method == "POST":
#         info = request.json.get("info")
#         deleteData(info)
#         return jsonify({"message": "Data deleted successfully!"})
#     else:
#         all_data = Data.query.all()
#         response = [data.info for data in all_data]
#         return render_template('index.html', response=response)


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')
    # return jsonify({"message": "Flask Boilerplate is running!"})


@app.route("/public", methods=["GET"])
def public():
    return jsonify({"temp": "abcdefgh"})

#query param
@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("r")
    return jsonify({"query": q})

#url param
@app.route("/user/<username>/<role>", methods=["GET"])
def get_user(username, role):
    return jsonify({"role": role})

# @app.route("/secure-data", methods=["GET"])
# def secure_data():
#     api_key = request.headers.get("x-api-key")
#     if api_key != API_KEY:
#         return jsonify({"error": "Unauthorized"})
#     return jsonify({"data": "super secret"})


@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"data": data})

# @app.route("/protected", methods=["POST"])
# def protected():
#     api_key = request.headers.get("x-api-key")
#     if api_key != API_KEY:
#         return jsonify({"error": "Unauthorized"}), 401
    
#     data = request.get_json()
#     return jsonify({"received": data, "status": "success"})

def func(a,b,c,d):
    return int(a)+int(b)+int(c)+int(d)

@app.route("/user/<a>/<b>/<c>/<d>", methods=["GET"])
def sum(a, b,c,d):
    ans = func(a,b,c,d)
    return jsonify({"sum": ans})

if __name__ == "__main__":
    app.run(host= "0.0.0.0",debug=True, port=5000)
