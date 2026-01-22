from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

orders = []


@app.route("/")
def home():
    return render_template("order.html")


@app.route("/kitchen")
def kitchen():
    return render_template("kitchen.html")


@app.route("/order", methods=["POST"])
def order():
    data = request.json
    orders.append(
        {
            "table": data["table"],
            "items": data["items"],
            "comment": data.get("comment", ""),
        }
    )
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
