from fastapi import FastAPI, HTTPException

app = FastAPI()


class ExchangeRateService:
    """
    Manages exchange rates and provides methods to retrieve rates and find valid conversion paths.
    """
    def __init__(self):
        self.rates = {
            ("USD", "ILS"): 3.2,
            ("EUR", "ILS"): 3.5,
            ("GBP", "ILS"): 4.3,
            ("EUR", "USD"): 1.1,
        }
        self._add_reverse_rates()

    def _add_reverse_rates(self):
        for (src, tgt), rate in list(self.rates.items()):
            self.rates[(tgt, src)] = 1 / rate

    def get_rate(self, source_currency: str, target_currency: str):
        return self.rates.get((source_currency, target_currency), None)

    def find_intermediate(self, source_currency: str, target_currency: str):
        """
        Find an intermediate currency for a two-step conversion.
        """
        for intermediate_currency in {cur for (cur, _) in self.rates.keys()}:
            if self.get_rate(source_currency, intermediate_currency) and \
               self.get_rate(intermediate_currency, target_currency):
                return intermediate_currency
        return None


class CurrencyConverter:
    """
    Handles currency conversion logic, including applying commissions for two-step transactions.
    """
    def __init__(self, rate_service: ExchangeRateService, commission_rate: float = 1.01):
        self.rate_service = rate_service
        self.commission_rate = commission_rate

    def currency_convert(self, source_currency: str, target_currency: str, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if source_currency == target_currency:
            return amount  # No conversion needed

        # Direct conversion
        rate = self.rate_service.get_rate(source_currency, target_currency)
        if rate:
            return amount * rate

        # Two-step conversion with intermediate currency
        intermediate_currency = self.rate_service.find_intermediate(source_currency, target_currency)
        if intermediate_currency:
            # Step 1: Source to Intermediate
            rate_to_intermediate = self.rate_service.get_rate(source_currency, intermediate_currency)
            intermediate_amount = amount * rate_to_intermediate

            # Step 2: Intermediate to Target
            rate_to_target = self.rate_service.get_rate(intermediate_currency, target_currency)
            final_amount = intermediate_amount * rate_to_target
            final_amount_with_commission = final_amount * self.commission_rate  # Apply commission

            return final_amount_with_commission

        # No valid conversion path
        raise ValueError("Exchange path not found.")


# Initialize services
rate_service = ExchangeRateService()
converter = CurrencyConverter(rate_service)


@app.get("/exchange")
def exchange(source_currency: str, target_currency: str, amount: float):
    """
    API endpoint to convert currencies.
    """
    try:
        converted_amount = converter.currency_convert(source_currency, target_currency, amount)
        return {
            "source_currency": source_currency,
            "target_currency": target_currency,
            "amount": amount,
            "converted_amount": converted_amount
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
