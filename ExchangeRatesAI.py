import csv


class ExchangeRates:
    """Reads a Bank of Canada exchange rate file and converts between USD and CAD."""

    PAIR_COLUMN = "FXAUSDCAD"  # CAD per 1 USD

    def __init__(self, filename):
        self.filename = filename
        self.usd_cad = self._read_latest_rate()

    def _read_latest_rate(self):
        # utf-8-sig strips the byte-order mark at the start of the file
        with open(self.filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if self.PAIR_COLUMN not in (reader.fieldnames or []):
                raise ValueError(f"Column {self.PAIR_COLUMN} not found in {self.filename}")
            rate = None
            for row in reader:
                value = row[self.PAIR_COLUMN].strip()
                if value:
                    rate = float(value)  # keep the last non-empty rate
        if rate is None:
            raise ValueError(f"No {self.PAIR_COLUMN} rate found in {self.filename}")
        return rate

    def convert(self, amount, from_currency, to_currency):
        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()
        valid = ("USD", "CAD")
        if from_currency not in valid or to_currency not in valid:
            raise ValueError("Currencies must be USD or CAD")
        if from_currency == to_currency:
            return amount
        if from_currency == "USD":
            return amount * self.usd_cad
        return amount / self.usd_cad


def main():
    rates = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")
    print(f"Latest USD/CAD exchange rate: {rates.usd_cad}")

    try:
        amount = float(input("Enter the amount: "))
    except ValueError:
        print("Invalid amount.")
        return
    from_currency = input("Convert from (USD or CAD): ")
    to_currency = input("Convert to (USD or CAD): ")

    try:
        result = rates.convert(amount, from_currency, to_currency)
    except ValueError as e:
        print(e)
        return
    print(f"{amount:,.2f} {from_currency.strip().upper()} = {result:,.2f} {to_currency.strip().upper()}")


if __name__ == "__main__":
    main()
