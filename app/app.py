from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(app="DevOps-app", status="ok", version=os.getenv("APP_VERSION", "dev"))

@app.get("/")
def root():
    return "Welcome to the world of DevOps\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
