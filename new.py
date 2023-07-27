from flask import Flask, jsonify
from blockcypher import get_address_full
import json
import pandas as pd

# Function to calculate USD amount from Satoshi value and exchange rate
def calculate_usd_amount(satoshi_amount, exchange_rate):
    return satoshi_amount * exchange_rate

app = Flask(__name__)

@app.route('/deposits')
def get_deposits():
    try:
        btc_addresses = read_btc_addresses_from_csv("wallets.csv")
        all_deposits = []

        for address in btc_addresses:
            response = get_address_full(address)
            transactions = response.get('txs', [])

            # Prepare the response data for this address
            deposits = []
            for tx in transactions:
                transaction_id = tx['hash']
                crypto_amount = sum([inp['output_value'] for inp in tx['inputs'] if address in inp['addresses']])
                usd_amount = calculate_usd_amount(tx['total'], 0.000041)  # Replace '0.000041' with the actual exchange rate

                deposit_data = {
                    'transaction_id': transaction_id,
                    'crypto_amount': crypto_amount,
                    'usd_amount': usd_amount,
                }
                deposits.append(deposit_data)

            # Add the deposits for this address to the overall list
            all_deposits.extend(deposits)

        # Save the JSON response to a new file
        with open('deposits_response.json', 'w') as file:
            json.dump(all_deposits, file)

        return jsonify(all_deposits)

    except Exception as e:
        # Handle exceptions gracefully
        error_response = {
            'error': 'An error occurred while processing the request.',
            'message': str(e)
        }
        return jsonify(error_response), 500

def read_btc_addresses_from_csv(file_path):
    df = pd.read_csv(file_path)
    btc_addresses = df['old_bitcoin_address'].str.strip().tolist()
    return btc_addresses

if __name__ == '__main__':
    app.run(debug=True)


