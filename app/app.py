from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

@app.route("/health")
def health():
    return jsonify(
        app="DevOps-app",
        status="ok",
        version=os.getenv("APP_VERSION", "dev"),
        environment=os.getenv("APP_ENV", "dev"),
        log_level=os.getenv("LOG_LEVEL", "info")
    )
@app.get("/")
def root():
    REQUESTS.inc()
    return "Welcome to the world of DevOps - StageFull:)\n"

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
