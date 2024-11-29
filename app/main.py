from flask import Flask
from routes.bank_accounts import bank_accounts_bp
from routes.income_expenses import income_expenses_bp
from routes.monthly_budget import monthly_budget_bp
from routes.net_worth import net_worth_bp
from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "mynameisvatsal"), verify_certs=False)

# Initialize Flask application
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(bank_accounts_bp, url_prefix="/bank_accounts")
app.register_blueprint(income_expenses_bp, url_prefix="/income_expenses")
app.register_blueprint(monthly_budget_bp, url_prefix="/monthly_budget")
app.register_blueprint(net_worth_bp, url_prefix="/net_worth")


# Root Route for Testing
@app.route("/")
def index():
    return {"message": "Welcome to the Financial Tracker API"}, 200


from datetime import datetime

def ensure_indices():
    try:
        print("Ensuring Elasticsearch indices are created...")

        # Check and create the 'bank_accounts' index if missing
        if not es.indices.exists(index="bank_accounts"):
            es.indices.create(index="bank_accounts", body={
                "mappings": {
                    "properties": {
                        "balance": {"type": "double"},
                        "last_updated": {"type": "date"},
                        "bank_name": {"type": "text"},
                        "account_no": {"type": "text"}
                    }
                }
            })
            print("************************************************************************************************")
            print("Created 'bank_accounts' index.")
            print("************************************************************************************************")
        else:
            print("************************************************************************************************")
            print("Index 'bank_accounts' already exists.")
            print("************************************************************************************************")

        # Ensure the total_balance document exists
        try:
            es.get(index="bank_accounts", id="total_balance")
            print("************************************************************************************************")
            print("'total_balance' document already exists.")
            print("************************************************************************************************")
        except Exception:
            print("************************************************************************************************")
            print("Creating 'total_balance' document...")
            print("************************************************************************************************")
            es.index(index="bank_accounts", id="total_balance", document={
                "balance": 0.0,
                "last_updated": datetime.now().isoformat()
            })
            print("************************************************************************************************")
            print("'total_balance' document created.")
            print("************************************************************************************************")

        # Check and create the 'income_expenses' index if missing
        if not es.indices.exists(index="income_expenses"):
            print("************************************************************************************************")
            print("Index 'income_expenses' does not exist. Creating with correct mapping...")
            print("************************************************************************************************")
            es.indices.create(index="income_expenses", body={
                "mappings": {
                    "properties": {
                        "type": {"type": "keyword"},
                        "amount": {"type": "double"},
                        "category": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword"}
                            }
                        },
                        "date": {"type": "date"}
                    }
                }
            })
            print("************************************************************************************************")
            print("Created 'income_expenses' index with correct mapping.")
            print("************************************************************************************************")
        else:
            print("************************************************************************************************")
            print("Index 'income_expenses' already exists.")
            print("************************************************************************************************")

        # Check if 'category.keyword' exists
        mapping = es.indices.get_mapping(index="income_expenses")
        if "keyword" not in mapping["income_expenses"]["mappings"]["properties"]["category"].get("fields", {}):
            print("************************************************************************************************")
            print("Updating 'income_expenses' index to include 'category.keyword'...")
            print("************************************************************************************************")
            es.indices.put_mapping(index="income_expenses", body={
                "properties": {
                    "category": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    }
                }
            })
            print("************************************************************************************************")
            print("Updated 'income_expenses' index mapping to include 'category.keyword'.")
            print("************************************************************************************************")

    except Exception as e:
        print("************************************************************************************************")
        print(f"Error ensuring indices: {e}")
        print("************************************************************************************************")   
        
if __name__ == "__main__":
    ensure_indices()
    app.run(debug=True, host="0.0.0.0", port=5000)