from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(app="week3-app", status="ok", version=os.getenv("APP_VERSION", "dev"))

@app.get("/")
def root():
    return "week3-app is running\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
