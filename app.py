import os
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Secrets from .env / Render environment
app.secret_key = os.getenv("SECRET_KEY")
KITCHEN_PASSWORD = os.getenv("KITCHEN_PASSWORD")

# Enable CORS (for WordPress frontend)
CORS(app)

# In-memory orders list
orders = []


# -------------------------
# Pages
# -------------------------

@app.route("/")
def home():
    return render_template("order.html")


def check_auth(username, password):
    return username == "kitchen" and password == KITCHEN_PASSWORD


def authenticate():
    return Response(
        "Authentication required",
        401,
        {"WWW-Authenticate": 'Basic realm="Kitchen"'}
    )


@app.route("/kitchen")
def kitchen():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return render_template("kitchen.html")


# -------------------------
# API
# -------------------------

@app.route("/order", methods=["POST"])
def order():
    data = request.json

    new_order = {
        "table": data.get("table"),
        "items": data.get("items", []),
        "comment": data.get("comment", "")
    }

    orders.append(new_order)
    print("New order:", new_order)

    return jsonify({"status": "ok"})


@app.route("/orders")
def get_orders():
    return jsonify(orders)


@app.route("/complete/<int:index>", methods=["POST"])
def complete(index):
    if 0 <= index < len(orders):
        orders.pop(index)
        return jsonify({"status": "removed"})
    return jsonify({"error": "invalid index"}), 400


# -------------------------
# Local dev only
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


