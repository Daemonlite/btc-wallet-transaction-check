from flask import Flask, jsonify
from blockcypher import get_address_full
import json


# Function to calculate USD amount from Satoshi value and exchange rate
def calculate_usd_amount(satoshi_amount, exchange_rate):
    return satoshi_amount * exchange_rate

app = Flask(__name__)

@app.route('/deposit')
def get_deposits():
    try:
        # change this to a list of addresses
        btc_addresses = [
            '31shz3veznNJt2QDyYgxNtp45JwCZHtey7',
            '324TfcS61q73U3Bk5BoN8QTF7Qb9ipQJtt',
            '327phgtLdDkE3aT4Fe4paavaNy8i6SHCu4'
        ]
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
                date = tx['received']
                deposit_data = {
                    'transaction_id': transaction_id,
                    'crypto_amount': crypto_amount,
                    'usd_amount': usd_amount,
                    'date':date
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


if __name__ == '__main__':
    app.run(debug=True)


