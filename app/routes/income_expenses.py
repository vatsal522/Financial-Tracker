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
    
    
    
    
@income_expenses_bp.route("/current_month_income", methods=["GET"])
def get_current_month_income():
    try:
        # Get the first and last days of the current month
        now = datetime.now()
        first_day = now.replace(day=1).isoformat()
        last_day = now.isoformat()

        # Elasticsearch query to sum income for the current month
        response = es.search(index="income_expenses", body={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"type": "income"}},
                        {"range": {"date": {"gte": first_day, "lte": last_day}}}
                    ]
                }
            },
            "aggs": {
                "total_income": {"sum": {"field": "amount"}}
            },
            "size": 0
        })

        # Extract the total income
        total_income = response["aggregations"]["total_income"]["value"]

        # Return the total income for the current month
        return jsonify({
            "message": "Successfully fetched current month's total income.",
            "current_month_income": total_income
        }), 200

    except Exception as e:
        # Log and return the error
        print(f"Error fetching current month's total income: {e}")
        return jsonify({"error": str(e)}), 500
    
    
@income_expenses_bp.route("/current_month_expenses", methods=["GET"])
def get_current_month_expenses():
    try:
        # Get the first and last days of the current month
        now = datetime.now()
        first_day = now.replace(day=1).isoformat()
        last_day = now.isoformat()

        # Elasticsearch query to sum expenses for the current month
        response = es.search(index="income_expenses", body={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"type": "expense"}},
                        {"range": {"date": {"gte": first_day, "lte": last_day}}}
                    ]
                }
            },
            "aggs": {
                "total_expenses": {"sum": {"field": "amount"}}
            },
            "size": 0
        })

        # Extract the total expenses
        total_expenses = response["aggregations"]["total_expenses"]["value"]

        # Return the total expenses for the current month
        return jsonify({
            "message": "Successfully fetched current month's total expenses.",
            "current_month_expenses": total_expenses
        }), 200

    except Exception as e:
        # Log and return the error
        print(f"Error fetching current month's total expenses: {e}")
        return jsonify({"error": str(e)}), 500
