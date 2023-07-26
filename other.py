from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
def get_crypto_deposits(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from the URL.")

    soup = BeautifulSoup(response.text, 'html.parser')
    balance_rows = soup.find_all('div', class_='account-hash__balance__row')

    btc_amount = None
    usd_amount = None

    for row in balance_rows:
        caption = row.find('span', class_='account-hash__balance__caption')
        if caption and caption.text.strip() == "Total received":
            values = row.find_all('span', class_='wb-ba')
            if len(values) >= 2:
                btc_amount = float(values[0].text.strip())
                usd_amount = float(values[1].text.strip().replace(',', ''))

    return {
        'crypto_amount_btc': btc_amount,
        'usd_amount': usd_amount
    }

@app.route('/received_funds', methods=['GET'])
def scraper():
    # Load the spreadsheet (CSV file) using pandas
    spreadsheet_path = 'wallets.csv'
    df = pd.read_csv(spreadsheet_path)

    crypto_data = {}  # To store the scraped data for each wallet address

    for address in df['old_bitcoin_address']:
        url = f"https://blockchair.com/bitcoin/address/{address}"
        try:
            amounts = get_crypto_deposits(url)
            crypto_data[address] = amounts
        except Exception as e:
            crypto_data[address] = {'error': str(e)}

    return jsonify(crypto_data)

if __name__ == "__main__":
    app.run(debug=True)
