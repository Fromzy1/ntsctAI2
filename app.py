#
# 2024-Nov-21
#
# Go to folder and launch
# uvicorn app:app --reload
#

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import json
from pprint import pprint
import OpenAIClient
import ElasticTools
import chart_util

load_dotenv()

app = FastAPI()

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Instantiate OpenAI and ElasticTools
LLM = OpenAIClient.Client()
et = ElasticTools.Tools()
index_dict = et.get_indices_dict()
myIndex = "kafka-application"
schema_fields = et.load_es_index_fields(index_dict[myIndex])
schema = et.get_index_schema(index_dict[myIndex])

# Read prompt template
with open('prompt_1.txt', 'r') as file:
    content = file.read()
prompt = content.format(schema=schema)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Render the homepage with the index dropdown"""
    index_list = [{"key": key, "value": value} for key, value in index_dict.items()]
    return templates.TemplateResponse("index.html", {"request": {}, "index_list": index_list})

@app.post("/get-index-fields/")
async def get_index_fields(selected_index: str = Form(...)):
    """Fetch and return the fields of the selected index."""
    try:
        fields = et.load_es_index_fields(selected_index)
        return {"fields": fields}
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate-query/")
async def generate_query(user_query: str = Form(...)):
    """Generate Elasticsearch query from user input."""
    response = LLM.generate_non_streaming_response(user_query, system_prompt=prompt)
    es_query = json.loads(response)
    return {
        "elasticsearch_query": response,
        "es_query": es_query,
    }


@app.post("/generate-graph/")
async def generate_graph(es_query: str = Form(...), user_query: str = Form(...)):
    """Generate graph based on Elasticsearch query."""
    es_query = json.loads(es_query)
    # Fetch results from Elasticsearch
    search_results = et.search_results(index_dict[myIndex], es_query=es_query)
    total_hits = search_results['hits']['total']['value']

    # Check for data and generate chart
    chart_path = None
    content_description = None
    if total_hits > 0:
        data = (
            search_results['aggregations']
            if "aggs" in es_query
            else search_results['hits']['hits']
        )
        finalChart = chart_util.ChartUtil(user_query)
        chart_path, content_description = finalChart.generate_chart(data)

    return {
        "chart_path": "/static/chart.png" if chart_path else None,
        "content_description": content_description,
        "total_hits": total_hits,
    }