from fastapi import FastAPI, HTTPException

from CurrencyConverter import CurrencyConverter


class ExchangeAPI:
    def __init__(self, converter: CurrencyConverter):
        self.app = FastAPI()
        self.converter = converter
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/exchange")
        def exchange(source_currency: str, target_currency: str, amount: float) -> dict:
            try:
                converted_amount = self.converter.currency_convert(
                    source_currency, target_currency, amount
                )
                return {
                    "source_currency": source_currency,
                    "target_currency": target_currency,
                    "amount": amount,
                    "converted_amount": converted_amount,
                }
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
