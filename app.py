import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import http.client
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
# API_KEY = os.getenv("API_KEY", "default_api_key")


# conn = http.client.HTTPSConnection("url")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(200))

    
    def __repr__(self):
        return f"<Data id={self.id} info={self.info}>"

with app.app_context():
    db.create_all()


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
