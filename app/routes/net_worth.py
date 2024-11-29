from flask import Blueprint, request, jsonify
from utils import get_elasticsearch_client
from datetime import datetime

net_worth_bp = Blueprint("net_worth", __name__)
es = get_elasticsearch_client()

@net_worth_bp.route("/add_balance", methods=["POST"])
def add_balance():
    try:
        data = request.json

        # Log the incoming data
        print("Add Balance API received data:", data)

        # Validate required fields
        if not all(key in data for key in ["bank_name", "account_no", "balance"]):
            return jsonify({"error": "Missing required fields: bank_name, account_no, or balance"}), 400

        # Construct the unique document ID
        doc_id = f"{data['bank_name']}_{data['account_no']}"

        # Prepare the document with last_updated field
        document = {
            "bank_name": data["bank_name"],
            "account_no": data["account_no"],
            "balance": data["balance"],
            "last_updated": datetime.now().isoformat()  # Automatically set last_updated
        }

        # Index into Elasticsearch
        response = es.index(index="bank_accounts", id=doc_id, document=document)

        # Log the Elasticsearch response
        print("Elasticsearch response:", response)

        # Return success response
        return jsonify({
            "message": "Balance added successfully.",
            "id": response["_id"],
            "index": response["_index"],
            "result": response["result"]
        }), 201

    except Exception as e:
        # Log and return the error
        print("Error in Add Balance API:", str(e))
        return jsonify({"error": str(e)}), 500



@net_worth_bp.route("/get_total_networth", methods=["GET"])
def get_total_networth():
    try:
        # Get total balance from all bank accounts
        balance_response = es.search(index="bank_accounts", body={
            "aggs": {"total_balance": {"sum": {"field": "balance"}}},
            "size": 0
        })
        total_balance = balance_response["aggregations"]["total_balance"]["value"]

        # Get total expenses
        expenses_response = es.search(index="income_expenses", body={
            "query": {"match": {"type": "expense"}},
            "aggs": {"total_expenses": {"sum": {"field": "amount"}}},
            "size": 0
        })
        total_expenses = expenses_response["aggregations"]["total_expenses"]["value"]

        # Calculate net worth
        total_networth = total_balance - total_expenses

        # Return results
        return jsonify({
            "total_balance": total_balance,
            "total_expenses": total_expenses,
            "networth": total_networth
        }), 200

    except Exception as e:
        # Log and return error
        return jsonify({"error": str(e)}), 500
    
    
@net_worth_bp.route("/get_all_balances", methods=["GET"])
def get_all_balances():
    try:
        # Elasticsearch query to fetch all documents
        response = es.search(index="bank_accounts", body={
            "query": {
                "match_all": {}
            },
            "size": 1000  # Fetch up to 1000 records
        })

        # Extract the source data
        records = [hit["_source"] for hit in response["hits"]["hits"]]

        return jsonify({
            "message": "Successfully fetched all balances.",
            "records": records
        }), 200

    except Exception as e:
        print("Error fetching balances:", str(e))
        return jsonify({"error": str(e)}), 500