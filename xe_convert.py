import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_exchange_rate(curr_one, curr_two):
    url = f"https://v6.exchangerate-api.com/v6/{os.getenv('ER_API_KEY')}/pair/{curr_one}/{curr_two}"
    response = requests.get(url)

    # Print the URL to ensure it's correct
    print(f"Fetching exchange rate from URL: {url}")

    if response.status_code == 200:
        data = response.json()
        if data["result"] == "success":
            exchange_rate = data["conversion_rate"]
            return exchange_rate
        else:
            raise ValueError(f"Error fetching exchange rate: {data['error-type']}")
    else:
        raise ValueError(
            f"Error fetching exchange rate: HTTP Status {response.status_code}"
        )


if __name__ == "__main__":
    print("\n*** Get Exchange Rate ***\n")

    currency_one = input("\nPlease enter Currency 1: ")
    currency_two = input("\nPlease enter Currency 2: ")

    try:
        exchange_rate = get_exchange_rate(currency_one, currency_two)
        print("\n")
        print("{:,.4f}".format(float(exchange_rate)))
    except ValueError as e:
        print(f"Error: {e}")
