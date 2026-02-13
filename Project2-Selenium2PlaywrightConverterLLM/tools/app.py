from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.converter import convert_selenium_to_playwright_stream

app = Flask(__name__, static_folder="../static", static_url_path="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("../static", "index.html")

@app.route("/api/convert", methods=["POST"])
def convert():
    data = request.json
    source_code = data.get("source_code", "")
    
    if not source_code:
        return jsonify({"status": "error", "message": "No source code provided"}), 400
        
    def generate():
        try:
            for chunk in convert_selenium_to_playwright_stream(source_code):
                yield chunk
        except Exception as e:
            yield f"// Error during streaming: {str(e)}"

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == "__main__":
    # Create static dir if not exists
    os.makedirs("../static", exist_ok=True)
    print("ðŸš€ Server starting at http://localhost:5000")
    app.run(port=5000, debug=True)
