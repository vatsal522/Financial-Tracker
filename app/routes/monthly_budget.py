from flask import Blueprint, request, jsonify
from utils import get_elasticsearch_client

monthly_budget_bp = Blueprint("monthly_budget", __name__)
es = get_elasticsearch_client()

# Add or Update Monthly Budget
@monthly_budget_bp.route("/", methods=["POST"])
def add_update_monthly_budget():
    data = request.json
    response = es.index(index="monthly_budget", document=data)
    
    # Return only relevant parts of the response
    return jsonify({
        "message": "Monthly budget added/updated successfully.",
        "id": response["_id"],
        "index": response["_index"],
        "result": response["result"]
    }), 201

# Get Monthly Budget
@monthly_budget_bp.route("/<month>", methods=["GET"])
def get_monthly_budget(month):
    response = es.search(index="monthly_budget", body={
        "query": {"match": {"month": month}}
    })
    budgets = [hit["_source"] for hit in response["hits"]["hits"]]
    return jsonify(budgets), 200