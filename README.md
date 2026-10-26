# 🤖 Building a Data Analytics Agent using LLMs

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PandasAI](https://img.shields.io/badge/PandasAI-2.2.15-green.svg)](https://github.com/Sinaptik-AI/pandas-ai)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.26-orange.svg)](https://github.com/langchain-ai/langchain)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Cloud-purple.svg)](https://groq.com/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellow.svg)](LICENSE)

An intelligent, conversational **Data Analytics Agent** powered by Large Language Models (**LLMs**) and **PandasAI**. This project allows non-technical users and data professionals to query, analyze, clean, and visualize structured datasets through natural language conversations.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture & Workflow](#-architecture--workflow)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dataset Details](#-dataset-details)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Usage & Examples](#-usage--examples)
  - [1. Data Exploration](#1-exploratory-data-analysis-eda)
  - [2. Data Cleaning & Imputation](#2-data-cleaning--imputation)
  - [3. Multi-Turn Conversation & Memory](#3-conversational-filtering--contextual-memory)
  - [4. Automated Data Visualization](#4-automated-visualizations)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Overview

Traditional exploratory data analysis (EDA) often requires writing repetitive SQL or Pandas code. This project bridges that gap by combining:
- **High-speed LLMs (via Groq Cloud)** for reasoning and code synthesis.
- **PandasAI & Custom Response Parsers** for safe, deterministic Python execution and formatted display.
- **Contextual Memory & Connectors** that supply schema semantic context (field descriptions) to minimize LLM hallucinations.

---

## 🏗 Architecture & Workflow

```text
 ┌─────────────────┐       Natural Language Prompt
 │      User       │ ──────────────────────────────────┐
 └─────────────────┘                                   ▼
                                           ┌──────────────────────┐
                                           │  Data Analytics      │
                                           │  Agent (PandasAI)    │
                                           └──────────┬───────────┘
                                                      │
                       Sends Schema & Context         │ Queries LLM
                                  ┌───────────────────┼───────────────────┐
                                  ▼                                       ▼
                       ┌──────────────────────┐               ┌───────────────────────┐
                       │   PandasConnector    │               │      LangChain /      │
                       │ (Dataset + Metadata) │               │   Groq LLM Service    │
                       └──────────────────────┘               └───────────────────────┘
                                  │                                       │
                                  └───────────────────┬───────────────────┘
                                                      │ Generates & Executes Code
                                                      ▼
                                           ┌──────────────────────┐
                                           │ Custom Response      │
                                           │ Parser & Engine      │
                                           └──────────┬───────────┘
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
          ┌─────────────────────────┐                                   ┌─────────────────────────┐
          │  Tabular Data & Stats   │                                   │   Charts & Visuals      │
          │  (Dataframe / Markdown) │                                   │  (Saved to exports/)    │
          └─────────────────────────┘                                   └─────────────────────────┘
```

---

## ✨ Key Features

- **🗣️ Natural Language Querying**: Ask questions in plain English (e.g., *"How many rows are there?"*, *"Show average salary grouped by education level"*).
- **📊 Statistical Summaries & Tables**: Receive rich summary statistics, missing value tables, and distributions on demand.
- **🧹 Interactive Data Cleaning**: Instruct the agent to impute missing values or drop unnecessary columns directly on the dataset.
- **🧠 Multi-Turn Memory**: Keeps track of recent conversation history (`memory_size`) for follow-up questions and refined constraints.
- **📈 Automated Visualizations**: Automatically generates charts (bar charts, line plots, etc.) and saves them to `exports/charts/`.
- **🏷️ Semantic Field Descriptions**: Enhances accuracy by feeding rich column descriptions into the agent connector.

---

## 🛠 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** (3.10+) | Core programming language |
| **PandasAI** (v2.2.15) | Conversational AI wrapper for tabular data manipulation |
| **LangChain** (v0.3.26) | LLM chaining, memory, and orchestration |
| **LangChain Groq** | Fast inference integration with Groq Cloud (`qwen/qwen3-32b`, etc.) |
| **Pandas & NumPy** | In-memory data processing and mathematical computations |
| **Flask** (v3.1.1) | Backend framework for web service & API expansion |
| **Python-dotenv** | Secure environment configuration management |

---

## 📂 Project Structure

```text
Building-a-Data-Analytics-Agent-using-LLMs/
├── Dataset/
│   └── ai_job_dataset.csv            # AI Job Market dataset used for analysis
├── exports/
│   └── charts/
│       └── temp_chart.png            # Generated visualization charts
├── research/
│   └── trials.ipynb                  # Prototyping notebook & agent experiments
├── src/
│   ├── __init__.py                   # Package initializer
│   ├── helper.py                     # Helper functions and utilities
│   └── prompt.py                     # Prompt templates and custom instructions
├── .env.example                      # Sample environment variables file
├── .gitignore                        # Git ignore patterns
├── LICENSE                           # Apache 2.0 License
├── pandasai.log                      # Execution log file (ignored in git)
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
├── setup.py                          # Setup configuration for package installation
└── template.sh                       # Shell script to scaffold directory structure
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

## ⚡ Getting Started

### Prerequisites

- Python 3.10 or higher
- A Groq Cloud API Key (or OpenAI API Key)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hammadrehmani/Building-a-Data-Analytics-Agent-using-LLMs.git
   cd Building-a-Data-Analytics-Agent-using-LLMs
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install local package in editable mode:**
   ```bash
   pip install -e .
   ```

### Environment Variables

Create a `.env` file in the root directory:
```bash
GROQ_API_KEY="your_groq_api_key_here"
```

---

## 💡 Usage & Examples

### Quick Start with Python / Jupyter

Launch Jupyter Notebook and explore [`research/trials.ipynb`](research/trials.ipynb):

```python
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pandasai import Agent
from pandasai.connectors import PandasConnector

# 1. Load Environment & LLM
load_dotenv()
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0
)

# 2. Load Dataset
df = pd.read_csv("Dataset/ai_job_dataset.csv")

# 3. Initialize Connector & Agent
connector = PandasConnector({"original_df": df})
agent = Agent(connector, config={"llm": llm, "enable_cache": False})
```

### Example Queries

#### 1. Exploratory Data Analysis (EDA)
```python
agent.chat("How many rows and columns are there?")
agent.chat("Provide statistics about the data in a table form.")
agent.chat("Show missing values in tabular form.")
```

#### 2. Data Cleaning & Imputation
```python
agent.chat("What is the currency for company location France except null?")
agent.chat("Impute the missing currency values by EUR, apply changes to original data.")
agent.chat("Drop the job_description_length field from original data.")
```

#### 3. Conversational Filtering & Contextual Memory
```python
agent.chat("Find jobs where Industry is Education and remote_ratio is 100.")
# Follow-up with retained memory:
agent.chat("Now allow remote ratio less than 100, but require years of experience > 5.")
```

#### 4. Automated Visualizations
```python
agent.chat("Show average salary grouped by experience level as a bar chart.")
# Chart will be generated and saved to exports/charts/
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/NewFeature`).
3. Commit your Changes (`git commit -m 'Add NewFeature'`).
4. Push to the Branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the Apache 2.0 License. See [LICENSE](LICENSE) for more information.

---

## 👤 Author

- **Muhammad Hammad**
  - Email: [mhammad.data@gmail.com](mailto:mhammad.data@gmail.com)
  - GitHub: [@hammadrehmani](https://github.com/hammadrehmani)