from flask import Flask, request, Response, jsonify, render_template, redirect, url_for, make_response
import json
import jwt
import datetime
from functools import wraps
import helper

app = Flask(__name__)
secret_key = "not_so_secret_cuz_this_is_just_a_poc"

### JWT helpers ###
def generate_token(data):
    payload = {
        "data": data,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return redirect(url_for("auth"))

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = data['data']['userid']
        except jwt.ExpiredSignatureError:
            return redirect(url_for("auth"))
        except jwt.InvalidTokenError:
            return redirect(url_for("auth"))

        return f(user_id, *args, **kwargs)
    return decorated

### Authentication ###
@app.route("/")
@token_required
def index(user_id):
    return render_template("common.html")

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")
    elif request.method == "POST":
        req_data = request.get_json() or request.form
        username = req_data.get("username")
        password = req_data.get("password")
        credentials_data = helper.check_login(username, password)

        if credentials_data is not None:
            token = generate_token({"userid": credentials_data, "username": username})
            response = make_response(jsonify({"success": True}), 200)
            response.set_cookie("token", token)
            return response
        else:
            return jsonify({"error": "Invalid credentials"}), 401

@app.route("/register", methods=["POST"])
def register():
    req_data = request.get_json()
    username = req_data.get("username")
    password = req_data.get("password")

    if helper.register_user(username, password):
        return jsonify({"success": True}), 201
    else:
        return jsonify({"error": "Username already exists or registration failed"}), 409

@app.route("/logout")
def logout():
    response = redirect(url_for("auth"))
    response.set_cookie("token", "", expires=0)
    return response

### app main entry point ###
@app.route("/new", methods=["POST"])
@token_required
def add_item(user_id):
    req_data = request.get_json()
    item = req_data["item"]
    res_data = helper.add_to_item(item, user_id)
    if res_data is None:
        return jsonify({"error": f"Item not added - {item}"}), 400
    return jsonify(res_data), 200

@app.route("/items/all")
@token_required
def get_all_items(user_id):
    res_data = helper.get_all_items(user_id)
    return jsonify(res_data), 200

@app.route("/item/update", methods=["PUT"])
@token_required
def update_status(user_id):
    req_data = request.get_json()
    item = req_data["item"]
    status = req_data["status"]
    res_data = helper.update_status(item, status)
    if res_data is None:
        return jsonify({"error": f"Error updating item - {item}, {status}"}), 400
    return jsonify(res_data), 200

@app.route("/item/remove", methods=["DELETE"])
@token_required
def delete_item(user_id):
    req_data = request.get_json()
    item = req_data["item"]
    res_data = helper.delete_item(item)
    if res_data is None:
        return jsonify({"error": f"Error deleting item - {item}"}), 400
    return jsonify(res_data), 200
