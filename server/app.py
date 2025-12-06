import html
import logging

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

from utils.model_utils import classify_all

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route("/")
def serve_index():
    return send_from_directory("../client", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("../client", filename)


@app.route("/load_model", methods=["GET"])
@cross_origin()
def load_model_route():
    try:
        logger.info("Models are already loaded on import.")
        return jsonify({"status": "Models are ready"}), 200
    except Exception as e:
        logger.error(f"Error in /load_model: {e}")
        return jsonify({"error": "Error while loading models."}), 500


@app.route("/select_model", methods=["POST"])
@cross_origin()
def select_model():
    try:
        return jsonify({"model": "tfidf_combo"}), 200
    except Exception as e:
        logger.error(f"Error in /select_model: {e}")
        return jsonify({"error": "Error while selecting model."}), 500


@app.route("/labels", methods=["GET"])
@cross_origin()
@cache.cached(timeout=3600)
def get_labels():
    """
    Returns available routing labels for frontend display.
    """
    try:
        from utils.model_utils import routing_labels
        return jsonify({"routing_labels": routing_labels}), 200
    except Exception as e:
        logger.error(f"Error in /labels: {e}")
        return jsonify({"error": "Error while fetching labels."}), 500


@app.route("/classify", methods=["POST"])
@cross_origin()
def classify():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Empty text"}), 400

        logger.info(f"Classifying text: {text}")

        sanitized_text = html.escape(text)

        result = classify_all(sanitized_text)

        logger.info(
            f"Classification result: "
            f"topic={result['topic']} "
            f"priority={result['priority']} "
            f"routing={result['routing']}"
        )

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in /classify: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while classifying the text."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
