import requests
import json
import os

def check_exchange_rates(date, currency): #date format is yyyy-mm-dd
    response = requests.get(f'https://api.frankfurter.dev/v1/{date}?base=ILS&symbols={currency}')
    return response.json()["rates"][currency]

def exchange_money(date, amount, currency): #date format is yyyy-mm-dd
    currency = currency.upper()
    if currency == 'ILS':
        return amount
    else:
        response = requests.get(f'https://api.frankfurter.dev/v1/{date}?base={currency}&symbols=ILS')
        rates = float(response.json()["rates"]['ILS'])
        new_amount = round(amount * rates, 2)
        return new_amount

def return_currencies_from_api():
    response = requests.get(f'https://api.frankfurter.dev/v1/latest').json()
    output = []
    for currency in response['rates'].keys():
        output.append(currency)
    return output
