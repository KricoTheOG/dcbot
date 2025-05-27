from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data['payment_status'] == 'finished':
        order_id = data['order_id']
        user_id, item_id = order_id.split("_")
        with open("users.json") as f:
            users = json.load(f)
        user = users.get(user_id, {"inventory": []})
        user["inventory"].append(item_id)
        users[user_id] = user
        with open("users.json", "w") as f:
            json.dump(users, f, indent=2)
        print(f"{user_id} bought {item_id}")
    return '', 200

if __name__ == "__main__":
    app.run(port=5000)