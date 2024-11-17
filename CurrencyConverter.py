from ExchangeRateService import ExchangeRateService


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
