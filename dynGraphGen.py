import matplotlib.pyplot as plt
import pandas as pd
import openai
import os
from dotenv import load_dotenv

def process_elasticsearch_data(data, use_llm=False):
    """
    Process Elasticsearch aggregation data and generate a graph.
    :param data: Elasticsearch-style dictionary with buckets.
    """
    # Extract bucket data

    for key in data:
        if isinstance(data[key], dict) and 'buckets' in data[key]:
            buckets = data[key]['buckets']
            break
    df = pd.DataFrame(buckets)
    for col in df.columns:
        if isinstance(df[col].iloc[0], dict) and 'value' in df[col].iloc[0]:
            value_field = col
    if value_field in df.columns and isinstance(df[value_field].iloc[0], dict):
        df[value_field] = df[value_field].apply(lambda x: x.get('value', None))

    # if 'top_servers' in data and 'buckets' in data['top_servers']:
    #     buckets = data['top_servers']['buckets']
    #     # Convert to a DataFrame for easier plotting
    #     df = pd.DataFrame(buckets)
    #     # Flatten nested fields like `total_bandwidth.value`
    #     if 'total_bandwidth' in df.columns:
    #         df['total_bandwidth'] = df['total_bandwidth'].apply(lambda x: x['value'])
    # else:
    #     print("Invalid data format: Missing 'top_servers' or 'buckets'.")
    #     return

    # Determine graph type
    if use_llm:
        # Use LLM to assist in determining the graph type
        graph_type = use_llm_for_graph_suggestion(df)
    else:
        graph_type = determine_graph_type(df)
    #graph_type = determine_graph_type(df)
    # Plot the graph
    print(f"Graph Type: {graph_type}")
    plot_graph(df, graph_type)

def determine_graph_type(df):
    """
    Determine the most suitable graph type based on DataFrame columns.
    :param df: DataFrame of processed Elasticsearch data.
    :return: Suggested graph type.
    """
    if 'key' in df.columns and 'total_bandwidth' in df.columns:
        return "bar"  # Bar chart for keys vs total_bandwidth
    return "unknown"

# Optional: Use LLM to assist with graph type determination
def use_llm_for_graph_suggestion(dataframe):
    """
    Use an LLM to determine the most appropriate graph type.
    :param dataframe: Pandas DataFrame of the data.
    :return: Suggested graph type from the LLM.
    """
    prompt = (
        f"Given the following data structure, suggest the best type of graph to visualize it using what is available in matplotlib. Propose only one. Give the type of graph like bar, line, time_series, scatter. It's just the name of the method available. Do not write any extra comments.:\n\n{dataframe.head().to_json()}"
    )
    load_dotenv()
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an expert data visualization assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def plot_graph(df, graph_type):
    """
    Generate a graph based on the type determined.
    :param df: DataFrame of processed Elasticsearch data.
    :param graph_type: Type of graph to create.
    """
    if graph_type == "bar":
        df.plot(kind="bar", x="key", y="total_bandwidth", legend=False)
        plt.xlabel("Server IP")
        plt.ylabel("Total Bandwidth")
        plt.title("Bandwidth by Server")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Unsupported graph type. Unable to plot.")