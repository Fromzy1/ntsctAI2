# ntsctAI2

**Secure AI-powered Elasticsearch Query Generator and Visualization Tool**

This project uses OpenAI's language model to convert natural language questions into Elasticsearch queries, runs them on a specified index, and visualizes the results with charts.

## 🧠 Overview

The goal of this application is to:
- Leverage a system prompt containing the index schema to guide query generation.
- Allow flexible natural language querying over Elasticsearch data.
- Automatically visualize the results based on aggregation or document data.

## 📂 Project Structure

ntsctAI2/
│
├── ntsctAI.py              # Main script: handles query, ES interaction, and visualization
├── prompt_1.txt            # System prompt template with placeholder for schema
├── .env                    # Environment variables (e.g., OpenAI API key)
├── OpenAIClient.py         # Wrapper for OpenAI API calls
├── ElasticTools.py         # Helper functions for Elasticsearch queries and index inspection
├── chart_util.py           # Utilities for chart generation based on ES results

## ⚙️ Requirements

- Python 3.8+
- Access to:
  - OpenAI API (via `.env`)
  - Elasticsearch instance with your data
- Required Python packages:
  - `openai`
  - `python-dotenv`
  - `elasticsearch`
  - `matplotlib` or `plotly` (depending on what your chart utility uses)

## 🔧 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/ntsctAI2.git
   cd ntsctAI2

	2.	Create .env file

OPENAI_ASSISTANT_ID="your_openai_assistant_id"
ELASTICSEARCH_URL=https://elastic-server:9200
ELASTICSEARCH_USERNAME=your_username
ELASTICSEARCH_PASSWORD=your_elastic_password
ELASTICSEARCH_CA_CERT=/path/to/http_ca.crt

	3.	Install dependencies

pip install -r requirements.txt


	4.	Edit the system prompt
Customize prompt_1.txt if needed to tune how the LLM interprets the schema and the query.

🚀 Usage

Run the script:

python ntsctAI.py

You’ll be prompted to confirm before launching the query. The output includes:
	•	The generated Elasticsearch query
	•	Matching results
	•	A chart visualization (if applicable)

📌 Example Queries

You can try replacing the query line in ntsctAI.py with examples like:

query="What are the top 6 servers that are consuming biggest bandwidth"
query="What are the different applications served by IP 13.13.0.0"

🛡️ Security Notes
	•	Do not commit your .env file with sensitive credentials.
	•	Ensure your Elasticsearch instance is secured and access-controlled.

📈 Output
	•	If the query contains "aggs": the results are aggregated and visualized.
	•	Otherwise: raw hit data is shown.

📞 Contact

Maintainer: Fromzy
