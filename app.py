# Imports ma stuff
import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import os

# Variable setting and Flask initialization
#Probs need to do an API key that reads from an .env file (wont commit cause of a gitignore bypass)
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
        # Fallback to reading from a csv file if the API request fails
        if os.path.exists('data-saves/backup_data.csv'):
            df = pd.read_csv('data-saves/backup_data.csv')
            # another weird line that may work but it gives back the data organised in a particaulr way so that the program doesn't have to remove heaps
            return df.to_dict(orient='records')
        print("Error fetching data from CoinGecko and no backup data available", 500)

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
    # currency = request.form.get() maybe add this
    # Default to 30 days if no value is provided
    # Redirecter in case you try to glitch the application (type in a link)
    if not selected_coins:
        return redirect(url_for('home'))

    if 'prices' not in get_coins(currency):
        return "Invalid data format received from CoinGecko", 500

    prices = get_coins(currency)['prices']

    #Convert to DataFrame for Pandas
    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    df.to_csv("data-saves/backup_data.csv")
    # Make sure this works
    coin_id = ""
    for coin in selected_coins:
        coin_id+= f"{coin}'s +"
        if coin_id != "" or selected_coins == "":
            coid_id += "+"

    # This plots the data displayed to a plot in the background (doesn't show)
    plt.figure(figsize=(10, 5))
    df.plot(
        kind='line',
        x='timestamp',
        y='price',
        color='blue',
        alpha=0.9,
        # This is needing a change (thought I changed this but apparently not) 
        title=f'{coin_id.capitalize()} Price Over Last {days} Days'
    )
    # You know funnily this pulls an error and it says its unlikely to work (becuase its outside the main loop (not really but matplotlib thinks that)) but it hasnt failed yet soooooo?
    # Saves plot to a file in static (flask checks here )
    plot_path = 'static/data.jpg'
    plt.savefig(plot_path)
    plt.close()
    return render_template('result.html', coin_id=coin_id, days=days, plot_path=plot_path, items=get_coins())
#Main Loop
# Because my code is laid in variables and the Flask routing the actual main loop is two lines and my code is super readable
if __name__ == '__main__':
    app.run(debug=True)