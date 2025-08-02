import pandas as pd
import pdfplumber

def parse(pdf_path: str) -> pd.DataFrame:
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        transactions = []
        balance = 0

        for page in pages:
            for table in page.extract_tables():
                for row in table:
                    if len(row) >= 3:
                        date = row[0].strip()
                        desc = row[1].strip()
                        amount_str = row[2].strip().replace(',', '')

                        
                        try:
                           amount = float(amount_str)
                        except ValueError:
                          continue

                        balance += amount
                        transactions.append((date, desc, amount, balance))

    df = pd.DataFrame(transactions, columns=['Date', 'Transaction Description', 'Amount', 'Balance'])
    #  Convert float to int for assertion matching
    df['Amount'] = df['Amount'].astype(int)
    df['Balance'] = df['Balance'].astype(int)

    return df
