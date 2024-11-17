from ExchangeRateService import ExchangeRateService
from CurrencyConverter import CurrencyConverter
from ExchangeAPI import ExchangeAPI

if __name__ == "__main__":
    import uvicorn

    # Initialize services
    rate_service = ExchangeRateService()
    converter = CurrencyConverter(rate_service)

    # Initialize the API with the converter
    exchange_api = ExchangeAPI(converter)

    # Run the FastAPI application
    uvicorn.run(exchange_api.app, host="0.0.0.0", port=8000)
