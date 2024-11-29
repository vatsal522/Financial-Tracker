from flask import Blueprint, request, jsonify
from utils import get_elasticsearch_client
from datetime import datetime

bank_accounts_bp = Blueprint("bank_accounts", __name__)
es = get_elasticsearch_client()

@bank_accounts_bp.route("/", methods=["POST"])
def add_bank_account():
    data = request.json
    data["last_updated"] = datetime.now()
    response = es.index(index="bank_accounts", document=data)
    
    # Return only relevant parts of the response
    return jsonify({
        "message": "Bank account added successfully.",
        "id": response["_id"],
        "index": response["_index"],
        "result": response["result"]
    }), 201