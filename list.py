from flask import Flask, jsonify
import requests

app = Flask(__name__)

BLOCKCHAIR_API_KEY = 'YOUR_BLOCKCHAIR_API_KEY'
ADDRESS_TO_CHECK = 'YOUR_ADDRESS_TO_CHECK'
START_DATE = '2023-05-20'
END_DATE = '2023-07-26'  # Use today's date as the end date

@app.route('/deposits', methods=['GET'])
def get_deposits():
    url = f'https://api.blockchair.com/bitcoin/dashboards/address/{ADDRESS_TO_CHECK}'
    params = {
        'from': START_DATE,
        'to': END_DATE,
        'apikey': BLOCKCHAIR_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    deposits = []
    for tx in data['data'][ADDRESS_TO_CHECK]['transactions']:
        if tx['type'] == 'funding':
            tx_id = tx['transaction']['hash']
            date = tx['transaction']['time']
            crypto_amount = tx['value']
            # Optionally, you can convert the crypto amount to USD using an external API
            # Here, we'll assume the conversion rate is stored in `crypto_to_usd_rate`
            # Replace this with a real API call if needed.
            crypto_to_usd_rate = 5000  # Replace this with a real rate.
            usd_amount = crypto_amount * crypto_to_usd_rate

            deposit_info = {
                'tx_id': tx_id,
                'date': date,
                'crypto_amount': crypto_amount,
                'usd_amount': usd_amount,
            }
            deposits.append(deposit_info)

    return jsonify(deposits)

if __name__ == '__main__':
    app.run(debug=True)
