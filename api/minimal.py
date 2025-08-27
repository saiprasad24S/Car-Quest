from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Car Quest!",
        "status": "working",
        "deployment": "vercel"
    })

@app.route('/test')
def test():
    return jsonify({"test": "success", "app": "Car Quest"})

# Vercel expects this
app = app
