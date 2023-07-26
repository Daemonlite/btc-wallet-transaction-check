from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

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

@app.route('/scraper', methods=['GET'])
def scraper():
    address = '31iCTFexVS7NQbhPJkpSSxEf6c2LYuVUnk'
    url = f"https://blockchair.com/bitcoin/address/{address}"
    amounts = get_crypto_deposits(url)
    return jsonify(amounts)

if __name__ == "__main__":
    app.run(debug=True)