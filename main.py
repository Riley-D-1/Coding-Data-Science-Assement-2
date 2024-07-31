import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
app = Flask(__name__)
base_url = 'https://api.coingecko.com/api/v3/coins'
#The coin id is defaultly set to bitcoin
coin_id="bitcoin"
endpoint = f'{base_url}/{coin_id}/market_chart'
params = {
    'vs_currency': 'usd',
    'days': '30'
}

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

items = get_coins()

@app.route('/')
def home():
    return render_template('index.html',items=items,coin_id=coin_id)

# Fetch data
"""
response = requests.get(endpoint, params=params)
data = response.json()

# Extract price data
prices = data['prices']

# Convert to DataFrame
df = pd.DataFrame(prices, columns=['timestamp', 'price'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Plot data
df.plot(
    kind='line',
    x='timestamp',
    y='price',
    color='blue',
    alpha=0.9,
    title=f'{coin_id.capitalize()} Price Over Last 30 Days'
)



plt.savefig('templates/images/data.jpg')
"""

if __name__ == '__main__':
    app.run(debug=True)