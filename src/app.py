from flask import Flask, request, jsonify
from data_loader import HSNDataLoader
from validator import HSNValidator
from responses import format_success_response, format_error_response
import os

app = Flask(__name__)

# Optional debug mode
DEBUG_MODE = False

# Absolute path to the Excel data file
DATA_PATH = os.path.abspath(r'C:\Applications\HSN Code Validation Agent\data\HSN_Master_Data.xlsx')

if DEBUG_MODE:
    print("\n=== DEBUG INFORMATION ===")
    print("Current working directory:", os.getcwd())
    print("Attempting to load from:", DATA_PATH)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Excel file not found at: {DATA_PATH}\n"
        f"Make sure the file exists or update DATA_PATH."
    )

# Load and validate data
data_loader = HSNDataLoader(DATA_PATH, verbose=DEBUG_MODE)
if not data_loader.load_data():
    raise RuntimeError("Failed to load HSN data")
validator = HSNValidator(data_loader)

# ✅ Home route to confirm server is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "✅ HSN Code Validation API is running.",
        "endpoints": {
            "/validate": "POST - Validate a single HSN code",
            "/validate_batch": "POST - Validate multiple HSN codes"
        },
        "status": "OK"
    })

# Endpoint for single HSN code validation
@app.route('/validate', methods=['POST'])
def validate_hsn():
    data = request.get_json()
    hsn_code = data.get('hsn_code')

    if not hsn_code:
        return jsonify({"error": "hsn_code parameter is required"}), 400

    result = validator.full_validation(hsn_code)

    if result['status'] == 'valid':
        return jsonify(format_success_response(
            hsn_code,
            result['description'],
            result['validation_details']
        ))
    else:
        return jsonify(format_error_response(
            hsn_code,
            result['error'],
            result['validation_stage']
        )), 400

# Endpoint for batch HSN code validation
@app.route('/validate_batch', methods=['POST'])
def validate_batch():
    data = request.get_json()
    hsn_codes = data.get('hsn_codes', [])

    if not isinstance(hsn_codes, list):
        return jsonify({"error": "hsn_codes must be an array"}), 400

    results = validator.validate_multiple(hsn_codes)
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000))) 
