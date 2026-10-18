import csv
 
CSV_FILE = "BankOfCanadaExchangeRate.2026.csv"
 
 
class ExchangeRates:
    """Loads the latest Bank of Canada exchange rates from a CSV file.
 
    Each column (e.g. FXAUSDCAD) holds how many CAD one unit of that
    currency is worth. The last row in the file is the latest rate.
    """
 
    def __init__(self, filename):
        # utf-8-sig strips the hidden BOM character at the start of the file
        with open(filename, newline="", encoding="utf-8-sig") as f:
            rows = [row for row in csv.reader(f) if row]  # skip blank lines
 
        header = rows[0]
        latest = rows[-1]
        self.date = latest[0]
 
        # CAD is the base currency, so 1 CAD = 1 CAD
        self.rates = {"CAD": 1.0}
        for column, value in zip(header[1:], latest[1:]):
            if value.strip():  # skip currencies with no rate in the latest row
                code = column[3:6]  # "FXAUSDCAD" -> "USD"
                self.rates[code] = float(value)
 
    def currencies(self):
        """Return the list of currency codes that have a rate."""
        return sorted(self.rates)
 
    def convert(self, amount, from_currency, to_currency):
        """Convert an amount from one currency to another."""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
 
        for code in (from_currency, to_currency):
            if code not in self.rates:
                raise ValueError(f"No exchange rate available for {code}.")
 
        # Convert to CAD first, then from CAD to the target currency
        amount_in_cad = amount * self.rates[from_currency]
        return amount_in_cad / self.rates[to_currency]
 
 
def prompt_amount():
    """Ask for a non-negative amount until the user enters a valid number."""
    while True:
        text = input("Enter the amount: ").strip().replace("$", "").replace(",", "")
        try:
            amount = float(text)
        except ValueError:
            print("Invalid amount. Please enter a number (e.g. 100 or 100.50).")
            continue
        if amount < 0:
            print("Please enter a non-negative amount.")
            continue
        return amount
 
 
def prompt_currency(label, rates):
    """Ask for a currency code until the user enters one that has a rate."""
    while True:
        code = input(f"Enter the '{label}' currency (e.g. USD or CAD): ").strip().upper()
        if code in rates.rates:
            return code
        print(f"Unknown currency '{code}'. Available: {', '.join(rates.currencies())}")
 
 
def main():
    rates = ExchangeRates(CSV_FILE)
    print(f"Using Bank of Canada rates from {rates.date}")
 
    amount = prompt_amount()
    from_currency = prompt_currency("from", rates)
    to_currency = prompt_currency("to", rates)
 
    result = rates.convert(amount, from_currency, to_currency)
    print(f"\n${amount:,.2f} {from_currency} = ${result:,.2f} {to_currency}")
 
 
if __name__ == "__main__":
    main()