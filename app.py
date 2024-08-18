# Imports ma stuff
import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime

# Variable setting and Flask initialization
#Probs need to do an API key that reads from an .env file (wont commit cause of a gitignore bypass)
app = Flask(__name__)
token_place=open("token.txt", "r")
api_key= token_place.readline()
time_now = datetime.timestamp(datetime.now())

# Function 

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
        data = response.json()
        coin_list_df = pd.DataFrame.from_dict(data)
        coin_list_df.drop(coin_list_df.iloc[:, 2:26], axis=1,inplace=True)
        coin_list_df.to_csv('data-saves/backup_coin_list.csv')
        return coin_list_df.to_dict(orient="records")
    except requests.RequestException:
        # Fallback to reading from a csv file if the API request fails
        if os.path.exists('data-saves/backup_coin_list.csv'):
            coin_list_backup_df = pd.read_csv('data-saves/backup_coin_list.csv', on_bad_lines='warn')
            return coin_list_backup_df.to_dict(orient="records")
        return("Error fetching data from CoinGecko and no backup data available", 500)


def get_coins_data(currency,coin_list,from_,to_):
    params2= {
            'vs_currency': currency,    
            'precision': 5,
            'to':to_,
            'from':from_,
        
        }
    
    #Notes- to is current time. from is in the past
    headers={'x-cg-demo-api-key': api_key}
    coins_data = []
    try:
        for id in coin_list:
            url2=f"https://api.coingecko.com/api/v3/coins/{id}/market_chart/range"  
            response=requests.get(url2,params=params2,headers=headers)
            data2=response.json()
            coins_data.append(data2)
            if requests.RequestException:
                print("error "+id)
        coins_df = pd.DataFrame(coins_data)
        coins_df.drop(coins_df.iloc[:, 1:3], axis=1,inplace=True)
        coins_df.to_csv('data-saves/backup_data.csv')
        return coins_df
    except requests.RequestException:
        # Fallback to reading from a csv file if the API request fails
        if os.path.exists('data-saves/backup_data.csv'):
            df = pd.read_csv('data-saves/backup_data.csv', on_bad_lines='warn')
            return df
        return("Error fetching data from CoinGecko and no backup data available", 500)

    
def Unix_to_timestamp(days):
    var =time_now - (int(days)*86400)
    return int(var)

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
    # Default to 30 days if no value is provided
    currency = "USD"
    coins_ = pd.read_csv('data-saves/backup_coin_list.csv')
    coin_list = (coins_['id'])

    # currency = request.form.get() maybe add this
    
    # Redirecter in case you try to glitch the application (type in a link)
    if not selected_coins:
        return redirect(url_for('home'))
    coins_data = get_coins_data(currency,coin_list,Unix_to_timestamp(365),int(time_now))
        #if 'prices' not in coins_data:
    #    return "Invalid data format received from CoinGecko", 500
    #when using the inbuilt debugging i found a major flaw it needs a coin to display all the prices
    
    plot_info_df = coins_data

    # Make sure this works
    title_name = ""
    for coin in selected_coins:
        title_name += f"{coin}'s +"
    # This plots the data displayed to a plot in the background (doesn't show)
    plt.figure(figsize=(10, 5))
    plot_info_df.plot(
        kind='line',
        x='date',
        y='prices',
        color='blue',
        alpha=0.9,
        # This is needing a change (thought I changed this but apparently not) 
        title=f'{title_name.capitalize()} Price Over Last {days} Days'
    )
    # You know funnily this pulls an error and it says its unlikely to work (becuase its outside the main loop (not really but matplotlib thinks that)) but it hasnt failed yet soooooo?
    # Saves plot to a file in static (flask checks here )
    plot_path = 'static/data.jpg'
    plt.savefig(plot_path)
    plt.close()
    return render_template('result.html')
#Main Loop
# Because my code is laid in variables and the Flask routing the actual main loop is two lines and my code is super readable. debugging is left on for debugging purposes (shocking)
if __name__ == '__main__':
    app.run(debug=True)
