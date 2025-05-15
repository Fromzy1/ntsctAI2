# ntsctAI — LLM Reasoning Interface for Network Observability

This is an internal prototype I built in 3 days to explore how LLMs could assist in interpreting complex network telemetry data through natural language reasoning.  
It leverages OpenAI GPT to simulate an agentic workflow: receiving high-level questions and inferring which metrics, fields, or anomalies are relevant.

## 🧠 What It Does

- Translates plain questions (e.g. “Was there any DNS anomaly yesterday?”) into metric exploration
- Uses prompt-based reasoning to infer relevant KPIs (e.g., `pkt_loss`, `dns_latency`, `query_response_ratio`)
- Applies Model Context Protocol logic: separates reasoning (agent) from data lookup (tool)
- Uses simple file-based responses to simulate tool execution

## 🚧 Why I Built It

At NETSCOUT, I’ve seen a clear opportunity to bridge traditional network observability with AI-powered assistants.  
This project is a proof of concept aimed at internal stakeholders (Product Management) to show how fast we can build usable agents without waiting for full retraining or integration.

It’s not a complete product — but a **thinking tool** and a **first step** towards agentic automation in security and observability contexts.

## 🔍 Sample Prompt (see `/prompt_1.txt`)

## 💡 Example Queries

- **Top applications by session count:**
  > "What are the top 10 applications with the most active sessions? Graph a heat map."

- **Timeouts vs bandwidth:**
  > "What are the application name with the most time outs? Is it related to their bandwidth usage?"

<!-- HTML-style images for size control -->
<div align="center">
  <img src="screenshots/heatmap_example.png" width="400"/>
  <img src="screenshots/timeout_bandwidth.png" width="400"/>
</div>

## 🛠 Technologies

- Python + FastAPI
- OpenAI GPT-4 (API)
- Prompt engineering
- Elastic

## 📦 Structure

- `ntsctAI.py` – core loop (reasoning + tool interaction)
- `prompt_1.txt` / `prompt_2.txt` – Prompt templates to guide query generation
- `ElasticTools.py`: Executes ES queries
- `chart_util.py`: Plots results using matplotlib/seaborn

## 🗺️ Next Steps (TODO)

- [ ] Agent-based modularization (e.g. trend agent, anomaly agent)
- [ ] Support for open-source models (e.g. llama.cpp, Ollama)
- [ ] Schema introspection via plugin tools (e.g. MCP)
- [ ] Docker packaging

---

This is not a research project. It's a fast, pragmatic exploration of how LLMs can help real-world IT and security teams interact with their data more intuitively.

## 📄 License

MIT

