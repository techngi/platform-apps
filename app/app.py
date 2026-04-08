from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

@app.get("/health")
def health():
    return jsonify(app="DevOps-app", status="ok", version=os.getenv("APP_VERSION", "dev"))

@app.get("/")
def root():
    REQUESTS.inc()
    return "Welcome to the world of DevOps - Stage2:)\n"

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
