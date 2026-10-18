import csv

class ExchangeRates:
    def __init__(self, filename):
    # open the csv file that has the Bank of Canada Exchange Rates
        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            # read through the rows in the csv file 
            for row in reader:
                pass

        # store the USD to CAD rate as a decimal number
        self.usd_to_cad = float(row["FXAUSDCAD"])

    def convert(self, amount, from_currency, to_currency):
        # convert USD to CAD
        if from_currency == "USD" and to_currency == "CAD":
            return amount * self.usd_to_cad

        # convert CAD to USD
        elif from_currency == "CAD" and to_currency == "USD":
            return amount / self.usd_to_cad

# ask the user for the amount and currencies 
amount = float(input("Enter the amount: "))
from_currency = input("Enter the from currency (USD or CAD): ").upper()
to_currency = input("Enter the to currency (USD or CAD): ").upper()

# create an ExchangeRate object using the csv file
converter = ExchangeRates("BankOfCanadaExchangeRate.2026.csv")

# convert the entered amount 
result = converter.convert(amount, from_currency, to_currency)

# display to the nearest penny, as dollar amount
print(f"${amount:,.2f} {from_currency} = ${result:,.2f} {to_currency}")