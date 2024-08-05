import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
from mpld3._server import serve
from datetime import datetime
import pytz
#All imports (yes there is a lot, but they all play a role )
#Variable setting
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

@app.route('/plot', methods=['POST'])
def plot():
    current_time = datetime.now(pytz.timezone('Australia/Sydney'))
    time_data=(f"{current_time.time()}_{current_time.date()}")
    csv_save_data=""
    for char in time_data:
        if char == ":":
            csv_save_data += "_"
        else:
            csv_save_data += char

    # Retrieve selected coins and number of days from the form
    selected_coins = request.form.getlist('coins')
    days = request.form.get('days', '30')  # Default to 30 days if no value is provided

    if not selected_coins:
        return redirect(url_for('home'))

    coin_id = selected_coins[0]
    endpoint = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days
    }




    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        return "Error fetching data from CoinGecko", 500
        

    data = response.json()
    if 'prices' not in data:
        return "Invalid data format received from CoinGecko", 500
    
    prices = data['prices']
    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.to_csv('data-saves/'+csv_save_data + '.csv', mode='a', header=False, index=False)


    # Plot data
    plt.figure(figsize=(10, 5))
    df.plot(
        kind='line',
        x='timestamp',
        y='price',
        color='blue',
        alpha=0.9,
        title=f'{coin_id.capitalize()} Price Over Last {days} Days'
    )

    # Save plot to a file for website
    plot_path = 'static/data.jpg'
    plt.savefig(plot_path)
    plt.close()

    return render_template('result.html', coin_id=coin_id, days=days, plot_path=plot_path, items=get_coins())

if __name__ == '__main__':
    app.run(debug=True)
