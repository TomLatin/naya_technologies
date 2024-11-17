# Currency Exchange Service and ETL Processor

This project consists of two main components:
1. **ExchangeRateService API(exchange_service.py)**: A FastAPI-based REST API that provides currency conversion based on predefined exchange rates.
2. **ETL Processor (etl_exchange.py)**: A script that loads transaction data from a CSV file, calls the ExchangeRateService API, and adds the `target_amount` column with the converted amount for each transaction.

## Prerequisites

- **Python Version**: 3.9.0 or higher.
- **Required Libraries**: The libraries required to run the scripts are listed in the `requirements.txt` file.

## Installation

1. Clone or download the repository.
2. Navigate to the project folder and run the following command to install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the ExchangeRateService API (`exchange_service.py`)

The `exchange_service.py` file starts a FastAPI application that provides a REST API for currency conversion.

### On Windows:

1. Open Command Prompt or PowerShell.
2. Navigate to the directory containing `exchange_service.py`.
3. Run the following command:
    ```bash
    uvicorn exchange_service:app --reload --host 0.0.0.0 --port 8000
    ```
4. The service will be available at `http://localhost:8000/exchange`.

### API Details

- **Endpoint**: `/exchange`
- **Method**: `GET`
- **Parameters**:
  - `source_currency`: The source currency code (e.g., USD).
  - `target_currency`: The target currency code (e.g., ILS).
  - `amount`: The amount to be converted (e.g., 100.0).
- **Response**: A JSON object with the `converted_amount`.

Example request:
```bash
GET http://localhost:8000/exchange?source_currency=USD&target_currency=ILS&amount=100.0
```

## Running the ETL Processor (etl_exchange.py)
The etl_exchange.py script processes transactions from a CSV file, calls the ExchangeRateService API to get the 
converted amounts, and saves the results as a JSON file.

Please note that you have correctly run exchange_service.py and it is working.

### On Windows:
1. Open Command Prompt or PowerShell.
2. Navigate to the directory containing etl_exchange.py.
3. Run the following command:
    ```bash
        python etl_exchange.py path_to_input_csv path_to_output_json
    ```
   
### Arguments:
* Input CSV File: etl_exchange.py expects an input CSV file with the following columns: source_currency, target_currency, and amount.
* Output JSON File: The script will create a JSON file with the processed data, which will include the target_amount column.