from flask import Flask, jsonify

# 1. Create the server app
app = Flask(__name__)

# 2. Create a "Route" (a specific job for the waiter)
@app.route('/', methods=['GET'])
def hello():
    # When someone visits this route, return this message
    return jsonify({"message": "Hello! The University API is awake!"})

# 3. Turn the server on
if __name__ == '__main__':
    app.run(debug=True, port=5000)