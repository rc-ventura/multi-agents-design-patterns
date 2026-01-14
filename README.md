# 🤖 Multi-Agents Design Patterns

A comprehensive collection of **Multi-Agent Systems (MAS)** design patterns implemented across different frameworks. This repository serves as a reference implementation for building complex, agentic workflows using **LangGraph**, **Google ADK**, and **CrewAI**.

![Architecture Overview](assets/Screenshot%202026-01-13%20at%208.56.54%E2%80%AFAM.png)

## 🚀 Overview

The goal of this project is to demonstrate how to implement common agentic patterns described in the [Google ADK Multi-Agent Patterns Guide](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/). We aim to provide clear, "small code" examples for:

1.  **LangGraph** (State-based orchestration)
2.  **Google ADK** (Native reference implementation)
3.  **CrewAI** (Role-based orchestration)

## 📂 Project Structure

```text
multi-agents-design-patterns/
├── adk-google-patterns/       # Google ADK implementations
├── crew-patterns/             # CrewAI implementations
├── lang-patterns/             # LangGraph & LangChain implementations
│   └── sequential-pipeline/   # Example: PDF Parsing -> Extraction -> Summary
├── assets/                    # Diagrams and Screenshots
├── pyproject.toml             # Dependency management (uv)
└── README.md                  # Documentation
```

## 🧩 Design Patterns

### 1. Sequential Pipeline (The Chain)
A linear flow where the output of one agent becomes the input of the next. Ideal for data processing pipelines (e.g., ETL, Document Processing).

*   **Implementations:**
    *   ✅ `lang-patterns/sequential-pipeline`
    *   🚧 `adk-google-patterns/sequential-pipeline` (Planned)
    *   🚧 `crew-patterns/sequential-pipeline` (Planned)

---

### 2. Parallel Fan-Out / Fan-In (The Swarm)
Executes multiple agents in parallel to perform independent tasks (e.g., Security Review, Style Check, Performance Analysis) and aggregates their results into a single output.

![Parallel Pattern](assets/Screenshot%202026-01-13%20at%204.07.30%E2%80%AFPM.png)

*   **Use Case:** Code Review, Multi-perspective analysis.
*   **Implementations:**
    *   🚧 `lang-patterns/parallel-fan-out`
    *   🚧 `adk-google-patterns/parallel-fan-out`
    *   🚧 `crew-patterns/parallel-fan-out`

---

### 3. Coordinator-Dispatcher (The Router)
A central "Brain" (Coordinator) analyzes the user's intent and routes the task to the most appropriate specialized agent (Dispatcher).

![Coordinator Pattern](assets/Screenshot%202026-01-13%20at%204.08.02%E2%80%AFPM.png)

*   **Use Case:** Customer Support (Routing to Billing vs Tech Support), Complex Query Routing.
*   **Implementations:**
    *   🚧 `lang-patterns/coordinator-dispatcher`
    *   🚧 `adk-google-patterns/coordinator-dispatcher`
    *   🚧 `crew-patterns/coordinator-dispatcher`

## ⚡ Getting Started

This project uses **[uv](https://github.com/astral-sh/uv)** for ultra-fast dependency management.

### Prerequisites
- Python 3.12+
- `uv` installed
- Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/multi-agents-design-patterns.git
   cd multi-agents-design-patterns
   ```

2. **Initialize and Install Dependencies:**
   We use a single root configuration for simplicity.
   ```bash
   uv init
   uv add langchain-google-genai langgraph langchain python-dotenv crewai google-genai
   ```

3. **Configure Credentials:**
   Create a `.env` file in the root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

### Running an Example

```bash
# Run the Sequential Pipeline (LangGraph)
uv run lang-patterns/sequential-pipeline/agent.py
```

## 🤝 Contributing
Feel free to open issues or submit PRs to add new patterns or frameworks!

## 📄 License
MIT
