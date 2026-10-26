import os
import io
import sys
import textwrap
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — must come before pyplot
import matplotlib.pyplot as plt

from groq import Groq

# app.py calls _load_env_file() before importing us, so the key is already
# in os.environ by the time this module is loaded.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip().strip("'\"")


def _read_api_key_directly() -> str:
    """Read GROQ_API_KEY directly from the .env file in the parent directory of src/."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    if k.strip() == "GROQ_API_KEY":
                        val = v.strip().strip("'\"")
                        if val:
                            return val
        except Exception as e:
            print(f"Error reading .env directly: {e}")
    return os.environ.get("GROQ_API_KEY", "").strip().strip("'\"")


def _get_client() -> Groq:
    """Return a Groq client. Key is read directly from .env file or os.environ."""
    key = _read_api_key_directly()
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. "
            "Please add it to your .env file in the root directory: GROQ_API_KEY=gsk_..."
        )
    return Groq(api_key=key)


CHARTS_DIR = os.path.join("static", "charts")
CHART_FILENAME = "temp_chart.png"


def _strip_markdown(code: str) -> str:
    """Remove ```python / ``` fences if the LLM added them."""
    code = code.strip()
    if code.startswith("```python"):
        code = code[len("```python"):]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()


def analyze_dataset(file_path: str, question: str) -> str:
    """
    Load a CSV/Excel file, ask the Groq LLM to write analysis code,
    execute it safely, and return the result as a string.

    Charts are saved to static/charts/temp_chart.png automatically.
    """
    # ── Load data ────────────────────────────────────────────────────────
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        return "Unsupported file format. Please upload a CSV or Excel file."

    # ── Prepare charts directory ──────────────────────────────────────────
    os.makedirs(CHARTS_DIR, exist_ok=True)
    chart_dest = os.path.abspath(os.path.join(CHARTS_DIR, CHART_FILENAME))
    if os.path.exists(chart_dest):
        try:
            os.remove(chart_dest)
        except Exception:
            pass
    plt.close("all")

    # ── Build data context for the LLM ───────────────────────────────────
    df_info = (
        f"Shape: {df.shape}\n"
        f"Columns: {list(df.columns)}\n"
        f"Dtypes:\n{df.dtypes.to_string()}\n"
        f"Sample (first 5 rows):\n{df.head().to_string()}"
    )

    # ── Build prompt ──────────────────────────────────────────────────────
    chart_path_safe = chart_dest.replace("\\", "\\\\")
    prompt = textwrap.dedent(f"""
        You are a Python data-analysis expert.

        A pandas DataFrame called `df` is already in scope with the following info:
        {df_info}

        User question: {question}

        Write Python code that answers the question. STRICT rules:
        1. `df` is already loaded — do NOT read any file.
        2. `matplotlib.pyplot` is imported as `plt` (Agg backend, non-interactive).
        3. `pandas` is imported as `pd`.
        4. If you create a chart, end with EXACTLY these two lines:
               plt.savefig(r'{chart_dest}', bbox_inches='tight', dpi=150)
               plt.close()
           Do NOT call plt.show().
        5. Store the textual answer in a variable named `result` (string).
           If the answer is a number or DataFrame, convert it: result = str(...).
        6. Output ONLY raw executable Python. No markdown fences, no prose.
    """).strip()

    # ── Call Groq API ─────────────────────────────────────────────────────
    client = _get_client()
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Python data analysis expert. "
                    "Output ONLY raw executable Python code — no markdown, no explanations."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=2048,
    )

    code = _strip_markdown(chat.choices[0].message.content)
    print(f"[agent] Generated code:\n{code}\n")

    # ── Execute the generated code ────────────────────────────────────────
    local_vars: dict = {"df": df, "plt": plt, "pd": pd}
    stdout_buf = io.StringIO()

    try:
        old_stdout = sys.stdout
        sys.stdout = stdout_buf
        exec(code, local_vars)          # nosec — intentional code execution
        sys.stdout = old_stdout
    except Exception as exc:
        sys.stdout = sys.__stdout__
        return (
            f"⚠️ The generated code raised an error: {exc}\n\n"
            f"**Generated code:**\n```python\n{code}\n```"
        )

    # ── Collect result ────────────────────────────────────────────────────
    result = local_vars.get("result", None)
    if result is None:
        captured = stdout_buf.getvalue().strip()
        result = captured if captured else "Analysis complete."

    return str(result)