import csv

class ExchangeRates:
    def __init__(self, filename):
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                pass

        self.usd_to_cad = float(row["FXAUSDCAD"])

    def convert(self, amount, from_currency, to_currency):
        if from_currency == "USD" and to_currency == "CAD":
            return amount * self.usd_to_cad
        elif from_currency == "CAD" and to_currency == "USD":
            return amount / self.usd_to_cad

amount = float(input("Enter the amount: "))
from_currency = input("Enter the from currency (USD or CAD): ").upper()
to_currency = input("Enter the to currency (USD or CAD): ").upper()

converter = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")

result = converter.convert(amount, from_currency, to_currency)

print(result)