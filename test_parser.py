import pandas as pd
from custom_parsers.icici_parser import parse



def test_icici_parser():
    expected = pd.read_csv("data/icici/icici_sample.csv")
    output = parse("data/icici/icici_sample.pdf")
    # Clean both DataFrames before comparing
    expected.columns = expected.columns.str.strip()
    output.columns = output.columns.str.strip()

    for col in expected.columns:
        expected[col] = expected[col].astype(str).str.strip()
        output[col] = output[col].astype(str).str.strip()

    print("\n🔍 Differences:")
    print("EXPECTED:")
    print(expected)
    print("\nOUTPUT:")
    print(output)

    
    assert expected.equals(output), "❌ Output doesn't match expected DataFrame"