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
              
        df 
        return response
    except requests.RequestException:
        # Fallback to reading from a csv file if the API request fails
        if os.path.exists('data-saves/backup_coin_list.csv'):
            df = pd.read_csv('data-saves/backup_data.csv', on_bad_lines='warn')
            return df
        return("Error fetching data from CoinGecko and no backup data available", 500)

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
    coins_data = get_coins(currency)
    csv_df = pd.DataFrame(columns=['Coin Id','Timestamp', 'Price'])
    csv_df.to_csv("data-saves/backup_data.csv")
    #if 'prices' not in coins_data:
    #    return "Invalid data format received from CoinGecko", 500

    #when using the inbuilt debugging i found a major flaw it needs a coin to display all the prices
    prices = coins_data['prices']

    #Convert to DataFrame for Pandas
    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    
    # Make sure this works
    coin_id = ""
    for coin in selected_coins:
        coin_id+= f"{coin}'s +"


    # This plots the data displayed to a plot in the background (doesn't show)
    plt.figure(figsize=(10, 5))
    df.plot(
        kind='line',
        x='Timestamp',
        y='Price',
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
