import requests

# Function to get the exchange rate from the API
def get_exchange_rate(from_currency, to_currency):
    api_key = 'YOUR_API_KEY'  # Replace with your API key from exchangeratesapi.io
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['rates'].get(to_currency)

        if exchange_rate:
            return exchange_rate
        else:
            print(f"Currency {to_currency} not found!")
            return None
    else:
        print("Failed to fetch exchange rates!")
        return None

# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    exchange_rate = get_exchange_rate(from_currency, to_currency)

    if exchange_rate:
        converted_amount = amount * exchange_rate
        return converted_amount
    else:
        return None

# Main program
if __name__ == "__main__":
    print("Currency Converter")
    
    # Input from the user
    amount = float(input("Enter the amount to convert: "))
    from_currency = input("From currency (e.g., USD): ").upper()
    to_currency = input("To currency (e.g., EUR): ").upper()

    # Convert the currency
    result = convert_currency(amount, from_currency, to_currency)

    if result:
        print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
    else:
        print("Conversion failed!")
