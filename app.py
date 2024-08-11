# Imports
import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

# Variable setting and Flask initialization
app = Flask(__name__)

# Function defining
def get_coins(currency):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': currency,
        'order': 'market_cap_desc',
        'per_page': 20,
        'page': 1,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        # Fallback to reading from a CSV file if the API request fails
        if os.path.exists('data-saves/backup_data.csv'):
            df = pd.read_csv('data-saves/backup_data.csv')
            return df.to_dict(orient='records')
        print("Error fetching data from CoinGecko and no backup data available")
        return []  # Return an empty list to indicate failure

# Flask routing
@app.route('/')
def home():
    items = get_coins("USD")
    return render_template('index.html', items=items)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Retrieve selected coins and number of days from the form
    selected_coins = request.form.getlist('coins')
    days = request.form.get('days', '30')
    currency = "USD"
    coin_market_list= ""
    # Retrieve coin data
    data = get_coins(currency)
    for coin_id in data:  
        url2=f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
        params2 = {
        'vs_currency': 'usd',
        'days': days
        }
        #Same as before but has 2s for readbiltity and so the code doesn't make any mistakes
        response = requests.get(url2, params=params2)


    # Extract price data
    prices = data['prices']
    if response.status_code != 200:
        return "Error fetching data from CoinGecko", 500
        

    data = response.json()
    if 'prices' not in data:
        return "Invalid data format received from CoinGecko", 500
    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')  # Ensure timestamp is in datetime format
    df.to_csv('data-saves/backup_data.csv', index=False)

    # Build coin_id string
    coin_id = " + ".join(selected_coins)
    
    # Plot data
    plt.figure(figsize=(10, 5))
    df.plot(
        kind='line',
        x='Timestamp',
        y='Price',
        color='blue',
        alpha=0.9,
        title=f'{coin_id.capitalize()} Price Over Last {days} Days'
    )

    # Saves plot to a file in static (flask checks here)
    plot_path = 'static/data.jpg'
    plt.savefig(plot_path)
    plt.close()

    return render_template('result.html', coin_id=coin_id, days=days, plot_path=plot_path, items=get_coins(currency))

# Main Loop 
if __name__ == '__main__':
    app.run(debug=True)
