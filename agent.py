import os
import importlib.util
from pathlib import Path
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

from test_parser import test_icici_parser
from langchain_openai import ChatOpenAI

client = ChatOpenAI(model="gpt-4")


def clean_code_snippet(code: str) -> str:
    """Clean extra markdown and remove text after `return df`."""
    # Remove markdown headers and non-code lines
    import re
    code_lines = code.splitlines()
    clean_lines = [line for line in code_lines if not re.match(r'^\s*(#|```|This|Example)', line)]

    code = "\n".join(clean_lines)

    # Trim anything after `return df`
    if "return df" in code:
        code = code[:code.find("return df") + len("return df")]

    # Trim any excess content before def
    if "def parse(" in code:
        code = code[code.find("def parse("):]

    return code.strip()


def generate_parser_code(csv_preview, bank_name):
    prompt_template = PromptTemplate.from_template("""
You are a senior Python developer. Write a Python parser for a bank statement PDF.

The function must be:

```python
def parse(pdf_path: str) -> pd.DataFrame:
Use only pdfplumber and pandas.

The output DataFrame must match this CSV structure:

{csv_preview}

Write only the function definition (no test code, no CLI).
""")

    prompt = prompt_template.format(csv_preview=csv_preview, bank_name=bank_name)
    response = client.invoke([HumanMessage(content=prompt)])
    raw_code = response.content.strip("` \n")

    # Clean the code before saving
    code = clean_code_snippet(raw_code)

    print("🔍 Generated Code:\n", code)  # Debug print

    return code


def save_parser(code, bank_name):
    output_dir = Path("custom_parsers")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"{bank_name.lower()}_parser.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f" Saved parser to {file_path}")
    return file_path


def load_and_test_parser(parser_path, sample_pdf_path):
    try:
        spec = importlib.util.spec_from_file_location("parser_module", parser_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except SyntaxError as e:
        print(f" Syntax error in parser: {e}")
        return False

    try:
        df = module.parse(sample_pdf_path)
        print(" Test run successful! Sample output:")
        print(df.head())
        return True
    except Exception as e:
        print(f" Runtime error during parser test: {e}")
        return False


def main(target_bank):
    sample_csv_path = Path("data") / f"{target_bank}.csv"
    sample_pdf_path = Path("data") / f"{target_bank}.pdf"

    if not sample_csv_path.exists() or not sample_pdf_path.exists():
        print(f" Missing data for target bank: {target_bank}")
        return

    csv_preview = sample_csv_path.read_text(encoding="utf-8")

    for attempt in range(3):
        print(f"\n Attempt {attempt+1} to generate parser...")
        code = generate_parser_code(csv_preview, target_bank)
        parser_path = save_parser(code, target_bank)
        if load_and_test_parser(parser_path, sample_pdf_path):
            break
    else:
        print(" Failed after 3 attempts.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Target bank name (e.g., icici)")
    args = parser.parse_args()
    if args.target == "icici":
        test_icici_parser()
