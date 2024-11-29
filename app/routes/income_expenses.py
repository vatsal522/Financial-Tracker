from flask import Blueprint, request, jsonify
from utils import get_elasticsearch_client
from datetime import datetime

income_expenses_bp = Blueprint("income_expenses", __name__)
es = get_elasticsearch_client()

# Add Income
@income_expenses_bp.route("/income", methods=["POST"])
def add_income():
    try:
        data = request.json

        # Validate required fields
        if not all(key in data for key in ["amount", "category"]):
            return jsonify({"error": "Missing required fields: amount, category"}), 400

        # Prepare the income document
        income_document = {
            "type": "income",
            "amount": data["amount"],
            "category": data["category"],
            "date": datetime.now().isoformat()
        }

        # Index the income document into Elasticsearch
        es.index(index="income_expenses", document=income_document)

        # Update the total balance in Elasticsearch
        response = es.update(index="bank_accounts", id="total_balance", body={
            "script": {
                "source": """
                    ctx._source.balance += params.amount;
                    ctx._source.last_updated = params.last_updated;
                """,
                "params": {
                    "amount": data["amount"],
                    "last_updated": datetime.now().isoformat()
                }
            },
            "upsert": {
                "balance": data["amount"],
                "last_updated": datetime.now().isoformat()
            }
        })

        # Log the balance update response
        print("Balance update response:", response)

        # Return success response
        return jsonify({
            "message": "Income added successfully and balance updated.",
            "balance_id": response["_id"]
        }), 201

    except Exception as e:
        # Log and return the error
        print(f"Error in Add Income API: {e}")
        return jsonify({"error": str(e)}), 500

# Add Expense
@income_expenses_bp.route("/expense", methods=["POST"])
def add_expense():
    data = request.json
    data["type"] = "expense"  # Force type to "expense"
    data["date"] = datetime.now()  # Automatically add timestamp if missing
    response = es.index(index="income_expenses", document=data)
    
    # Return only relevant parts of the response
    return jsonify({
        "message": "Expense added successfully.",
        "id": response["_id"],
        "index": response["_index"],
        "result": response["result"]
    }), 201