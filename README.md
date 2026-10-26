# 🤖 AI Data Analysis Agent using LLMs

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama--3.3--70B-f55036.svg)](https://groq.com/)
[![PandasAI](https://img.shields.io/badge/PandasAI-2.2.15-green.svg)](https://github.com/Sinaptik-AI/pandas-ai)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.26-orange.svg)](https://github.com/langchain-ai/langchain)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellow.svg)](LICENSE)

An intelligent, full-stack **AI Data Analysis & Visualization Agent** that empowers users to query, analyze, clean, and visualize structured datasets through natural language conversations. Powered by **FastAPI**, **Groq LPU Inference**, and **PandasAI / LangChain**, the system handles arbitrary CSV and Excel datasets, dynamically writes and executes Python analysis code, and returns instant data summaries and interactive charts.

---

## 📌 Table of Contents

- [Features](#-features)
- [Architecture & Workflow](#-architecture--workflow)
- [Project Structure](#-project-structure)
- [Dataset Details](#-dataset-details)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
- [Running the Application](#-running-the-application)
  - [Option A: Full-Stack Web App (FastAPI)](#option-a-full-stack-web-app-fastapi)
  - [Option B: Jupyter Notebook Research (PandasAI)](#option-b-jupyter-notebook-research-pandasai)
- [Example Queries](#-example-queries)
- [API Endpoints](#-api-endpoints)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Features

- **Natural Language Data Queries**: Ask arbitrary questions about your dataset without writing SQL or Pandas code manually.
- **Automated Visualizations**: Dynamically generates matplotlib charts (bar charts, line graphs, scatter plots, distributions) on demand.
- **Multi-Format Support**: Works seamlessly with both **CSV** (`.csv`) and **Excel** (`.xlsx`) files.
- **Ultra-Fast LLM Inference**: Powered by Groq's high-throughput LPU inference (`llama-3.3-70b-versatile` / `qwen/qwen3-32b`).
- **Modern Interactive UI**: Responsive web frontend with drag-and-drop file upload, query history, live status badges, and embedded visualization viewers.
- **REST API & Interactive Docs**: Built on **FastAPI** with CORS support, async file handling, and auto-generated Swagger UI / OpenAPI documentation.
- **Research & Experimentation Sandbox**: Includes exploratory Jupyter Notebook trials testing PandasAI agent pipelines and memory retention.

---

## 🏗️ Architecture & Workflow

```mermaid
graph TD
    User([User / Web Browser]) -->|1. Uploads CSV/XLSX + Query| FastAPI[FastAPI Server :8000]
    FastAPI -->|2. Pass file & question| Agent[AI Agent Engine]
    Agent -->|3. Inspect schema, types & sample| DataContext[DataFrame Context]
    DataContext -->|4. Structured Prompt| Groq[Groq LPU: Llama-3.3-70B]
    Groq -->|5. Generate Python Pandas/Matplotlib Code| Agent
    Agent -->|6. Safe Code Execution| ExecEnv[Python Execution Environment]
    ExecEnv -->|7a. Textual Insight| Result[Analysis Result]
    ExecEnv -->|7b. Save Plot| Chart[static/charts/temp_chart.png]
    Result & Chart -->|8. JSON Response| FastAPI
    FastAPI -->|9. Render Output & Chart| User
```

---

## 📁 Project Structure

```text
├── Dataset/
│   └── ai_job_dataset.csv     # Sample global AI job market dataset
├── app.py                     # FastAPI application & API endpoints
├── research/
│   └── trials.ipynb           # Jupyter notebook exploring PandasAI & LangChain
├── src/
│   ├── __init__.py
│   ├── agent.py               # Core LLM prompt generation & execution engine
│   ├── helper.py              # Helper functions and utilities
│   ├── prompt.py              # Prompt templates and custom instructions
│   └── utils.py               # Utility functions & directory helpers
├── static/
│   ├── charts/                # Directory for dynamic chart outputs
│   ├── css/
│   │   └── style.css          # Frontend styling
│   └── js/
│       └── script.js          # Client-side form handling and AJAX
├── templates/
│   └── index.html             # Jinja2 web interface template
├── uploads/                   # Stored dataset files
├── .env.example               # Template for environment variables
├── requirements.txt           # Python package dependencies
├── setup.py                   # Package setup configuration
└── README.md                  # Project documentation
```

---

## 📊 Dataset Details

The default dataset ([Dataset/ai_job_dataset.csv](Dataset/ai_job_dataset.csv)) contains global AI job market records with features including:
- `job_id`: Unique identifier for each posting
- `job_title`: Advertised role title
- `salary_usd`: Standardized annual salary in USD
- `salary_currency`: Original salary currency
- `experience_level`: Entry (`EN`), Mid (`MI`), Senior (`SE`), Executive (`EX`)
- `employment_type`: Full-time (`FT`), Part-time (`PT`), Contract (`CT`), Freelance (`FL`)
- `company_location` & `employee_residence`: ISO country codes
- `company_size`: Small (`S`), Medium (`M`), Large (`L`)
- `remote_ratio`: 0 (Onsite), 50 (Hybrid), 100 (Remote)
- `required_skills`: Technical skill list
- `education_required`, `years_experience`, `industry`, `benefits_score`

---

## 🛠️ Prerequisites

Ensure you have the following installed:
- **Python**: `3.10` or higher
- **Groq API Key**: Obtain a free API key from [Groq Console](https://console.groq.com/keys).

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/hammadrehmani/Building-a-Data-Analytics-Agent-using-LLMs.git
cd Building-a-Data-Analytics-Agent-using-LLMs
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Environment Configuration
Create a `.env` file in the project root directory (or copy from `.env.example`):
```bash
cp .env.example .env
```
Open `.env` and add your Groq API key:
```env
GROQ_API_KEY="gsk_your_actual_groq_api_key"
```

---

## 🖥️ Running the Application

### Option A: Full-Stack Web App (FastAPI)

Start the development server with **Uvicorn**:

```bash
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Once running, navigate to:
- **Web Interface:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Option B: Jupyter Notebook Research (PandasAI)

Launch Jupyter Notebook to explore conversational data analysis with PandasAI:

```bash
jupyter notebook research/trials.ipynb
```

```python
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pandasai import Agent
from pandasai.connectors import PandasConnector

# 1. Load Environment & LLM
load_dotenv()
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)

# 2. Load Dataset
df = pd.read_csv("Dataset/ai_job_dataset.csv")

# 3. Initialize Connector & Agent
connector = PandasConnector({"original_df": df})
agent = Agent(connector, config={"llm": llm, "enable_cache": False})

# 4. Chat with your dataset
agent.chat("How many rows and columns are there?")
agent.chat("Show average salary grouped by experience level as a bar chart")
```

---

## 💡 Example Queries

Upload a dataset (such as `Dataset/ai_job_dataset.csv`) and try asking:
- *"Show me the summary statistics of the dataset."*
- *"Which experience level has the highest average salary? Plot a bar chart."*
- *"Find the correlation between years of experience and salary and plot a scatter plot."*
- *"Show the distribution of remote work ratio across different industries."*
- *"Find jobs where Industry is Education and remote_ratio is 100."*

---

## 📡 API Endpoints

### `GET /`
Serves the web application user interface.

### `POST /analyze`
Analyzes an uploaded dataset based on a natural language prompt.
- **Parameters (Multipart Form-Data)**:
  - `file`: The `.csv` or `.xlsx` file.
  - `query`: String containing your question or instruction.
- **Response**:
  ```json
  {
    "answer": "Analysis result text...",
    "has_chart": true,
    "chart_url": "/static/charts/temp_chart.png"
  }
  ```

---

## 📜 License

Distributed under the Apache 2.0 License. See [LICENSE](LICENSE) for more information.

---

## 👤 Author

**Muhammad Hammad**  
- GitHub: [@hammadrehmani](https://github.com/hammadrehmani)
- Email: [mhammad.data@gmail.com](mailto:mhammad.data@gmail.com)
