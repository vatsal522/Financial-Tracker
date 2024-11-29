from elasticsearch import Elasticsearch

def get_elasticsearch_client():
    """Initialize and return an Elasticsearch client."""
    return Elasticsearch(
        hosts=["https://localhost:9200"],
        basic_auth=("elastic", "mynameisvatsal"),
        verify_certs=False
    )