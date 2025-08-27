from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Car Quest API is working!", "status": "success"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "Car Quest"})

if __name__ == '__main__':
    app.run(debug=True)
