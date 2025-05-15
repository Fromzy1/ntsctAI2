# ntsctAI — LLM Reasoning Interface for Network Observability

This is an internal prototype I built in 3 days to explore how LLMs could assist in interpreting complex network telemetry data through natural language reasoning.  
It leverages OpenAI GPT to simulate an agentic workflow: receiving high-level questions and inferring which metrics, fields, or anomalies are relevant.

## 🧠 What It Does

- Translates plain questions (e.g. “Was there any DNS anomaly yesterday?”) into metric exploration
- Uses prompt-based reasoning to infer relevant KPIs (e.g., `pkt_loss`, `dns_latency`, `query_response_ratio`)
- Applies Model Context Protocol logic: separates reasoning (agent) from data lookup (tool)
- Uses simple file-based responses to simulate tool execution

## 🚧 Why I Built It

Following an informal conversation with a customer who said:  
*“It would be great if we could just ask an LLM ‘what’s going on?’ and get an answer that interprets the available data,”*  
I decided to give it a try.

It took me less than a week of spare-time work to build a working prototype.  
The goal was not to build a full product, but to explore whether we could simulate useful, domain-specific reasoning on top of existing network and security telemetry.

This became a thinking tool for internal discussion and a first step toward agentic automation in operational environments.

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

