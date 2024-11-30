# Financial Tracker Dashboard

This project is a Financial Tracker Dashboard that helps users manage their finances by tracking income, expenses, and net worth. The dashboard is built using Streamlit for the frontend and Flask for the backend, with Elasticsearch as the data store.

In the US, many individuals have multiple bank accounts and there is no single place to collate all that information. This dashboard provides that feature, allowing users to aggregate and manage all their financial data in one place. All the data is securely stored in your Docker container, ensuring easy access and management.

### Why Store Financial Data Locally?

Storing financial data locally in your Dockerized Elasticsearch container ensures maximum privacy, security, and control over your sensitive information. Here’s why this approach is better:

#### Key Benefits

	•	Privacy: Your data stays with you, avoiding third-party cloud providers.
	•	Security: Minimized risk of breaches as data isn’t transmitted externally.
	•	Cost-Effective: No recurring subscription fees—utilizes your existing hardware.
	•	Customizable: Fully adaptable to your needs without reliance on provider restrictions.
	•	Offline Access: Access your financial data anytime without requiring an internet connection.

#### How Your Data is Stored

	•	Elasticsearch: Data is stored locally in a Dockerized Elasticsearch container.
	•	Persistent Storage: Docker volumes ensure data is retained even after container restarts.
	•	Secure Setup: Basic authentication and HTTPS protect your information.

## Features

- **Add Income and Expenses**: Users can add their income and expenses through the dashboard.
- **View Income and Expenses by Category**: Visualize income and expenses categorized for better insights.
- **Net Worth Overview**: Get a summary of total balance, total expenses, and net worth.
- **AI Recommendations**: Generate financial recommendations using AI based on the user's financial data.
- **API Endpoints**: Provides RESTful API endpoints for managing financial data.

## Project Structure

```
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── bank_accounts.py
│   │   ├── income_expenses.py
│   │   ├── monthly_budget.py
│   │   └── net_worth.py
├── services/
│   ├── bank_accounts.py
│   ├── income_expenses.py
│   ├── monthly_budget.py
│   └── net_worth.py
├── app/
│   ├── streamlit_dashboard.py
│   └── utils.py
├── debugging/
├── docker-compose.yml
├── elasticsearch_indices.json
├── myenv/
│   ├── .gitignore
│   ├── bin/
│   ├── etc/
│   ├── include/
│   ├── lib/
│   └── pyvenv.cfg
├── README.md
└── .env
```



## Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- Node.js (for Streamlit)

### Installation

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up the environment**:
    ```sh
    python -m venv myenv
    source myenv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure environment variables**:
    Create a `.env` file in the root directory with the following content:
    ```env
    ELASTIC_PASSWORD=<>
    KIBANA_PASSWORD=<>
    STACK_VERSION=8.15.3
    CLUSTER_NAME=docker-cluster
    LICENSE=basic
    ES_PORT=9200
    KIBANA_PORT=5601
    MEM_LIMIT=1073741824
    LANGCHAIN_API_KEY=your_langchain_api_key
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_PROJECT=your_project_name
    ```

4. **Start the services**:
    ```sh
    docker compose up
    ```

5. **Run the Flask backend**:
    ```sh
    python app/main.py
    ```

6. **Run the Streamlit dashboard**:
    ```sh
    streamlit run app/streamlit_dashboard.py
    ```

## Usage

- **Access the dashboard**: Open your browser and go to `http://localhost:2000`.
- **API Endpoints**:
  - `POST /income_expenses/income`: Add income
  - `POST /income_expenses/expense`: Add expense
  - `POST /net_worth/add_balance`: Add bank account balance 
  - `GET /income_expenses/current_month_income`: Get current month's income
  - `GET /income_expenses/current_month_expenses`: Get current month's expenses
  - `GET /net_worth/get_total_networth`: Get total net worth
  - `GET /net_worth/get_all_balances`: Get all bank account balances

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

