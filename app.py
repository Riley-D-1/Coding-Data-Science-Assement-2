import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

def get_coins():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 20,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

@app.route('/')
def home():
    items = get_coins()
    return render_template('index.html', items=items)

@app.route('/plot', methods=['GET'])
def plot():
    coin_id = request.args.get('coin', 'bitcoin')  # Default to 'bitcoin' if no coin is selected
    days = request.args.get('days', '30')  # Default to 30 days if no value is provided
    endpoint = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days
    }

    response = requests.get(endpoint, params=params)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    #Plot functionalties
    plt.figure(figsize=(10, 5))
    df.plot(
        kind='line',
        x='timestamp',
        y='price',
        color='blue',
        alpha=0.9,
        title=f'{coin_id.capitalize()} Price Over Last {days} Days'
    )

    # Save plot to a jpg for the website
    plot_path = 'static/data.jpg'
    plt.savefig(plot_path)
    plt.close()

    return render_template('result.html', coin_id=coin_id, days=days, plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
