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

    def add_rate(self, source_currency: str, target_currency: str, rate: float):
        self.rates[(source_currency, target_currency)] = rate
        self.rates[(target_currency, source_currency)] = 1 / rate

