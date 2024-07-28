from flask import Flask, request, jsonify, abort, session
from flask.logging import create_logger
import os
import database, client_handling
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
log = create_logger(app)

# Define a valid token (in a real application, store this securely)
VALID_TOKEN = os.getenv('VALID_TOKEN')  # Needs to be set in the environment

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != VALID_TOKEN:
            abort(401)  # Unauthorized
        return f(*args, **kwargs)
    return decorator

@app.route('/register', methods=['POST'])
@token_required
def register():
    data = request.json
    if database.add_client(data):
        return jsonify({'status': 'success', 'message': 'Registered'})
    return jsonify({'status': 'error', 'message': 'Registration failed'})

@app.route('/fetch_company_data', methods=['POST'])
@token_required
def fetch_company_data():
    data = request.json
    companies = database.get_compenies()
    return jsonify({'status': 'success', 'data': companies})

@app.route('/buy', methods=['POST'])
@token_required
def buy():
    data = request.json
    ans = client_handling.buy(data['symbol'], data['amount'])
    if ans != 'not sefichant cash in account!':
        return jsonify({'status': 'success', 'message': ans})
    return jsonify({'status': 'error', 'message': ans})

@app.route('/sell', methods=['POST'])
@token_required
def sell():
    data = request.json
    ans = client_handling.sell(data['symbol'], data['amount'])
    if ans != 'not sefichant cash in account!':
        return jsonify({'status': 'success', 'message': ans})
    return jsonify({'status': 'error', 'message': ans})

@app.route('/deposit', methods=['POST'])
@token_required
def deposit():
    data = request.json
    ans = client_handling.deposit(data['amount'])
    return jsonify({'status': 'success', 'message': ans})

@app.route('/withdraw', methods=['POST'])
@token_required
def withdraw():
    data = request.json
    ans = client_handling.withdraw(data['amount'])
    if ans != 'not sefichant cash in account!':
        return jsonify({'status': 'success', 'message': ans})
    return jsonify({'status': 'error', 'message': ans})

@app.route('/data', methods=['POST'])
@token_required
def receive_data():
    data = request.json
    log.info(f"Received data: {data}")
    return jsonify({"received": data})

@app.route('/send_data', methods=['GET'])
@token_required
def send_data():
    data_to_send = {"message": "Hello, client!"}
    log.info(f"Sending data: {data_to_send}")
    return jsonify(data_to_send)

@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    username = credentials.get('username')
    password = credentials.get('password')
    res = database.login(username, password)
    if res is not None:
        compenies = database.get_compenies()
        session['logged_in'] = True
        log.info(f"User {username} logged in")
        return jsonify({"status": "success", "message": "Logged in", "user": res, "compenies": compenies})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    log.info("User logged out")
    return jsonify({"message": "Logged out"})

if __name__ == "__main__":
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), ssl_context=('certs/server.crt.pem', 'certs/server.key.pem'))
