import pandas as pd
import requests
import json
from tqdm import tqdm
from typing import Optional

# URL for the Exchange Rate API (assuming it's running on localhost)
EXCHANGE_API_URL = "http://localhost:8000/exchange"  # Replace with the correct URL if needed


def fetch_exchange_rate(row: pd.Series) -> Optional[float]:
    """
    Fetch the exchange rate from the API and return the converted amount.
    """
    source_currency = row['source_currency']
    target_currency = row['target_currency']
    amount = row['amount']

    params = {
        "source_currency": source_currency,
        "target_currency": target_currency,
        "amount": amount
    }

    try:
        response = requests.get(EXCHANGE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["converted_amount"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate for {source_currency} to {target_currency}: {e}")
        return


def process_transactions(csv_file: str, output_file: str) -> None:
    """
    Load transactions from CSV, fetch exchange rates for each transaction,
    and create a target_amount column. Save the results as JSON.
    """
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Check if the necessary columns exist
    if 'source_currency' not in df or 'target_currency' not in df or 'amount' not in df:
        raise ValueError("CSV must contain 'source_currency', 'target_currency', and 'amount' columns.")

    # Initialize progress bar
    tqdm.pandas()

    # Apply the fetch_exchange_rate function to each row in the DataFrame with progress bar
    df['target_amount'] = df.progress_apply(fetch_exchange_rate, axis=1)

    # Save results as JSON
    results = df.to_dict(orient='records')
    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Processing complete. Results saved to {output_file}")


if __name__ == "__main__":
    # Replace with the actual path to your CSV file and desired output file
    input_csv = "transaction.csv"
    output_json = "transactions_with_target_amount.json"

    process_transactions(input_csv, output_json)
