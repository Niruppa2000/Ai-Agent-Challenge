# Ai-Agent-Challenge

# 🤖 Agent-as-Coder: Karbon AI Challenge

A coding agent that automatically writes a custom parser for bank statement PDFs using LLMs.

## 🧪 How it Works

Agent loop:
1. Read PDF & sample CSV.
2. Generate parser using Groq's LLM.
3. Save it to `custom_parsers/{bank}_parser.py`.
4. Test against sample CSV using `pandas.DataFrame.equals()`.
5. Retry (max 3) on failure.

## 🛠️ How to Run

```bash
git clone https://github.com/Niruppa2000/ai-agent-challenge
cd ai-agent-challenge

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set your Groq API Key
export GROQ_API_KEY=your_key_here

# Run agent
python agent.py --target icici

# Run test
pytest test_parser.py
